from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
import pandas as pd
import html

df = pd.read_csv('jeopardy_sanitized.csv')

# Connect to Postgres
#engine = create_engine("postgresql://postgres:password@localhost/Jeopardy")
engine = create_engine("postgresql://postgres:postgres@db:5432/Jeopardy")
metadata = MetaData()

# Define table
questions_table = Table(
    "questions", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("show_number", Integer),
    Column("air_date", String),
    Column("round", String),
    Column("category", String),
    Column("value", String),
    Column("question", String),
    Column("answer", String)
)

# Insert DataFrame into table
with engine.connect() as conn:
    for _, row in df.iterrows():
        insert_stmt = questions_table.insert().values(
            show_number=row["Show Number"],
            air_date=row["Air Date"],
            round=row["Round"],
            category=row["Category"],
            value=int(row["Value"]),
            question=row["Question"],
            answer=row["Answer"]
        )
        conn.execute(insert_stmt)
    conn.commit()
