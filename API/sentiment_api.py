from fastapi import FastAPI, HTTPException
import uvicorn
import os 
import pandas as pd
from dotenv import load_dotenv 
from pydantic import BaseModels
from typing import List
from nltk.sentiment import SentimentIntensityAnalyzer

load_dotenv()
app = FastAPI(title="API_SENTIMENT")

#analyser une citation
@app.post("/analyse_sentiment/")
def analyse(quote):
    sia = SentimentIntensityAnalyzer()
    sentiment = sia.polarity_scores(quote)
    return sentiment

