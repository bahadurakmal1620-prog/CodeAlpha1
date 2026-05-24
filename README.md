# PyBot — FAQ Chatbot (CodeAlpha Internship · Task 2)

A Python-powered FAQ chatbot using NLP techniques (tokenization, stop word
removal, stemming, TF-IDF, and cosine similarity) to match user questions
with the most relevant FAQ entry.

## Features
- 20 Python Programming FAQs preloaded
- Custom NLP pipeline (no heavy dependencies)
- TF-IDF + Cosine Similarity for intent matching
- Confidence score shown for every answer
- Clean dark-themed chat UI (browser-based)

## Requirements
- Python 3.7 or higher
- No third-party packages required (uses stdlib only)

## How to Run

1. Make sure both files are in the same folder:
   - app.py
   - index.html

2. Open a terminal in that folder and run:
   python app.py

3. Open your browser and visit:
   http://localhost:5000

## NLP Pipeline (in app.py)

User Input
   │
   ▼
Tokenize (split into words, lowercase, remove punctuation)
   │
   ▼
Remove Stop Words (common words like "the", "is", "a"...)
   │
   ▼
Stem (reduce words to base form: "running" → "run")
   │
   ▼
TF-IDF Vectorize (weight words by importance)
   │
   ▼
Cosine Similarity (compare with all FAQ vectors)
   │
   ▼
Return Best Match + Confidence Score

## File Structure

faq_chatbot/
├── app.py        ← Python backend (NLP engine + HTTP server)
├── index.html    ← Chat UI (HTML/CSS/JS)
└── README.md     ← This file
