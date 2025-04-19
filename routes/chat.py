from fastapi import APIRouter
from pydantic import BaseModel
from textblob import TextBlob

from core.intent import get_intent
from core.emotion import detect_emotion  # <- Emotion detector
from db.database import (
    get_user_data,
    update_user_data,
    append_expense,
    add_chat_history
)

router = APIRouter()


class ChatInput(BaseModel):
    message: str
    user_id: str


# Dummy refund status database
refund_status_db = {
    "TXN123": "Refunded",
    "TXN456": "Processing",
    "TXN789": "Failed"
}


@router.post("/chat")
def chat(input: ChatInput):
    user_id = input.user_id
    msg = str(TextBlob(input.message)).lower()

    # Step 1: Detect intent
    intent = get_intent(msg)

    # Step 2: Fallback heuristics
    if not intent:
        if "student" in msg and "tip" in msg:
            intent = "money_tips"
        elif "budget" in msg:
            intent = "budget_help"
        elif "expense" in msg or "spend" in msg:
            intent = "track_expense"

    # Step 3: Fetch user data
    user = get_user_data(user_id)

    # Step 4: Response logic
    if intent == "check_refund":
        txn_id = msg.split("txn")[-1].strip().upper()
        status = refund_status_db.get("TXN" + txn_id, "Transaction ID not found")
        reply = f"🔄 The refund status for TXN{txn_id} is: {status}"

    elif intent == "set_budget":
        amount = int(''.join(filter(str.isdigit, msg)))
        update_user_data(user_id, "budget", amount)
        reply = f"✅ Budget set to ₹{amount}."

    elif intent == "add_expense":
        amount = int(''.join(filter(str.isdigit, msg)))
        append_expense(user_id, amount)
        user = get_user_data(user_id)  # Refresh after update
        total = sum(user["expenses"])
        remaining = user["budget"] - total
        reply = f"💸 Added ₹{amount}. Total spent: ₹{total}. Remaining: ₹{remaining}."

    elif intent == "remaining_budget":
        total = sum(user["expenses"])
        remaining = user["budget"] - total
        reply = f"📊 You have ₹{remaining} left from ₹{user['budget']} budget."

    elif intent == "money_tips":
        reply = "💡 Tip: Track your daily expenses and avoid impulse buys."

    elif intent == "investment_suggestions":
        reply = "📈 Consider SIPs, FDs, or PPF. Want advice based on your risk level?"

    elif intent == "track_expense":
        reply = "📘 Categorize your expenses: rent, food, transport, etc."

    elif intent == "budget_help":
        reply = "📝 Steps: Track income > Categorize expenses > Set spending limits."

    elif intent == "greet":
        reply = "👋 Hey there! I'm FinMate, your finance buddy. Ask me anything."

    elif intent == "goodbye":
        reply = "👋 Goodbye! Stay smart with your money!"

    else:
        # Emotion fallback
        emotion = detect_emotion(input.message)
        reply = f"I'm not sure how to help, but it sounds like you're feeling **{emotion}**."

    # Step 5: Save to chat history
    add_chat_history(user_id, msg, reply)

    # Step 6: Return response
    return {"reply": reply}
