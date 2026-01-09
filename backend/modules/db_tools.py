# backend/modules/db_tools.py

import os
from loguru import logger
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Union
import pandas as pd 
from pathlib import Path

# Définition du type accepté pour write_db
DataStorage = Union[pd.DataFrame, List[dict]]

# --- 1. Configuration des Chemins ---

# Chemin relatif de la BDD (comme spécifié par l'utilisateur)
DB_FILE_PATH_RELATIVE = os.path.join("backend", "data", "quotes_db.sqlite")

# Détermination du répertoire racine du projet pour obtenir un chemin absolu fiable
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent.parent # Remonte de modules -> backend -> racine

# Chemin Absolu vers la BDD
DB_FILE_PATH = PROJECT_ROOT / DB_FILE_PATH_RELATIVE
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_FILE_PATH.absolute()}" 

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- 2. Modèle de Données (ORM) : La Classe Citation ---

class QuoteModel(Base):
    """
    Modèle ORM représentant la table 'quotes'.
    """
    __tablename__ = "quotes"
    
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)

# --- 3. Fonctions d'Interface (Le Contrat) ---

def get_db_session() -> Session:
    """Fournit une session de BDD."""
    return SessionLocal()

def write_db(data: DataStorage):
    """
    Écrit les données en base de données, gérant les entrées de type DataFrame ou List[dict].
    """
    quotes_to_insert = []

    # --- SWITCH LOGIC: Conversion de la donnée entrante en List[dict] ---
    if isinstance(data, pd.DataFrame):
        # Cas Pandas: Conversion du DataFrame en liste de dictionnaires
        logger.info("Conversion de l'entrée: DataFrame -> List[dict].")
        quotes_to_insert = data.to_dict('records') 
    
    elif isinstance(data, list):
        # Cas SQLAlchemy/List: Utiliser la liste telle quelle
        logger.info("Entrée traitée comme List[dict].")
        quotes_to_insert = data
        
    else:
        logger.error(f"Type de donnée non supporté pour write_db: {type(data)}")
        raise TypeError("write_db n'accepte que pd.DataFrame ou List[dict].")

    # --- Logique d'Insertion SQLAlchemy (Commune) ---
    db = get_db_session()
    try:
        for quote_data in quotes_to_insert:
            # Récupère la valeur du texte (méthode .get fonctionne maintenant)
            text_value = quote_data.get('text', '').strip()
            
            if not text_value:
                 text_value = "NULL_TEXT_EMPTY"
                 logger.warning(f"Tentative d'écriture de texte vide, corrigé en '{text_value}'.")
            
            new_quote = QuoteModel(text=text_value)
            db.add(new_quote)
            
        db.commit()
        logger.success(f"Écriture de {len(quotes_to_insert)} citation(s) dans la BDD réussie.")
        
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Erreur d'écriture dans la BDD: {e}")
    finally:
        db.close()

def read_db() -> pd.DataFrame:
    """
    Lit toutes les citations depuis la BDD et les renvoie sous forme de DataFrame.
    Gère le cas de BDD vide (KeyError) pour respecter le contrat Pandas.
    """
    db = get_db_session()
    try:
        quotes = db.query(QuoteModel).all()
        
        data = []
        for quote in quotes:
            text = quote.text.strip()
            
            # Nettoyage à la lecture
            if not text or text == "NULL_TEXT_EMPTY":
                cleaned_text = "NULL_TEXT_EMPTY"
            else:
                cleaned_text = text
                
            data.append({'id': quote.id, 'text': cleaned_text})

        # Correction de la KeyError: renvoie un DF vide avec les colonnes attendues si 'data' est vide
        if not data:
             return pd.DataFrame(columns=['id', 'text']).set_index('id')
             
        return pd.DataFrame(data).set_index('id')
        
    except SQLAlchemyError as e:
        logger.error(f"Erreur de lecture dans la BDD: {e}")
        return pd.DataFrame(columns=['id', 'text']).set_index('id')
    finally:
        db.close()

def get_all_quotes() -> List[dict]:
    """Récupère toutes les citations sous forme de liste de dictionnaires (plus naturel pour l'API)."""
    db = get_db_session()
    try:
        quotes = db.query(QuoteModel).all()
        return [{'id': q.id, 'text': q.text} for q in quotes]
    except SQLAlchemyError as e:
        logger.error(f"Erreur de lecture dans la BDD: {e}")
        return []
    finally:
        db.close()


def initialize_db():
    """
    Crée le dossier 'data', la base de données et les tables si elles n'existent pas.
    """
    # 1. Crée le dossier 'data' s'il n'existe pas
    data_dir = DB_FILE_PATH.parent
    if not os.path.exists(data_dir):
        os.makedirs(data_dir, exist_ok=True)
        logger.info(f"Dossier '{data_dir}' créé.")

    # 2. Crée les tables
    if os.path.exists(DB_FILE_PATH):
        logger.info("La base de données SQLite existe.")
    else:
        logger.info(f"Création de la base de données SQLite à {DB_FILE_PATH}.")

    Base.metadata.create_all(bind=engine)
    logger.info("Les tables de la BDD ont été vérifiées/créées.")