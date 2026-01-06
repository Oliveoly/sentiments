# backend/modules/df_tools.py
import os 
from loguru import logger 
import pandas as pd
from sqlalchemy.orm import Session, DeclarativeBase, mapped_column
from sqlalchemy import String, create_engine

engine = create_engine(DB_URL)
session = Session(engine)

class Quote(DeclarativeBase):
    __tablename__ = "quote"
    quote_id = mapped_column(primary_key=True, nullable= False)
    quote = mapped_column(String)




#adapter ce code à sqlalchemy plutot que dataframe pandas
CSV_FILE_PATH = os.path.join("backend","data", "quotes_db.csv")
DB_FILE = os.path.join("backend","data","quotes_db.db")
DB_URL = f"sqlite:///{DB_FILE}"

def write_db(df: pd.DataFrame):
    quote = Quote()
    session.add(quote)
    #df.to_csv(CSV_FILE_PATH, index=True, index_label='id')

def read_db()->pd.DataFrame:
    df = pd.read_csv(CSV_FILE_PATH, index_col='id')
    df.text = df.text.fillna("Vide")
    return df

def initialize_db():
    engine = create_engine(DB_URL)
    session = Session(engine)