# FinMate ChatBot 🤖

An intelligent, emotion-aware chatbot built with FastAPI and integrated NLP/ML features.

## 🚀 Features
- Emotion detection
- Intent classification
- Real-time chat API
- Refund & money inquiry routes
- Modular backend structure (routes, core logic, DB)

## 🛠 Tech Stack
- Python 3.13
- FastAPI
- Machine Learning (custom models)
- JSON-based data handling

## 📁 Project Structure

This is a simple chatbot that uses FastAPI and a locally hosted AI model (MiniLM) to answer user queries and provide finance tips.
ChatBot/
├── core/
│   ├── __init__.py
│   ├── ai.py
│   ├── emotion.py
│   ├── intent.py
│   ├── models.py
│   └── utils.py
│
├── db/
│   ├── __init__.py
│   └── database.py
│
├── routes/
│   ├── __init__.py
│   ├── chat.py
│   ├── history.py
│   ├── money.py
│   └── refund.py
│
├── users.json
├── Dockerfile
├── main.py          # (Assumed entry point — let me know if it’s named differently)
└── README.md        # (You can add the one I suggested earlier)


## How to Run
✅ Steps to Run This ChatBot Application Locally
1. Clone the Repository
Open terminal / PowerShell / Command Prompt:

bash
Copy
Edit
git clone https://github.com/Abhishekmaheshwari123/ChatBot.git
cd ChatBot

2. Set Up a Virtual Environment (Recommended)
bash
Copy
Edit
# For Windows:
python -m venv venv
venv\Scripts\activate

# For Mac/Linux:
python3 -m venv venv
source venv/bin/activate

3. Install the Required Dependencies
bash
Copy
Edit
pip install -r requirements.txt
Make sure the requirements.txt file includes all necessary packages like:

txt
Copy
Edit
fastapi
uvicorn
numpy
scikit-learn
transformers
torch
# any other libraries you're using


4. Run the Application
bash
Copy
Edit
uvicorn main:app --reload
main:app means you're telling uvicorn to look for the FastAPI app inside main.py.


5. Visit in Browser
Once running, open your browser and go to:

cpp
Copy
Edit
http://127.0.0.1:8000
You’ll see your application running!
