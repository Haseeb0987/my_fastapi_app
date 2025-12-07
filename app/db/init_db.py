# app/db/init_db.py
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import text
from app.db.base import Base
from app.models import *  # import all models here later

async def create_tables(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def test_connection(engine: AsyncEngine):
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        print("Database connection successful!")
    except Exception as e:
        print("Database connection failed:", e)