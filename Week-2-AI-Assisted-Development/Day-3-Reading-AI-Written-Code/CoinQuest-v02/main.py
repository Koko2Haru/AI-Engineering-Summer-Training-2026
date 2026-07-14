from contextlib import asynccontextmanager
from datetime import date
from enum import Enum

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

import database


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs once on startup: make sure the table exists.
    database.init_db()
    yield


app = FastAPI(lifespan=lifespan)


class Category(str, Enum):
    food = "Food"
    transport = "Transport"
    shopping = "Shopping"
    bills = "Bills"
    other = "Other"


class ExpenseIn(BaseModel):
    amount: float = Field(gt=0)   # no zero or negative spending
    category: Category            # must be one of the known categories
    note: str = ""
    date: date                    # must be a real YYYY-MM-DD date


@app.post("/api/expenses")
def create_expense(expense: ExpenseIn):
    return database.insert_expense(
        amount=expense.amount,
        category=expense.category.value,    # store the plain "Food" string
        note=expense.note,
        spent_on=expense.date.isoformat(),  # store as "YYYY-MM-DD" text
    )


@app.get("/api/expenses")
def list_expenses():
    return database.get_expenses()


app.mount("/", StaticFiles(directory="static", html=True), name="static")
