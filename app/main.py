from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from typing import Annotated
from sqlmodel import Session
from pathlib import Path

from app.routers.authentication_router import router as auth_router
from app.routers.category_router import router as category_router
from app.databases.session import create_db_and_tables

app = FastAPI()

# Tidak dipakai lagi karena sudah menggunakan Alembic
# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()
    
app.include_router(auth_router, prefix="/api")
app.include_router(category_router, prefix="/api")