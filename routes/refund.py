from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

refund_status_db = {
    "TXN123": "Refunded",
    "TXN456": "Processing",
    "TXN789": "Failed"
}

class RefundQuery(BaseModel):
    transaction_id: str

@router.post("/refund-status")
def check_refund(query: RefundQuery):
    status = refund_status_db.get(query.transaction_id.upper(), "Transaction ID not found")
    return {"transaction_id": query.transaction_id, "status": status}
