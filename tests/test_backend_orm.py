import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import pandas as pd

from backend.modules.db_tools import write_db,read_db, Base, QuoteModel
#-----------
# FIXTURE -> on crée une db pour nos tests que l'on passe en parametres, il nous faut un décorateur
#-----------
##create engine

@pytest.fixture(scope="module")
def engine_test():
    """Create Engine"""
    return create_engine("sqlite:///:memory:")

##create db

@pytest.fixture(scope="module")
def setup_db(engine_test):
    """create table"""
    Base.metadata.create_all(engine_test)
    yield
    Base.metadata.drop_all(engine_test)

#create db session 
@pytest.fixture(scope="function")
def db_session(engine_test, setup_db):
    """yield db session"""
    connection = engine_test.connect()
    transaction = connection.begin()

    SessionTest = sessionmaker(autocommit = False, autoflush=False,bind=engine_test)
    #ouverture de la session
    session = SessionTest(bind = connection)
    yield session
    #nettoyage
    session.close()
    transaction.rollback()
    connection.close()

#----------
# MOCK -> on ouvre une session fictive pour eviter de toucher la principele
# --------
## override session local
@pytest.fixture(autouse=True)
def override_get_db_session(monkeypatch, db_session, ):
    """mock get db session"""
    def mock_get_db_session() :
        return db_session
    monkeypatch.setattr('backend.modules.db_tools.get_db_session', mock_get_db_session)


#--------
#test
#--------
def test_add_and_read_quote():
    quote = "test"
    dico = {"text" : [quote]}
    df = pd.DataFrame(dico)
    #ajouter citation
    write_db(df)
    #lire citation
    df2 = read_db()
    citation = df2.iloc[0]["text"]
    assert not df2.empty
    assert citation == quote