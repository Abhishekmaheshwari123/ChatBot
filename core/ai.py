from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

tokenizer = AutoTokenizer.from_pretrained("nateraw/bert-base-uncased-emotion")
model = AutoModelForSequenceClassification.from_pretrained("nateraw/bert-base-uncased-emotion")

def emotion_classifier(msg: str) -> str:
    inputs = tokenizer(msg, return_tensors="pt")
    with torch.no_grad():
        logits = model(**inputs).logits
    label_id = logits.argmax().item()
    emotion = model.config.id2label[label_id]
    return f"I'm not sure how to help, but it sounds like you're feeling **{emotion}**."
