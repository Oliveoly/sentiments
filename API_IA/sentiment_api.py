from fastapi import FastAPI, HTTPException
import uvicorn
import os 
import pandas as pd
from dotenv import load_dotenv 
from pydantic import BaseModel
from typing import List
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')
load_dotenv()
app = FastAPI(title="API_SENTIMENT")

class Texte(BaseModel):
    texte: str


@app.get("/")
def read_root():
    return {"Hello": "World", "status": "API is running"}

#analyser une citation
@app.post("/analyse_sentiment/")
def analyse(quote : Texte):
    sia = SentimentIntensityAnalyzer()
    sentiment = sia.polarity_scores(quote.texte)
    #logger.info(f"Résultats: {sentiment}")
    return {
            "neg": sentiment["neg"],
            "neu": sentiment["neu"],
            "pos": sentiment["pos"],
            "compound": sentiment["compound"],
        }

