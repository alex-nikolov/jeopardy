from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from . import models

#models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Jeopardy Questions API")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "FastAPI with PostgreSQL, SQLAlchemy, Alembic & OpenAI ready!"}
