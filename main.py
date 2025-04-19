# main.py

import spacy
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from transformers import pipeline

# Load spaCy model for NER (Named Entity Recognition) and tokenization
nlp = spacy.load("en_core_web_sm")

# Load the transformer model for intent classification (zero-shot classification)
intent_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Initialize FastAPI app
app = FastAPI()

# Function to extract entities using spaCy
def extract_entities(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

# Function to classify intent using HuggingFace Transformers (BART model)
def classify_intent(text):
    labels = ["refund", "budget", "savings", "general inquiry"]
    result = intent_classifier(text, candidate_labels=labels)
    return result['labels'][0], result['scores'][0]  # Top label and confidence score

@app.post("/process_message/")
async def process_message(text: str):
    # Step 1: Extract entities using spaCy
    entities = extract_entities(text)
    
    # Step 2: Classify the intent using the Transformer model
    intent, confidence = classify_intent(text)

    # Example response based on the classified intent
    response = {
        "entities": entities,
        "intent": intent,
        "confidence": confidence,
        "message": f"Intent detected as: {intent} with confidence {confidence:.2f}"
    }
    
    return JSONResponse(content=response)
