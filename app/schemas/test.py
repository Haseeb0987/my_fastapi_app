# app/schemas/example.py
from pydantic import BaseModel
from datetime import datetime

class TestBase(BaseModel):
    title: str
    content: str | None = None

class TestCreate(TestBase):
    pass

class TestRead(TestBase):
    id: int
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True