import datetime
from fastapi import APIRouter

router = APIRouter()

@router.get("/demo")
def demo(message: str):
    return {
        "time": datetime.datetime.now().isoformat(),
        "demo": message
    }