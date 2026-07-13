from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import database

app = FastAPI()


@app.on_event("startup")
def startup():
    database.init_db()


class ExpenseIn(BaseModel):
    amount: float
    category: str
    note: str = ""
    date: str


@app.post("/api/expenses")
def create_expense(expense: ExpenseIn):
    return database.insert_expense(
        amount=expense.amount,
        category=expense.category,
        note=expense.note,
        spent_on=expense.date,
    )


@app.get("/api/expenses")
def list_expenses():
    return database.get_expenses()


app.mount("/", StaticFiles(directory="static", html=True), name="static")
