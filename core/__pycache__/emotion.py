from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

tokenizer = AutoTokenizer.from_pretrained("nateraw/bert-base-uncased-emotion")
model = AutoModelForSequenceClassification.from_pretrained("nateraw/bert-base-uncased-emotion")

def detect_emotion(text):
    inputs = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        logits = model(**inputs).logits
        emotion = model.config.id2label[logits.argmax().item()]
    return emotion
