# Rafid — What It Is

*Source document 1 of 7. Self-contained: assumes no knowledge of the other files.*

---

## The one-line version

**Rafid takes a badly written CV, rewrites it into a strong one, then finds live freelance work that fits it — all inside a Discord chat, and it sends one job suggestion every morning without being asked.**

Measured result: the same CV went from **42/100 to 73/100**, two points short of a professionally written version of the same person.

---

## The name

**Rafid** (رافد) is Arabic for *a tributary — the smaller stream that feeds a larger river* — and also *one who supports or provides*. Renamed from "Sanad" partway through the build; the Day 1–4 reports still use the old name as a dated record.

---

## What problem it solves

Applying for freelance work has two failure points, and they compound.

**The first is the CV.** Most people's CVs are honest but badly written — responsibilities instead of results, no numbers anywhere, formatting an applicant tracking system cannot parse. The person cannot see the problem, because they wrote it.

**The second is the search.** Freelance boards return hundreds of projects a day, almost none relevant. Reading them is the whole job.

Solving only the second problem — which is what the predecessor project did — assumes the CV is already good. Rafid fixes the CV **first**, then matches with the improved version.

---

## What it actually does

1. **Reviews** your CV. You send a PDF in a Discord DM; it asks you 8–15 specific questions about the vague parts, then returns a score out of 100 plus a full report as a PDF.
2. **Rewrites** it. On your approval it produces an optimised CV and a change report, both as PDFs, inventing nothing.
3. **Matches** it against live freelance projects, returning the top five with a pitch written for each.
4. **Remembers** your CV between sessions. Restart everything and it still knows who you are.
5. **Sends one job every morning at 08:00, unprompted.**

Point 5 is what makes it an automation rather than a chatbot, and it is central to the pitch. Everything else waits for you to speak first.

---

## What a conversation actually looks like

```
You     hi
Rafid   Ahlan! I'm Rafid. I help you land freelance work in two steps...
        Start by sending me your CV as a PDF.

You     [synthetic-cv-messy.pdf]
Rafid   Got synthetic-cv-messy.pdf - reading it now. This takes a minute or two.

Rafid   1. What's the target role and seniority you're applying for?
        2. Freelance (2020-present): how many total clients?
        3. How many websites/online stores have you built?
        ... 14 questions total ...
        Answer by number, and skip any you genuinely don't know.

You     1. Junior Full-Stack Developer
        2. Approximately 25 clients
        ...

Rafid   Thanks, these are solid. A few points still need precision:
        1. The 20% sales increase - compared to what baseline, over what window?
        2. "Several thousand products" - do you have an actual number?

You     1. Compared to pre-launch sales, first 3 months.
        2. Approximately 2,000-5,000.

Rafid   Here's the full review - 40/100, Weak. [+ PDF attached]
        Want me to rewrite this?

You     yes
Rafid   Done. Nothing invented. [+ optimised CV PDF] [+ change report PDF]

You     find me work
Rafid   Searching live projects and matching them to your CV - about a minute.
Rafid   5 projects that fit your CV
        1. WordPress & Elementor Enhancements - 80/100 - 8-15 CAD
           > With expertise in WordPress and Elementor, I enhanced the design
             of a homeware e-commerce shop, increasing sales by 20%...
        ...

--- next morning, without being asked ---

Rafid   Good morning - one gig for you today
        Build Indian Personal Finance Web App - 70/100 - 12500-37500 INR
```

---

## What makes it "agentic"

The capstone this was built for is titled **"Agentic AI Application"**. The predecessor project was a deterministic pipeline; this is the layer above it.

| | Predecessor (FreelanceScout) | Rafid |
|---|---|---|
| **Entry point** | one web form | free-form chat, any message |
| **Control flow** | fixed node order | an agent decides intent per message |
| **AI decides** | scoring, pitch writing | *plus* what the user actually wants |
| **The pipeline** | **is** the product | is a **tool the agent calls** |
| **Memory** | none | CV persists across sessions |
| **Initiative** | waits to be triggered | acts on its own every morning |

The real difference is that something must answer, on **every single message**: *is this a CV upload, an answer to a question I asked, an approval, a job request, or just chat?* Nothing is pre-ordained by the trigger.

That routing is done by a language model reading the message. **There is no keyword matching anywhere in it** — the message `I like banana` was correctly routed to conversation rather than to the job search, and answered with a joke before steering back to purpose.

---

## Who it is for

**One person, self-hosted.** Each user runs their own instance. There is no user table, no authentication, no multi-tenancy. This was a deliberate scope cut: it is what made the rest fit in a three-day build window, and it is stated as a limitation rather than hidden.

---

## The demo fixtures

Two CVs of the same fictional person, **Marcus Silva**, a freelance web and e-commerce developer in Lisbon:

- `synthetic-cv-messy.pdf` — the same facts written badly. Scores **42/100**
- `synthetic-cv-polished.pdf` — written well. Scores **75–85** depending on the target role

Both describe the same underlying career, so the demo is a genuine before/after and job matching stays consistent across them. Nothing real is ever sent to a third-party model.

---

## Status

**Feature-complete.** Every requirement in the agreed v1 scope is built and demonstrated:

- Discord DM in and out, with a welcome on first contact
- CV review with intake questions, summary in chat plus PDF
- Rewrite producing optimised CV and change report as PDFs
- Job matching with pitches, top five
- CV persisted between sessions
- Daily 08:00 digest — one unseen gig, or an explicit "nothing new today"

Built over five days: one day of planning, three of building, one of testing and documentation.
