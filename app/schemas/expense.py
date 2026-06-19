from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ExpenseCreate(BaseModel):
    amount: float = Field(..., gt=0, description="Transaction value must be positive")
    category: str = Field(..., description="Expense category tag")
    description: Optional[str] = Field(None, max_length=255)
    date: Optional[datetime] = None  # ── PASTE/ADD THIS LINE HERE