# backend/main.py
from fastapi import FastAPI

# def timer_decorator(function):
#     def wrapper(*args, **kwargs):
#         start = time.perf_counter()
#         result = function(*args, **kwargs)
#         end = time.perf_counter()
#         print(f"La fonction {function.__name__} a été exécutée en : {end - start: .5f} secondes")
#         return result
#     return wrapper

# --- Configuration ---
app = FastAPI(title="API")

# --- Routes API ---
# http://www.google.com/fr route fr
# http://www.google.com/en route en 
# http://www.google.com/ route principale

@app.get("/")
def read_root():
    return {"Hello": "World", "status": "API is running"}

@app.get("/citation")
def read_citation():
    return {"auteur": "Cyril", "citation": "Caractéristique qui, pour tout ensemble, fini ou infini, permet de définir une notion équivalente au nombre d'éléments à travers la mise en place d'une bijection entre ensembles."}

@app.get("/fr")
def read_root_fr():
    return {"Bonjour": "Monde", "status": "API est ok"}
