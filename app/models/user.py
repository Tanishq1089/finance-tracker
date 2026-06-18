from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from ..database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    expenses = relationship("Expense", back_populates="owner")
    budgets = relationship("Budget", back_populates="owner")