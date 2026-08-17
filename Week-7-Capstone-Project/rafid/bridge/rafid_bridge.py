"""Rafid bridge — a tiny local HTTP server that lets n8n talk to Claude Code.

Why this exists
---------------
n8n's Execute Command node spawns with `shell: true, detached: true`, which on
Windows becomes `cmd.exe /d /s /c "<command>"`. Any prompt containing spaces,
quotes or newlines gets mangled, and external executables aren't reliably found
on the child's PATH. Both were confirmed by testing, so Execute Command was
dropped in favour of this.

n8n reaches it with a plain HTTP Request node. The prompt travels as JSON in the
request body and is piped to Claude Code on stdin, so nothing is ever parsed by
a shell.

Standard library only — no pip install.

Run:
    python rafid_bridge.py            # listens on 127.0.0.1:8900

Endpoints
---------
GET  /health
    -> {"ok": true, "claude": "<path>", "version": "..."}

POST /claude
    body: {"session_id": "<uuid>", "prompt": "...", "cwd": "<optional dir>"}
    -> {"ok": true, "session_id": "...", "resumed": true|false, "output": "..."}

    First call for a session_id creates it; later calls resume it. That is what
    keeps the cv-reviewer intake questions working across separate Discord
    messages, since every poll is a separate n8n execution.

POST /md2pdf
    body: {"markdown": "...", "filename": "rafid-review.pdf", "title": "..."}
    -> {"ok": true, "path": "<abs path>", "filename": "...", "bytes": 12345}

    The skills emit Markdown; Discord needs a PDF attachment. n8n cannot run a
    script (Execute Command is the thing this whole file replaces), so the
    bridge renders it. md2pdf.convert() is imported directly rather than
    shelled out to - same process, no quoting, no PATH.

    Files land in ../workspace/, which is gitignored.

POST /fetch
    body: {"url": "https://cdn.discordapp.com/...", "filename": "cv-123.pdf"}
    -> {"ok": true, "path": "<abs path>", "filename": "...", "bytes": 12345}

GET  /file?name=<filename>
    -> the raw file bytes from ../workspace/ (application/pdf)

    Why these exist: n8n 2.x refuses to let the Read/Write File node touch
    arbitrary paths ("Access to the file is not allowed"), so n8n cannot save
    the incoming CV or read back a generated PDF. Rather than making every user
    set N8N_RESTRICT_FILE_ACCESS_TO, the bridge owns all filesystem access and
    n8n only ever speaks HTTP. Same reasoning that replaced Execute Command,
    and it keeps working if n8n moves into a container.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import urllib.request
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

HOST = "127.0.0.1"
PORT = 8900
TIMEOUT = 600  # a full cv-reviewer run can take minutes

# The skills run their own Python (extract_text.py, review_cv.py, ...). Claude
# Code asks permission before running them, and in headless -p mode there is
# nobody to ask - it just replies "I need permission" into the Discord chat.
#
# Permissions are granted per working directory, so this surfaced the moment the
# workspace moved: the old directory had accumulated approvals, the new one had
# none. Bypassing is scoped by the fact that cwd is the workspace, which holds
# only uploaded CVs and generated PDFs. Override if you want it stricter:
#   set RAFID_PERMISSION_MODE=acceptEdits
PERMISSION_MODE = os.environ.get("RAFID_PERMISSION_MODE", "bypassPermissions")

# Runtime scratch: downloaded CVs in, generated PDFs out. Gitignored.
WORKSPACE = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "workspace")
)


def find_claude():
    """Locate the Claude Code executable without relying on the caller's PATH."""
    found = shutil.which("claude")
    if found:
        return found
    candidates = [
        os.path.join(os.environ.get("APPDATA", ""), "npm", "claude.cmd"),
        os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "npm", "claude.cmd"),
        os.path.join(os.path.expanduser("~"), ".claude", "local", "claude"),
    ]
    for c in candidates:
        if c and os.path.isfile(c):
            return c
    return None


CLAUDE = find_claude()


