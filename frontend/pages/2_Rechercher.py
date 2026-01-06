# frontend/pages/0_insérer.py
import streamlit as st
import requests 
import os 
import pandas as pd
from dotenv import load_dotenv 

load_dotenv()

API_ROOT_URL =  f"http://{os.getenv('API_BASE_URL')}:{os.getenv('FAST_API_PORT', '8080')}"



st.title("Lire une citation")

mode = st.radio("Choisissez le mode de recherche:",
         ("Aléatoire", "Par ID "))

if mode == "Aléatoire":
    st.subheader("Citation Aléatoire")
    # afficher une citation aléatoire
    API_URL =  API_ROOT_URL + "/read/random/"
    if st.button("obetnir une citation aléatoire:"):
        try : 
            response = requests.get(API_URL)

            if response.status_code == 200:
                result = response.json()

                if result:
                    st.success(f"Citation avec ID {result.get('id', 'N/A')}")
                    st.info(result.get('text', 'text non trouvé'))
                    st.balloons()
                else:
                    st.warning("Aucune citation disponible dans la DB")
            else:
                st.error(f"Erreur de l'API avec le code {response.status_code}")


        except requests.exceptions.ConnectionError:
            st.error(f"ERREUR : Impossible de se connecter à l'API à {API_URL}")
            st.warning("Veuillez vous assurer que le serveur Uvicorn est bien lancé en arrière-plan.")

else:
    # afficher une citation par ID
    st.subheader("Citation par ID")
    API_URL =  API_ROOT_URL + "/read/"
    # selectionne l'ID
    # un formulaire
    with st.form("search_by_id"):
        quote_id = st.number_input("Entrez l'ID de la citation:", 
                                   min_value=1, step=1)
        submitted = st.form_submit_button("Rechercher")
    # connaitre toutes les id
    # selectionne l'id
    if submitted:
        # appel la route /read/id
        try : 
            response = requests.get( API_URL + str(quote_id) )
        # le reste est pareil
            if response.status_code == 200:
                result = response.json()

                if result:
                    st.success(f"Citation avec ID {quote_id}")
                    st.info(result.get('text', 'text non trouvé'))
                    st.balloons()
                    #analyser la citation obtenue avec l'api d'analyse de sentiment
                    analyse_submit = st.form_submit_button("Analyser la citation")
                    if analyse_submit :
                        try :
                            response = requests.post("http://127.0.0.1:9000/analyse_sentiment/", json={"texte": result.get('text')})
                            sentiment = response.json()
                            st.write("Résultats de l'analyse :")
                            st.write(f"Polarité négative : {sentiment['neg']}")
                            st.write(f"Polarité neutre : {sentiment['neu']}")
                            st.write(f"Polarité positive : {sentiment['pos']}")
                            st.write(f"Score composé : {sentiment['compound']}")
                        except :
                            st.error(f"ERREUR : Impossible de se connecter à l'API SENTIMENT")
                            
                else:
                    st.warning(f"La citation {quote_id} n'est pas disponible dans la DB")
            else:
                st.error(f"Erreur de l'API avec le code {response.status_code}")


        except requests.exceptions.ConnectionError:
            st.error(f"ERREUR : Impossible de se connecter à l'API à {API_URL}")
            st.warning("Veuillez vous assurer que le serveur Uvicorn est bien lancé en arrière-plan.")





