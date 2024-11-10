from fastapi import Depends, FastAPI, HTTPException
import os
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi import FastAPI
from databases import Database

DB_USER = os.getenv("MYSQL_USER")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
DB_HOST = os.getenv("MYSQL_DATABASE")
DB_NAME = os.getenv("MYSQL_DATABASE_NAME")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


database = Database(DATABASE_URL)

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!!!!!!!!!!"}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/healthcheck")
async def health_check():
    try:
        # Attempt a simple connection without querying any tables
        async with database.connection() as conn:
            await conn.execute(text("SELECT 1"))
        return {"status": "Database connected successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database connection failed") from e