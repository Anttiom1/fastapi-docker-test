import contextlib
from fastapi import Depends, FastAPI, HTTPException
import os
import mysql
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi import FastAPI
from sqlalchemy.exc import SQLAlchemyError
import mysql.connector


DB_USER = os.getenv("MYSQL_USER")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
DB_HOST = os.getenv("MYSQL_DATABASE_HOST")
DB = os.getenv("MYSQL_DATABASE")

app = FastAPI()

print(DB_USER)

@app.get("/")
def read_roots():
    return {"message": "Hello, FastAPI!!!!!!!!!!"}


@app.get("/checkconnection")
async def check_db():
    try:
        # Establish connection to the MySQL database
        with mysql.connector.connect(host="DB_HOST", user="DB_USER", database="DB", password="DB_PASSWORD") as con:
            with con.cursor() as cur:
                # Execute a simple query to check the connection
                cur.execute("SELECT 1")
                result = cur.fetchone()  # Fetch the result of the query (just checking if we can fetch something)
                if result:
                    return {"message": "Database connection is successful!"}
                else:
                    raise HTTPException(status_code=500, detail="Database returned no result.")
    except mysql.connector.Error as err:
        # Handle any errors that occur during the connection
        raise HTTPException(status_code=500, detail=f"Database connection failed: {err}")


