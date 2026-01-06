# backend/modules/df_tools.py
from loguru import logger 
import pandas as pd
import os 

CSV_FILE_PATH = os.path.join("backend","data", "quotes_db.csv")

def write_db(df: pd.DataFrame):
    df.to_csv(CSV_FILE_PATH, index=True, index_label='id')

def read_db()->pd.DataFrame:
    df = pd.read_csv(CSV_FILE_PATH, index_col='id')
    df.text = df.text.fillna("Vide")
    return df

def initialize_db():
    if os.path.exists(CSV_FILE_PATH):
        logger.info("La base de données existe")
    else:
        logger.info(f"impossible de trouver le fichier {CSV_FILE_PATH}")
        df = pd.DataFrame(columns=['id', 'text'])
        df = df.set_index('id')
        write_db(df)
        logger.info(f"le fichier {CSV_FILE_PATH} a été créé")