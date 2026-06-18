from sqlalchemy import Column, Integer, Float, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from ..database import Base
from .expense import Category

class Budget(Base):
    __tablename__ = "budgets"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category = Column(Enum(Category), nullable=False)
    monthly_limit = Column(Float, nullable=False)
    month = Column(String, nullable=False)

    owner = relationship("User", back_populates="budgets")