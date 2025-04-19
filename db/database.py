from tinydb import TinyDB, Query
from tinydb.operations import set as tinydb_set

# Initialize database and query object
db = TinyDB("users.json")
User = Query()

def get_user_data(user_id: str) -> dict:
    """
    Retrieve user data. If not found, initialize with default structure.
    """
    user = db.get(User.user_id == user_id)
    if not user:
        default_data = {
            "user_id": user_id,
            "budget": 0,
            "expenses": [],
            "history": []
        }
        db.insert(default_data)
        return default_data
    return user

def update_user_data(user_id: str, key: str, value):
    """
    Update a specific key in the user's data.
    """
    db.update(tinydb_set(key, value), User.user_id == user_id)

def append_expense(user_id: str, amount: float):
    """
    Safely append an expense to the user's expense list.
    """
    if not isinstance(amount, (int, float)):
        raise ValueError("Amount must be a number.")

    def update_expenses(user):
        user["expenses"].append(amount)
        return user

    db.update(update_expenses, User.user_id == user_id)

def add_chat_history(user_id: str, msg: str, reply: str):
    """
    Safely append a chat entry to the user's history.
    """
    if not isinstance(msg, str) or not isinstance(reply, str):
        raise ValueError("Chat message and reply must be strings.")

    def update_history(user):
        user["history"].append({"msg": msg, "reply": reply})
        return user

    db.update(update_history, User.user_id == user_id)