def session_exists(session_id):
    """Claude Code stores transcripts as <session-id>.jsonl under ~/.claude/projects."""
    root = os.path.join(os.path.expanduser("~"), ".claude", "projects")
    if not os.path.isdir(root):
        return False
    target = f"{session_id}.jsonl"
    for dirpath, _dirnames, filenames in os.walk(root):
        if target in filenames:
            return True
    return False


def run_claude(session_id, prompt, cwd=None):
    if not CLAUDE:
        return False, "claude executable not found - npm install -g @anthropic-ai/claude-code", False

    resumed = session_exists(session_id)
    flag = ["--resume", session_id] if resumed else ["--session-id", session_id]
    cmd = [CLAUDE, "-p", *flag]
    if PERMISSION_MODE:
        cmd += ["--permission-mode", PERMISSION_MODE]

    # Claude Code sandboxes file access to its working directory. Default to the
    # workspace, which is where the CV was just written - otherwise the session
    # inherits whatever directory the bridge happened to be launched from and
    # refuses to read the file it was asked to review.
    os.makedirs(WORKSPACE, exist_ok=True)
    workdir = cwd or WORKSPACE

    try:
        proc = subprocess.run(
            cmd,
            input=prompt,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=TIMEOUT,
            cwd=workdir,
            shell=False,  # no shell: the prompt is never parsed by cmd.exe
        )
    except subprocess.TimeoutExpired:
        return False, f"claude timed out after {TIMEOUT}s", resumed

    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout or "").strip()
        return False, f"claude exited {proc.returncode}: {detail[:800]}", resumed

    return True, (proc.stdout or "").strip(), resumed


def safe_name(name, default="rafid-report.pdf"):
    """Reduce a caller-supplied filename to something that cannot escape WORKSPACE."""
    name = os.path.basename(name or "")          # kill any directory component
    name = re.sub(r"[^A-Za-z0-9._-]", "-", name).strip("-.")
    if not name:
        name = default
    if not name.lower().endswith(".pdf"):
        name += ".pdf"
    return name


# --- durable state -----------------------------------------------------------
# n8n's workflow static data is only written when an execution FINISHES. A CV
# review takes minutes while the poll fires every 15s, so eight overlapping
# executions all read the same stale cursor and reprocessed the same message.
# The cursor has to be claimed before the slow work starts, so it lives here
# instead - written synchronously, under a lock.
STATE_LOCK = threading.Lock()


def state_path():
    return os.path.join(WORKSPACE, "state.json")


