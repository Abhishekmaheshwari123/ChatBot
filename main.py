from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from textblob import TextBlob  # ✅ Added for spell correction

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# ✅ Emotion classification model
tokenizer = AutoTokenizer.from_pretrained("nateraw/bert-base-uncased-emotion")
model = AutoModelForSequenceClassification.from_pretrained("nateraw/bert-base-uncased-emotion")

# Dummy database for refund status
refund_status_db = {
    "TXN123": "Refunded",
    "TXN456": "Processing",
    "TXN789": "Failed"
}

# Budget tracking variables
user_budget = 0
user_expenses = []

# Request models
class RefundQuery(BaseModel):
    transaction_id: str

class ChatInput(BaseModel):
    message: str

@app.get("/")
def root():
    return FileResponse("static/index.html")



@app.post("/refund-status")
def check_refund_status(query: RefundQuery):
    status = refund_status_db.get(query.transaction_id.upper(), "Transaction ID not found")
    return {"transaction_id": query.transaction_id, "status": status}

@app.get("/money-tips")
def money_tips(user_type: Optional[str] = None):
    common_tips = [
        "Track your daily expenses using an app or a notebook.",
        "Cook at home instead of eating out.",
        "Avoid impulse purchases. Wait 24 hours before buying.",
        "Set up automatic savings transfers from your bank.",
        "Cancel unused subscriptions (Netflix, Spotify, etc.)."
    ]

    student_tips = [
        "Buy second-hand books or borrow from the library.",
        "Use student discounts when shopping or traveling.",
        "Limit takeout and use campus dining if cheaper."
    ]

    employee_tips = [
        "Bring lunch to work instead of eating out.",
        "Use public transport or carpool to save on fuel.",
        "Contribute to retirement savings if your employer matches."
    ]

    if user_type:
        user_type = user_type.lower()
        if user_type == "student":
            return {"user_type": "student", "tips": common_tips + student_tips}
        elif user_type == "employee":
            return {"user_type": "employee", "tips": common_tips + employee_tips}
        else:
            return {"user_type": user_type, "tips": common_tips}

    return {"tips": common_tips}

# Serve the static HTML UI
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/chat-ui")
def chat_ui():
    return FileResponse("static/index.html")

@app.post("/chat")
def chatbot(input: ChatInput):
    global user_budget, user_expenses

    # ✅ Spell correction
    corrected_msg = str(TextBlob(input.message)).lower()
    msg = corrected_msg

    # Refund status
    if "refund" in msg and "txn" in msg:
        txn_id = msg.split("txn")[-1].strip().upper()
        status = refund_status_db.get("TXN" + txn_id, "Transaction ID not found")
        return {"reply": f"The refund status for TXN{txn_id} is: {status}"}

    # More intelligent refund handling with fuzzy check
    elif any(word in msg for word in ["refud", "refoond", "reund", "reund", "refnd"]) and "txn" in msg:
        txn_id = msg.split("txn")[-1].strip().upper()
        status = refund_status_db.get("TXN" + txn_id, "Transaction ID not found")
        return {"reply": f"(Did you mean refund?) The refund status for TXN{txn_id} is: {status}"}

    # Money-saving tips
    elif "tip" in msg or "save" in msg:
        if "student" in msg:
            tips = money_tips("student")["tips"]
        elif "employee" in msg:
            tips = money_tips("employee")["tips"]
        else:
            tips = money_tips()["tips"]
        return {"reply": tips[0]}

    # Set budget
    elif "set my budget to" in msg:
        amount = int(''.join(filter(str.isdigit, msg)))
        user_budget = amount
        return {"reply": f"✅ Got it! Your monthly budget is set to ₹{amount}."}

    # Add expense
    elif "spent" in msg:
        amount = int(''.join(filter(str.isdigit, msg)))
        user_expenses.append(amount)
        total_spent = sum(user_expenses)
        remaining = user_budget - total_spent
        return {"reply": f"💸 Added ₹{amount} to your expenses. You've spent ₹{total_spent}. Remaining: ₹{remaining}."}

    # Check remaining budget
    elif "remaining budget" in msg or "how much left" in msg:
        total_spent = sum(user_expenses)
        remaining = user_budget - total_spent
        return {"reply": f"📊 You have ₹{remaining} left from your ₹{user_budget} budget."}

    # Expense tracking help
    elif "expense" in msg and ("track" in msg or "manage" in msg):
        return {"reply": "You can manage your expenses by categorizing them: rent, food, travel, and subscriptions. Want a template?"}

    # Budget planning help
    elif "budget" in msg and ("create" in msg or "plan" in msg):
        return {"reply": "To create a budget: 1. Track income 2. Categorize expenses 3. Set limits. Want me to walk you through it?"}

    # Intent classification fallback (emotion detection)
    inputs = tokenizer(input.message, return_tensors="pt")
    with torch.no_grad():
        logits = model(**inputs).logits
        predicted_class_id = logits.argmax().item()
        intent = model.config.id2label[predicted_class_id]

    return {
        "reply": f"I'm not sure how to help with that exactly, but it seems like you're asking about: **{intent}**. Want to try rephrasing or ask about refunds, tips, or budgets?"
    }
