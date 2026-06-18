from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from ..database import get_db
from ..models.budget import Budget
from ..routers.auth import get_current_user

router = APIRouter(prefix="/budgets", tags=["budgets"])

class BudgetCreate(BaseModel):
    category: str
    monthly_limit: float
    month: str

@router.post("/")
def set_budget(data: BudgetCreate, db: Session = Depends(get_db),
               user=Depends(get_current_user)):
    existing = db.query(Budget).filter(
        Budget.user_id == user.id,
        Budget.category == data.category,
        Budget.month == data.month
    ).first()
    if existing:
        existing.monthly_limit = data.monthly_limit
        db.commit()
        db.refresh(existing)
        return {"id": existing.id, "category": data.category,
                "monthly_limit": existing.monthly_limit, "month": existing.month}
    budget = Budget(
        user_id=user.id,
        category=data.category,
        monthly_limit=data.monthly_limit,
        month=data.month
    )
    db.add(budget)
    db.commit()
    db.refresh(budget)
    return {"id": budget.id, "category": data.category,
            "monthly_limit": budget.monthly_limit, "month": budget.month}

@router.get("/")
def list_budgets(month: Optional[str] = None, db: Session = Depends(get_db),
                 user=Depends(get_current_user)):
    q = db.query(Budget).filter(Budget.user_id == user.id)
    if month:
        q = q.filter(Budget.month == month)
    results = q.all()
    return [{"id": b.id, "category": str(b.category).split(".")[-1],
             "monthly_limit": b.monthly_limit, "month": b.month} for b in results]

@router.delete("/{budget_id}")
def delete_budget(budget_id: int, db: Session = Depends(get_db),
                  user=Depends(get_current_user)):
    b = db.query(Budget).filter(
        Budget.id == budget_id, Budget.user_id == user.id
    ).first()
    if not b:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(b)
    db.commit()
    return {"msg": "Deleted"}