#### Installation des bibliothèques
`pip install fastapi uvicorn loguru streamlit requests python-dotenv`

Un mini programme complet:
* **frontend** (streamlit)
  * **pages**
* **backend**:
  * **modules** (contenir nos propres modules)
  * **data** (nos csv)

#### Architecture
```
mon_projet/
├── API
│   └── sentiment_api.py
├── APP
│   └── sentiment_streamlit.py
├── backend
│   ├── modules
│   │   └── df_tools.py
│   ├── data
│   │   └── quotes_db.csv
│   └── main.py
├── frontend
│   ├── app.py
│   └── pages
│       ├── 0_insérer.py
│       ├── 1_Afficher.py
│       ├── 2_Rechercher.py
│       ├── 3_
│       └── 4_
├── logs
├── README.md
├── .env
├── .venv
└── .gitignore
```

#### Ma base de données "quotes_db.csv"
Colonnes:
- `id`
- `text`

#### Commande pour lancer le serveur uvicorn

`uvicorn chemin.nom:app --reload --log-level debug`

#### Commandes pour le terminale pour faire un GET

- `Powershell` : `Invoke-WebRequest -Method GET "http://127.0.0.1:8000/citation"`

- `MAC Linux` : `CURL -X GET "http://127.0.0.1:8000/citation"`

#### Commande pour streamlit

`streamlit run frontend.\app.py`
