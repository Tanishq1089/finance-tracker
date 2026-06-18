from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, func
from sqlalchemy.orm import relationship
import enum
from ..database import Base

class Category(str, enum.Enum):
    food = "food"
    transport = "transport"
    utilities = "utilities"
    entertainment = "entertainment"
    health = "health"
    shopping = "shopping"
    other = "other"

class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(Enum(Category), nullable=False)
    description = Column(String, default="")
    date = Column(DateTime, server_default=func.now())

    owner = relationship("User", back_populates="expenses")