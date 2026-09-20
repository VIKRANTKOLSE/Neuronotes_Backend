from psycopg_pool import AsyncConnectionPool
import os
from dotenv import load_dotenv
from urllib.parse import quote
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging

load_dotenv(Path(__file__).resolve().parents[2]/".env")

def required_env(name:str)->str:
    value=os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing {name} environment variable")
    return value

DB_HOST=required_env("DB_HOST")
DB_PORT=required_env("DB_PORT")
DB_USER=required_env("DB_USER")
DB_PASSWORD=quote(required_env("DB_PASSWORD"),safe="")
DB_NAME=required_env("DB_NAME")

DB_CONNECTION_STRING=f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

pool : AsyncConnectionPool | None

@asynccontextmanager
async def lifespan(app:FastAPI):
    global pool 
    logging.info("intialising postgreSQL asyncConnectionPool")
    pool=AsyncConnectionPool(
        conninfo=DB_CONNECTION_STRING,
        min_size=5,
        max_size=20,
        kwargs={"autocommit":False},
        open=False
    )
    await pool.open()
    app.state.pool=pool

    from services.CC_MIRT_input import build_q_matrix
    await build_q_matrix(app)

    yield
    logging.info("Closing PostgreSQL AsyncConnectionPool")
    await pool.close()

app=FastAPI(lifespan=lifespan)