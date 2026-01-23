from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from typing import Annotated
from sqlmodel import Session
from pathlib import Path

from app.routers.authentication_router import router as auth_router
from app.databases.session import get_session, create_db_and_tables

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    
app.include_router(auth_router, prefix="/api")