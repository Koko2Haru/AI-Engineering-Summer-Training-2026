import json
import re
from contextlib import asynccontextmanager
from datetime import date
from typing import Literal

import httpx
import ollama
from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, field_validator

import database

MONTH_RE = re.compile(r"^\d{4}-\d{2}$")

# Swap the coach's model here — run `ollama list` to see what's installed locally.
OLLAMA_MODEL = "llama3.2:latest"
OLLAMA_TIMEOUT_SECONDS = 30

COACH_SYSTEM_PROMPTS = {
    "coach": (
        "You are CoinQuest's AI coach: an upbeat, supportive personal finance analyst. "
        "Encourage the player, acknowledge what's going well, and give constructive, "
        "practical advice. Keep a warm, professional tone."
    ),
    "roast": (
        "You are CoinQuest's roast comedian: savage, blunt, and hilarious about the "
        "player's spending habits. Be merciless but funny — never cruel about things "
        "outside their control (like income). Comedy roast, not a personal attack."
    ),
    "pirate": (
        "You are CoinQuest's pirate captain: narrate the player's spending as a "
        "nautical adventure, speaking entirely in pirate slang ('arr', 'matey', 'ye', "
        "'booty', 'plunder'). Stay in character the whole time."
    ),
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs once on startup: make sure the table exists.
    database.init_db()
    yield


app = FastAPI(lifespan=lifespan)


class ExpenseIn(BaseModel):
    amount: float = Field(gt=0)   # no zero or negative spending
    category: str = Field(min_length=1, max_length=40)  # free text (custom "Other" categories)
    note: str = ""
    date: date                    # must be a real YYYY-MM-DD date
    payment_method: Literal["Cash", "Credit"] = "Cash"

    @field_validator("category")
    @classmethod
    def strip_category(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("category must not be blank")
        return v


@app.post("/api/expenses")
def create_expense(expense: ExpenseIn):
    return database.insert_expense(
        amount=expense.amount,
        category=expense.category,
        note=expense.note,
        spent_on=expense.date.isoformat(),  # store as "YYYY-MM-DD" text
        payment_method=expense.payment_method,
    )


@app.get("/api/expenses")
def list_expenses():
    return database.get_expenses()


@app.delete("/api/expenses/{expense_id}", status_code=204)
def delete_expense(expense_id: int):
    if not database.delete_expense(expense_id):
        raise HTTPException(status_code=404, detail="Expense not found")


class BulkDeleteIn(BaseModel):
    ids: list[int]


@app.post("/api/expenses/bulk-delete")
def bulk_delete_expenses(payload: BulkDeleteIn):
    if not payload.ids:
        raise HTTPException(status_code=422, detail="ids must not be empty")
    return {"deleted": database.delete_expenses(payload.ids)}


class BudgetIn(BaseModel):
    cash_budget: float = Field(ge=0)
    credit_budget: float = Field(ge=0)


@app.get("/api/budget")
def get_budget():
    return database.get_budgets()


@app.put("/api/budget")
def update_budget(budget: BudgetIn):
    return database.set_budgets(budget.cash_budget, budget.credit_budget)


@app.get("/api/summary")
def get_summary(month: str | None = Query(default=None)):
    if month is None:
        month = date.today().strftime("%Y-%m")
    elif not MONTH_RE.match(month):
        raise HTTPException(status_code=422, detail="month must be in YYYY-MM format")

    return database.get_summary(month)


@app.get("/api/xp")
def get_xp():
    return {"xp": database.get_idle_xp()}


class CoachIn(BaseModel):
    month: str | None = None
    mode: Literal["coach", "roast", "pirate"] = "coach"


@app.post("/api/coach")
def coach(payload: CoachIn):
    month = payload.month or date.today().strftime("%Y-%m")
    if not MONTH_RE.match(month):
        raise HTTPException(status_code=422, detail="month must be in YYYY-MM format")

    summary = database.get_summary(month)
    if not summary["category_totals"]:
        raise HTTPException(
            status_code=400,
            detail="No expenses logged for this month yet — nothing for the coach to review.",
        )

    # The boss is always the real biggest category, computed in Python — the
    # model only ever narrates a number it's handed, never derives one.
    boss_category = max(summary["category_totals"], key=summary["category_totals"].get)
    boss_damage = summary["category_totals"][boss_category]

    stats_block = (
        f"Month: {month}\n"
        f"Per-category totals (SAR): {summary['category_totals']}\n"
        f"Total spent: {summary['total_spent']:.2f} SAR "
        f"(Cash: {summary['cash_spent']:.2f} SAR, Credit: {summary['credit_spent']:.2f} SAR)\n"
        f"Monthly budget: {summary['budget']:.2f} SAR "
        f"(Cash: {summary['cash_budget']:.2f} SAR, Credit: {summary['credit_budget']:.2f} SAR)\n"
        f"Remaining budget: {summary['remaining']:.2f} SAR\n"
        f"Current streak: {summary['streak']} day(s)\n"
        f"Biggest spending category (this month's boss): {boss_category}, "
        f"totaling {boss_damage:.2f} SAR\n"
    )

    user_prompt = (
        "Here are this month's pre-computed stats. These numbers are final — do not "
        "add, subtract, or recompute anything, only interpret them in words.\n\n"
        f"{stats_block}\n"
        "Reply with STRICT JSON only, no markdown fences, no extra keys, exactly this shape:\n"
        '{"review": "2-3 sentence review of the spending this month", '
        '"tip": "one short actionable saving tip", '
        '"boss": {"name": "a fun invented monster name themed around the biggest '
        'spending category (do not just repeat the category word itself)", '
        '"weakness": "one habit-level tip to defeat this boss"}}'
    )

    try:
        client = ollama.Client(timeout=OLLAMA_TIMEOUT_SECONDS)
        response = client.chat(
            model=OLLAMA_MODEL,
            messages=[
                {"role": "system", "content": COACH_SYSTEM_PROMPTS[payload.mode]},
                {"role": "user", "content": user_prompt},
            ],
            format="json",
        )
        data = json.loads(response["message"]["content"])

        review = str(data["review"])
        tip = str(data["tip"])
        boss_name = str(data["boss"]["name"])
        boss_weakness = str(data["boss"]["weakness"])
    except (
        httpx.HTTPError,
        ConnectionError,  # ollama's client raises the builtin ConnectionError when unreachable
        ollama.ResponseError,
        json.JSONDecodeError,
        KeyError,
        TypeError,
        ValueError,
    ):
        raise HTTPException(
            status_code=502,
            detail="The AI coach is unavailable right now — please try again later.",
        )

    return {
        "review": review,
        "tip": tip,
        "boss": {
            "name": boss_name,
            "damage": boss_damage,  # real Python-computed total, never the model's copy
            "weakness": boss_weakness,
        },
    }


app.mount("/", StaticFiles(directory="static", html=True), name="static")
