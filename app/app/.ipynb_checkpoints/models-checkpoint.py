from sqlalchemy import Column, Integer, String, DateTime
from .database import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    show_number = Column(Integer, nullable=False)
    air_date = Column(DateTime, nullable=False)
    round = Column(String(32), nullable=False)
    category = Column(String(64), nullable=False)
    value = Column(Integer, nullable=True)
    question = Column(String(256), nullable=False)
    answer = Column(String(64), nullable=False)
