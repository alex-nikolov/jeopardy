from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .models import Question
import random


app = FastAPI(title="Jeopardy Questions API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "FastAPI with PostgreSQL, SQLAlchemy, Alembic & OpenAI ready!"}


@app.get("/question/")
def get_random_question(round: str = Query(...), value: int = Query(...), db: Session = Depends(get_db)):
    """
    Returns a random question based on the provided round and value.
    """
    questions = db.query(Question).filter(Question.round == round, Question.value == value).all()
    if not questions:
        raise HTTPException(status_code=404, detail="No questions found for the given round and value")
    
    question = random.choice(questions)
    
    return {
        "question_id": question.id,
        "round": question.round,
        "category": question.category,
        "value": question.value,
        "question": question.question
    }