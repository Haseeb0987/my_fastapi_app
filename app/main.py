from fastapi import FastAPI
from app.api.v1.routes import example, demo
from app.db.init_db import create_tables
from app.db.base import engine
import asyncio

app = FastAPI(title="Medium-Level FastAPI Boilerplate")

app.include_router(example.router, prefix="/api/v1/example")
app.include_router(demo.router, prefix="/api/v1/demo")


# Reload Check
@app.on_event("startup")
async def on_startup():
    await create_tables(engine)

@app.get("/")
async def root():
    return {"message": "FastAPI + SQL Server is running!"}