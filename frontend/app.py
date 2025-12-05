# frontend/app.py
import streamlit as st
import requests

API_ROOT_URL = "http://127.0.0.1:8000"

st.title("Démonstration d'API avec FastAPI et Streamlit")

st.subheader("Vérification de l'API")

# --- Le Bouton ---
if st.button("Ping l'API (Route /)"):
    try:
        # 1. Requête GET vers la route principale
        response = requests.get(API_ROOT_URL)

        # 2. Si il y a un résultat alors l'afficher
        if response.status_code == 200:
            st.success("Connexion réussie à l'API FastAPI !")
            st.code(f"Statut HTTP : {response.status_code}")

            st.json(response.json())
        else:
            st.error(f"L'API a répondu avec une erreur. Statut : {response.status_code}")

    except requests.exceptions.ConnectionError:
        st.error(f"ERREUR : Impossible de se connecter à l'API à {API_ROOT_URL}")
        st.warning("Veuillez vous assurer que le serveur Uvicorn est bien lancé en arrière-plan.")