from tkinter import *
from customtkinter import *

import requests
import json


access_token = None  # Variable globale pour stocker le token (à adapter selon vos besoins)


def login(username, password):
    api_url = "http://127.0.0.1:8080/api/login"
    data = {"username": username, "password": password}
    # Conversion en double quote
    data = json.dumps(data)
    response = requests.post(api_url, data=data)
    if response.status_code == 200:
        response_data = json.loads(response.content)
        token = response_data.get("token")
        if token:
            global access_token
            access_token = token
        return True
    else:
        return False
        # ... Actions à effectuer après la connexion (e.g., messages à l'utilisateur) ...
        # else:
    # ... Gérer l'absence de token dans la réponse ...


# else:


# ... Gérer l'échec de la connexion ...

def call_api_with_token():
    api_url = "http://localhost:8080/api/visits"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(api_url, headers=headers)
    return (response.content.decode("utf-8"))

# ... Autres fonctions d'appel à l'API ...
