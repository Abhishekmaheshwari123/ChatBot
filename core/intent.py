from sentence_transformers import SentenceTransformer, util

embedder = SentenceTransformer("all-MiniLM-L6-v2")

intents = {
    "set_budget": ["set my budget to 2000", "my budget is 5000", "i have 10000 as budget"],
    "add_expense": ["i spent 300 on food", "spent 100", "add 500 expense", "i spet 300 on travel"],
    "remaining_budget": ["how much money left", "remaining budget", "how much left in my budget"],
    "check_refund": ["check refund for txn123", "refund status of txn456", "what about txn789 refund"],
    "money_tips": ["give me financial tips", "i'm a student", "how to save money", "suggest money tips"],
    "track_expense": ["how to track spending", "track expense guide"],
    "budget_help": ["help plan budget", "guide for budgeting"],
    "investment_suggestions": ["can i invest", "where to invest", "how to grow money"],
    "greet": ["hi", "hello", "hey there"],
    "goodbye": ["bye", "goodbye", "see you later"]
}

def get_intent(user_msg: str):
    user_embedding = embedder.encode(user_msg, convert_to_tensor=True)
    best_intent = None
    best_score = 0.0

    for intent, examples in intents.items():
        for ex in examples:
            ex_embedding = embedder.encode(ex, convert_to_tensor=True)
            score = util.pytorch_cos_sim(user_embedding, ex_embedding).item()
            if score > best_score:
                best_score = score
                best_intent = intent

    if best_score > 0.6:
        return best_intent
    return None
