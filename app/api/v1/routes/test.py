# app/api/v1/routes/test.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_db
from app.services.test_service import TestService
from app.schemas.test import TestCreate, TestRead
from app.common.api_response import APIResponse

router = APIRouter()

@router.post("/create", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_test(test_data: TestCreate, db: AsyncSession = Depends(get_db)):
    """Create a new test record"""
    try:
        service = TestService(db)
        test = await service.create_test(test_data)
        response = APIResponse(
            success=True,
            data=test.model_dump(),
            message="Test created successfully",
            status_code=status.HTTP_201_CREATED
        )
        return response.to_dict()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{test_id}", response_model=dict)
async def get_test(test_id: int, db: AsyncSession = Depends(get_db)):
    """Get a test record by ID"""
    service = TestService(db)
    test = await service.get_test_by_id(test_id)
    
    if not test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test not found"
        )
    
    response = APIResponse(
        success=True,
        data=test.model_dump(),
        message="Test retrieved successfully"
    )
    return response.to_dict()

@router.get("/", response_model=dict)
async def get_all_tests(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """Get all test records with pagination"""
    service = TestService(db)
    tests = await service.get_all_tests(skip=skip, limit=limit)
    
    response = APIResponse(
        success=True,
        data=[test.model_dump() for test in tests],
        message=f"Retrieved {len(tests)} tests"
    )
    return response.to_dict()

@router.put("/{test_id}", response_model=dict)
async def update_test(test_id: int, test_data: TestCreate, db: AsyncSession = Depends(get_db)):
    """Update a test record"""
    service = TestService(db)
    test = await service.update_test(test_id, test_data)
    
    if not test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test not found"
        )
    
    response = APIResponse(
        success=True,
        data=test.model_dump(),
        message="Test updated successfully"
    )
    return response.to_dict()

@router.delete("/{test_id}", response_model=dict)
async def delete_test(test_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a test record"""
    service = TestService(db)
    success = await service.delete_test(test_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test not found"
        )
    
    response = APIResponse(
        success=True,
        data=None,
        message="Test deleted successfully"
    )
    return response.to_dict()