def read_state():
    try:
        with open(state_path(), encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return {}


def write_state(state):
    os.makedirs(WORKSPACE, exist_ok=True)
    tmp = state_path() + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(state, fh, indent=2)
    os.replace(tmp, state_path())  # atomic on Windows and POSIX


def workspace_path(filename):
    """Resolve a name inside WORKSPACE, refusing anything that escapes it."""
    path = os.path.abspath(os.path.join(WORKSPACE, filename))
    if os.path.commonpath([path, WORKSPACE]) != WORKSPACE:
        raise ValueError("path escapes the workspace")
    return path


def fetch_to_workspace(url, filename, max_bytes=25 * 1024 * 1024):
    """Download a URL straight to WORKSPACE. Used for Discord CV attachments."""
    if not re.match(r"^https?://", url or ""):
        raise ValueError("url must be http(s)")

    os.makedirs(WORKSPACE, exist_ok=True)
    dst = workspace_path(filename)

    req = urllib.request.Request(url, headers={"User-Agent": "rafid-bridge/1.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = resp.read(max_bytes + 1)

    if len(data) > max_bytes:
        raise ValueError(f"file larger than {max_bytes} bytes")

    with open(dst, "wb") as fh:
        fh.write(data)
    return dst


def render_pdf(markdown, filename, title, style="report"):
    """Markdown -> PDF via md2pdf.convert(), in-process.

    `style` picks the look: "report" for the review and change report, "resume"
    for the optimised CV, which needs a denser layout and a name that carries
    the top of the page.

    reportlab is imported lazily so that a machine without it can still use
    /claude - only PDF generation should fail, not the whole bridge.
    """
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.platypus import SimpleDocTemplate

    import md2pdf  # sits beside this file; Python puts the script dir on sys.path

    os.makedirs(WORKSPACE, exist_ok=True)
    dst = os.path.join(WORKSPACE, filename)

    # Keep the source markdown next to the PDF. When output looks wrong it is
    # usually the model's markdown, not the renderer - this makes that a
    # one-second check instead of a guess.
    try:
        with open(os.path.splitext(dst)[0] + ".md", "w", encoding="utf-8") as fh:
            fh.write(markdown)
    except OSError:
        pass  # debugging aid only, never fail the render over it

    left, right, top, bottom = md2pdf.STYLES.get(style, md2pdf.REPORT)["margins"]
    doc = SimpleDocTemplate(
        dst,
        pagesize=A4,
        leftMargin=left * mm,
        rightMargin=right * mm,
        topMargin=top * mm,
        bottomMargin=bottom * mm,
        title=title,
        author="Rafid",
    )
    doc.build(md2pdf.convert(markdown, style=style))
    return dst


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        route = parsed.path.rstrip("/")

        if route == "/file":
            name = (parse_qs(parsed.query).get("name") or [""])[0]
            try:
                path = workspace_path(safe_name(name))
            except ValueError as exc:
                return self._send(400, {"ok": False, "error": str(exc)})
            if not os.path.isfile(path):
                return self._send(404, {"ok": False, "error": f"no such file: {name}"})

            with open(path, "rb") as fh:
                body = fh.read()
            self.send_response(200)
            self.send_header("Content-Type", "application/pdf")
            self.send_header("Content-Length", str(len(body)))
            self.send_header(
                "Content-Disposition", f'attachment; filename="{os.path.basename(path)}"'
            )
            self.end_headers()
            return self.wfile.write(body)

        if route == "/state":
            with STATE_LOCK:
                return self._send(200, {"ok": True, "state": read_state()})

        if route != "/health":
            return self._send(404, {"ok": False, "error": "not found"})
        version = None
        if CLAUDE:
            try:
                version = subprocess.run(
                    [CLAUDE, "--version"], capture_output=True, text=True, timeout=60
                ).stdout.strip()
            except Exception as exc:  # noqa: BLE001 - report, don't crash the probe
                version = f"(version check failed: {exc})"
        self._send(200, {"ok": bool(CLAUDE), "claude": CLAUDE, "version": version})

    def do_POST(self):
        route = urlparse(self.path).path.rstrip("/")
        if route not in ("/claude", "/md2pdf", "/fetch", "/claim", "/state", "/reset"):
            return self._send(404, {"ok": False, "error": "not found"})

        try:
            length = int(self.headers.get("Content-Length") or 0)
            data = json.loads(self.rfile.read(length).decode("utf-8") or "{}")
        except (ValueError, TypeError) as exc:
            return self._send(400, {"ok": False, "error": f"bad JSON body: {exc}"})

        if route == "/md2pdf":
            return self._handle_md2pdf(data)
        if route == "/fetch":
            return self._handle_fetch(data)
        if route == "/claim":
            return self._handle_claim(data)
        if route == "/state":
            return self._handle_state(data)
        if route == "/reset":
            return self._handle_reset()
        return self._handle_claude(data)

    def _handle_reset(self):
        """Forget the conversation, keep the cursor.

        Start a clean demo without replaying the whole DM history: dropping
        session_id and greeted means the next message gets the welcome and opens
        a fresh Claude session, while last_seen_message_id stays put so old
        messages are not reprocessed.
        """
        with STATE_LOCK:
            state = read_state()
            kept = {"last_seen_message_id": state.get("last_seen_message_id")}
            write_state({k: v for k, v in kept.items() if v is not None})
            state = read_state()

        self._send(200, {"ok": True, "reset": True, "state": state})

    def _handle_claim(self, data):
        """Atomically claim a Discord message. Only one caller can ever win."""
        mid = str(data.get("message_id") or "").strip()
        if not mid.isdigit():
            return self._send(400, {"ok": False, "error": "message_id must be a numeric snowflake"})

        with STATE_LOCK:
            state = read_state()
            last = state.get("last_seen_message_id")
            first_contact = not state.get("greeted")

            if last is not None and int(mid) <= int(last):
                return self._send(200, {"ok": True, "claimed": False, "last_seen": last})

            state["last_seen_message_id"] = mid
            state["greeted"] = True
            write_state(state)

        self._send(200, {
            "ok": True,
            "claimed": True,
            "last_seen": mid,
            "is_first_contact": first_contact,
            "session_id": state.get("session_id"),
        })

    def _handle_state(self, data):
        """Merge a patch into the durable state and return the whole thing."""
        patch = data.get("patch")
        if not isinstance(patch, dict):
            return self._send(400, {"ok": False, "error": "patch object is required"})

        with STATE_LOCK:
            state = read_state()
            state.update(patch)
            write_state(state)

        self._send(200, {"ok": True, "state": state})

    def _handle_fetch(self, data):
        url = (data.get("url") or "").strip()
        if not url:
            return self._send(400, {"ok": False, "error": "url is required"})

        filename = safe_name(data.get("filename"), default="download.pdf")
        try:
            path = fetch_to_workspace(url, filename)
        except Exception as exc:  # noqa: BLE001 - report the failure, keep serving
            return self._send(500, {"ok": False, "error": f"fetch failed: {exc}"})

        self._send(200, {
            "ok": True,
            "path": path,
            "filename": filename,
            "bytes": os.path.getsize(path),
        })

    def _handle_claude(self, data):
        prompt = (data.get("prompt") or "").strip()
        if not prompt:
            return self._send(400, {"ok": False, "error": "prompt is required"})

        session_id = data.get("session_id") or str(uuid.uuid4())

        ok, output, resumed = run_claude(session_id, prompt, data.get("cwd"))
        self._send(200 if ok else 500, {
            "ok": ok,
            "session_id": session_id,
            "resumed": resumed,
            "output" if ok else "error": output,
        })

    def _handle_md2pdf(self, data):
        markdown = data.get("markdown") or ""
        if not markdown.strip():
            return self._send(400, {"ok": False, "error": "markdown is required"})

        filename = safe_name(data.get("filename"))
        title = (data.get("title") or "Rafid Report").strip()
        style = (data.get("style") or "report").strip().lower()

        try:
            path = render_pdf(markdown, filename, title, style)
        except ImportError as exc:
            return self._send(500, {
                "ok": False,
                "error": f"reportlab is not installed: {exc} - pip install reportlab",
            })
        except Exception as exc:  # noqa: BLE001 - report the failure, keep serving
            return self._send(500, {"ok": False, "error": f"pdf render failed: {exc}"})

        self._send(200, {
            "ok": True,
            "path": path,
            "filename": filename,
            "bytes": os.path.getsize(path),
        })

    def log_message(self, fmt, *args):
        sys.stderr.write("[rafid-bridge] %s\n" % (fmt % args))


if __name__ == "__main__":
    if not CLAUDE:
        print("WARNING: claude executable not found on this machine.", file=sys.stderr)
    print(f"rafid-bridge listening on http://{HOST}:{PORT}")
    print(f"  claude:    {CLAUDE}")
    print(f"  workspace: {WORKSPACE}")
    print("  GET  /health")
    print("  GET  /file?name=<filename>")
    print("  GET  /state")
    print("  POST /claude  {session_id, prompt, cwd?}")
    print("  POST /md2pdf  {markdown, filename?, title?}")
    print("  POST /fetch   {url, filename?}")
    print("  POST /claim   {message_id}")
    print("  POST /state   {patch: {...}}")
    print("  POST /reset   (forget session + greeting, keep the cursor)")
    print(f"  permission-mode: {PERMISSION_MODE}")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
