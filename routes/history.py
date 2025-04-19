from fastapi import APIRouter
from db.database import get_user_data

router = APIRouter()

@router.get("/history")
def get_history(user_id: str):
    user = get_user_data(user_id)
    return {"history": user["history"]}
