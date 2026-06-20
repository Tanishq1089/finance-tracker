from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import extract
from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from ..database import get_db
from ..models.expense import Expense, Category
from ..routers.auth import get_current_user

router = APIRouter(prefix="/expenses", tags=["expenses"])

# --- PYDANTIC SCHEMAS TO SUPPORT HISTORICAL DATES ---
class ExpenseCreate(BaseModel):
    amount: float
    category: str
    description: str = ""
    date: Optional[datetime] = None  # Allows custom transaction date payloads

class ExpenseUpdate(BaseModel):
    amount: Optional[float] = None
    category: Optional[str] = None
    description: Optional[str] = None
    date: Optional[datetime] = None  # Allows updating transaction dates

# --- ROUTE OVERRIDES & BUSINESS LOGIC ---

@router.post("/")
def create_expense(data: ExpenseCreate, db: Session = Depends(get_db),
                   user=Depends(get_current_user)):
    exp = Expense(
        user_id=user.id,
        amount=data.amount,
        category=data.category,
        description=data.description
    )
    
    # Override default timestamp if a custom historical date was sent from frontend
    if data.date:
        exp.date = data.date
        
    db.add(exp)
    db.commit()
    db.refresh(exp)
    
    # Integrated unified clean string serialization format matching GET/PUT maps
    return {
        "id": exp.id, 
        "amount": exp.amount, 
        "category": str(exp.category).split(".")[-1],
        "description": exp.description, 
        "date": exp.date.isoformat()
    }

@router.get("/")
def list_expenses(category: Optional[str] = None,
                  month: Optional[int] = None,
                  year: Optional[int] = None,
                  db: Session = Depends(get_db),
                  user=Depends(get_current_user)):
    q = db.query(Expense).filter(Expense.user_id == user.id)
    if category:
        q = q.filter(Expense.category == category)
    if month:
        q = q.filter(extract("month", Expense.date) == month)
    if year:
        q = q.filter(extract("year", Expense.date) == year)
    results = q.order_by(Expense.date.desc()).all()
    
    # FIXED: Replaced str(e.date) with e.date.isoformat() to ensure UI chart syncing
    return [{
        "id": e.id, 
        "amount": e.amount, 
        "category": str(e.category).split(".")[-1],
        "description": e.description, 
        "date": e.date.isoformat()
    } for e in results]

@router.delete("/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db),
                   user=Depends(get_current_user)):
    exp = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == user.id
    ).first()
    if not exp:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(exp)
    db.commit()
    return {"msg": "Deleted"}

@router.put("/{expense_id}")
def update_expense(expense_id: int, data: ExpenseUpdate,
                   db: Session = Depends(get_db),
                   user=Depends(get_current_user)):
    exp = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == user.id
    ).first()
    if not exp:
        raise HTTPException(status_code=404, detail="Not found")
        
    if data.amount is not None:
        exp.amount = data.amount
    if data.category is not None:
        exp.category = data.category
    if data.description is not None:
        exp.description = data.description
    if data.date is not None:
        exp.date = data.date
        
    db.commit()
    db.refresh(exp)
    
    # FIXED: Replaced str(exp.date) with exp.date.isoformat() to keep data payloads consistent
    return {
        "id": exp.id, 
        "amount": exp.amount,
        "category": str(exp.category).split(".")[-1],
        "description": exp.description, 
        "date": exp.date.isoformat()
    }