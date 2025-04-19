from pydantic import BaseModel

class ChatInput(BaseModel):
    message: str
    user_id: str

class RefundQuery(BaseModel):
    transaction_id: str
