from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from typing import Annotated
from sqlmodel import Session
from pathlib import Path

from app.routers.authentication_router import router as auth_router
from app.routers.category_router import router as category_router
from app.routers.item_router import router as item_router
from app.routers.user_router import router as user_router
# from app.databases.session import create_db_and_tables

app = FastAPI()

# Tidak dipakai lagi karena sudah menggunakan Alembic
# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()
    
app.include_router(auth_router, prefix="/api")
app.include_router(category_router, prefix="/api")
app.include_router(item_router, prefix="/api")
app.include_router(user_router, prefix="/api")

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "failed",
            "message": exc.detail
        }
    )
    