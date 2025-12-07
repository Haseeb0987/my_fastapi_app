# app/services/test_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.example import Test
from app.schemas.test import TestCreate, TestRead

class TestService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_test(self, test_data: TestCreate) -> TestRead:
        """Create a new test record"""
        db_test = Test(
            title=test_data.title,
            content=test_data.content
        )
        self.db.add(db_test)
        await self.db.commit()
        await self.db.refresh(db_test)
        return TestRead.model_validate(db_test)

    async def get_test_by_id(self, test_id: int) -> TestRead | None:
        """Get a test record by ID"""
        stmt = select(Test).where(Test.id == test_id)
        result = await self.db.execute(stmt)
        test = result.scalars().first()
        
        if not test:
            return None
        return TestRead.model_validate(test)

    async def get_all_tests(self, skip: int = 0, limit: int = 100) -> list[TestRead]:
        """Get all test records with pagination"""
        stmt = select(Test).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        tests = result.scalars().all()
        return [TestRead.model_validate(test) for test in tests]

    async def update_test(self, test_id: int, test_data: TestCreate) -> TestRead | None:
        """Update a test record"""
        stmt = select(Test).where(Test.id == test_id)
        result = await self.db.execute(stmt)
        db_test = result.scalars().first()
        
        if not db_test:
            return None
        
        db_test.title = test_data.title
        db_test.content = test_data.content
        
        await self.db.commit()
        await self.db.refresh(db_test)
        return TestRead.model_validate(db_test)

    async def delete_test(self, test_id: int) -> bool:
        """Delete a test record"""
        stmt = select(Test).where(Test.id == test_id)
        result = await self.db.execute(stmt)
        db_test = result.scalars().first()
        
        if not db_test:
            return False
        
        await self.db.delete(db_test)
        await self.db.commit()
        return True