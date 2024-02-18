from tkinter import *
from customtkinter import *
from datetime import datetime

import requests
import json
import jwt

access_token = None  # Variable globale pour stocker le token


def login(username, password, message_label):
    api_url = "http://127.0.0.1:8080/api/login"
    data = {"username": username, "password": password}
    data = json.dumps(data)
    response = requests.post(api_url, data=data)
    if response.status_code == 200:
        response_data = json.loads(response.content)
        encoded_token = response_data.get("token")
        # Décoder le token
        decoded_token = jwt.decode(encoded_token, options={"verify_signature": False})
        print(decoded_token)
        roles = decoded_token.get("roles")  # Supposons que les rôles sont inclus dans le token
        if encoded_token and "ROLE_SECRETARIAT" in roles:
            global access_token
            access_token = encoded_token
            return True
        else:
            message_label.configure(text="Erreur, veuillez contacter votre administrateur", text_color="red")
            return False
    else:
        message_label.configure(text="Nom d'utilisateur ou mot de passe incorrect.", text_color="red")
        return False


def call_api_with_token():
    api_url = "http://localhost:8080/api/visits"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(api_url, headers=headers)
    return (response.content.decode("utf-8"))


# ... Autres fonctions d'appel à l'API ...


def get_patient_details(patient_id, visit_id):
    print(patient_id, visit_id)
    api_url = f"http://localhost:8080/api/patients/{patient_id}/{visit_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(api_url, headers=headers)
    return (response.content.decode("utf-8"))


def print_patient_details(visit_id, patient_id, root):
    # Récupérer les informations détaillées de la visite à partir de l'API
    details = get_patient_details(patient_id, visit_id)
    details = json.loads(details)
    print(details)
    # Création d'une nouvelle fenêtre pour afficher les détails
    details_window = CTkToplevel(root)

    # Obtenir la largeur et la hauteur de l'écran
    screen_width = details_window.winfo_screenwidth()
    screen_height = details_window.winfo_screenheight()

    # Calculer la position x et y pour centrer la fenêtre
    x = (screen_width / 2) - (details_window.winfo_reqwidth() / 2)
    y = (screen_height / 2) - (details_window.winfo_reqheight() / 2)

    # Positionner la fenêtre au centre de l'écran
    details_window.geometry("+%d+%d" % (x, y))
    # Création d'un fieldset pour les informations personnelles du patient
    personal_info_frame = CTkFrame(master=details_window, fg_color="white",
                                   corner_radius=10)  # Ajout de couleur et coins arrondis
    personal_info_frame.pack(pady=10, padx=20, fill=BOTH)

    # Ajout d'un titre au fieldset
    personal_info_title = CTkLabel(master=personal_info_frame, text="Informations personnelles du patient",
                                font=("Arial", 16), text_color="black")
    personal_info_title.pack()

    # Création des labels pour chaque détail et ajout au fieldset
    firstname_label = CTkLabel(master=personal_info_frame, text=f"Prénom : {details['user']['firstname']}",
                            font=("Arial", 14), text_color="black")
    firstname_label.pack()

    lastname_label = CTkLabel(master=personal_info_frame, text=f"Nom : {details['user']['lastname']}", font=("Arial", 14), text_color="black")
    lastname_label.pack()

    address_label = CTkLabel(master=personal_info_frame, text=f"Adresse : {details['adress']}", font=("Arial", 14), text_color="black")
    address_label.pack()

    # Création d'un fieldset pour les visites
    visits_frame = CTkFrame(master=details_window, fg_color="white",
                            corner_radius=10)  # Ajout de couleur et coins arrondis
    visits_frame.pack(pady=10, padx=20, fill=BOTH)

    # Ajout d'un titre au fieldset
    visits_title = CTkLabel(master=visits_frame, text="Détail de la visite en cours",
                         font=("Arial", 16), text_color="black")
    visits_title.pack()

    for visit in details['visits']:
        startdate = datetime.strptime(visit['startDate'], "%Y-%m-%dT%H:%M:%S%z")  # Convertir la date en objet datetime
        startdate_label = CTkLabel(master=visits_frame, text=f"Date de début : {startdate.strftime('%d-%m-%Y')}",
                                   font=("Arial", 14), text_color="black")
        startdate_label.pack()

        enddate = datetime.strptime(visit['EndDate'], "%Y-%m-%dT%H:%M:%S%z")  # Convertir la date en objet datetime
        enddate_label = CTkLabel(master=visits_frame, text=f"Date de fin : {enddate.strftime('%d-%m-%Y')}",
                                 font=("Arial", 14), text_color="black")
        enddate_label.pack()

        reason_label = CTkLabel(master=visits_frame, text=f"Raison : {visit['reason']}", font=("Arial", 14), text_color="black")
        reason_label.pack()

    # Création d'un fieldset pour les prescriptions
    prescriptions_frame = CTkFrame(master=details_window,
                                   corner_radius=10, fg_color="white")  # Ajout de couleur et coins arrondis
    prescriptions_frame.pack(pady=10, padx=20, fill=BOTH)

    # Ajout d'un titre au fieldset
    prescriptions_title = CTkLabel(master=prescriptions_frame, text="Prescriptions",
                                font=("Arial", 16), text_color="black")
    prescriptions_title.pack()

    for prescription in details['prescriptions']:
        for medication in prescription['MedicationList']:
            drug_label = CTkLabel(master=prescriptions_frame,
                                  text=f"Médicament : {medication['drug']['name']}, Dosage : {medication['dosage']}",
                                  font=("Arial", 14), text_color="black")
            drug_label.pack()

        if prescription['opinion']:
            opinion_title_label = CTkLabel(master=prescriptions_frame,
                                           text=f"Titre de l'opinion : {prescription['opinion']['title']}",
                                           font=("Arial", 14), text_color="black")
            opinion_title_label.pack()

            opinion_description_label = CTkLabel(master=prescriptions_frame,
                                                 text=f"Description de l'opinion : {prescription['opinion']['description']}",
                                                 font=("Arial", 14), text_color="black")
            opinion_description_label.pack()
        else:
            no_opinion_label = CTkLabel(master=prescriptions_frame,
                                        text="Aucune opinion disponible.", font=("Arial", 14), text_color="black")
            no_opinion_label.pack()

    # Bouton pour revenir à l'affichage principal
    back_button = CTkButton(master=details_window, text="Retour", command=lambda: details_window.destroy())
    back_button.pack()
