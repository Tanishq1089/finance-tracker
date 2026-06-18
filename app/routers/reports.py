from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from ..database import get_db
from ..models.expense import Expense
from ..models.budget import Budget
from ..routers.auth import get_current_user

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/monthly-summary")
def monthly_summary(year: int, month: int,
                    db: Session = Depends(get_db), user=Depends(get_current_user)):
    rows = (db.query(Expense.category, func.sum(Expense.amount).label("total"))
              .filter(Expense.user_id == user.id,
                      extract("year",  Expense.date) == year,
                      extract("month", Expense.date) == month)
              .group_by(Expense.category).all())
    month_key = f"{year}-{month:02d}"
    budgets = {b.category: b.monthly_limit for b in
               db.query(Budget).filter(Budget.user_id == user.id, Budget.month == month_key)}
    return [{"category": r.category, "spent": round(r.total, 2),
             "budget": budgets.get(r.category), "over_budget": bool(
             budgets.get(r.category) and r.total > budgets[r.category])} for r in rows]

@router.get("/spending-trend")
def spending_trend(db: Session = Depends(get_db), user=Depends(get_current_user)):
    rows = (db.query(extract("year", Expense.date).label("year"),
                     extract("month", Expense.date).label("month"),
                     func.sum(Expense.amount).label("total"))
              .filter(Expense.user_id == user.id)
              .group_by("year", "month")
              .order_by("year", "month").all())
    return [{"period": f"{int(r.year)}-{int(r.month):02d}", "total": round(r.total, 2)} for r in rows]