# app/schemas/example.py
from pydantic import BaseModel
from datetime import datetime

class ExampleBase(BaseModel):
    name: str
    description: str | None = None

class ExampleCreate(ExampleBase):
    pass

class ExampleRead(ExampleBase):
    id: int
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True