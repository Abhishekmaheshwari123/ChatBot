from textblob import TextBlob

def spell_correct(text: str) -> str:
    return str(TextBlob(text))
