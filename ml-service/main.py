from fastapi import FastAPI
from api.predict import router
from config.database import app


app.include_router(router)

