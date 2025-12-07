# app/api/v1/routes/example.py
from http.client import HTTPException
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_db
from app.models.example import Example
from app.schemas.example import ExampleCreate, ExampleRead
from app.common.api_response import APIResponse
import os
import json

router = APIRouter()
encoding_json = os.path.join(os.path.dirname(__file__), "../../../../encodings.json")

@router.post("/examples/", response_model=ExampleRead)
async def create_example(example_in: ExampleCreate, db: AsyncSession = Depends(get_db)):
    db_example = Example(**example_in.model_dump())
    db.add(db_example)
    await db.commit()
    await db.refresh(db_example)
    return APIResponse(success=True, data=db_example, message="Example created successfully").to_dict()

@router.get("/examples/{example_id}", response_model=ExampleRead)
async def get_example(example_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.get(Example, example_id)
    if not result:
        raise HTTPException(status_code=404, detail="Example not found")
    return APIResponse(success=True, data=result).to_dict()


@router.get("/echo")
def echo(message: str):
    print(f"Loading encodings from: {encoding_json}")
    with open(encoding_json, "r") as file:
        encodings_data = file.read()
    print(f"Encodings data: {encodings_data}")
    return APIResponse(success=True, data={"message": message}, message="Echo successful").to_dict()

@router.get("/encodings/{person_id}")
def get_encodings_by_id(person_id: str):

    with open(encoding_json, "r") as file:
        data = json.load(file)
        target_ecodings = data.get(person_id, {})
        print(f"Encodings for {person_id}: {target_ecodings}")

    return APIResponse(success=True, data=target_ecodings).to_dict()

@router.get("/encodings/class/{class_name}")
def get_encodings_by_class(class_name: str):
    with open(encoding_json, "r") as file:
        data = json.load(file)
        filtered_encodings = {
            pid: details for pid, details in data.items() if details.get("class") == class_name
        }
        print(f"Encodings for class {class_name}: {filtered_encodings}")
    return APIResponse(success=True, data=filtered_encodings).to_dict()
