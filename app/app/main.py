from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .models import Question
import random
from openai import OpenAI


client = OpenAI()
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

@app.post("/verify-answer/")
def verify_answer(question_id: int, answer: str, db: Session = Depends(get_db)):
    """
    Verify if the given answer is correct for the question_id using OpenAI.
    """
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    prompt = f"""
    You are a trivia answer checker. Compare the user's answer to the correct answer.

    Question: {question.question}
    Correct Answer: {question.answer}
    User's Answer: {answer}

    Return whether the user's answer is correct or incorrect.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        result_text = response.choices[0].message.content

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")

    return {
        "question_id": question_id,
        "verification": result_text
    }

