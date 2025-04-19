from fastapi import APIRouter
from typing import Optional

router = APIRouter()

@router.get("/money-tips")
def tips(user_type: Optional[str] = None):
    common = [
        "Track expenses", "Avoid impulse buys", "Cook at home"
    ]
    student = ["Buy used books", "Use student discounts"]
    employee = ["Bring lunch", "Carpool"]

    if user_type:
        if user_type.lower() == "student":
            return {"tips": common + student}
        elif user_type.lower() == "employee":
            return {"tips": common + employee}
    return {"tips": common}
