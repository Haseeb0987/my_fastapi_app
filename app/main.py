from fastapi import FastAPI
from app.api.v1.routes import example, demo, test, face_recog
from app.db.init_db import create_tables
from app.db.base import engine
import asyncio
from app.api.v1.routes.auth import router as auth_router

app = FastAPI(title="Medium-Level FastAPI Boilerplate")

app.include_router(example.router, prefix="/api/v1/example")
app.include_router(demo.router, prefix="/api/v1/demo")
app.include_router(test.router, prefix="/api/v1/tests")
app.include_router(face_recog.router, prefix="/api/v1/faceRecognition")

# Auth Router

app.include_router(auth_router, prefix="/api/v1")


# Reload Check
@app.on_event("startup")
async def on_startup():
    await create_tables(engine)

@app.get("/")
async def root():
    return {"message": "FastAPI + SQL Server is running!"}