from tkinter import *
from customtkinter import *

import requests
import json

access_token = None  # Variable globale pour stocker le token


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
    # ... Gérer l'absence de token dans la réponse ...


def call_api_with_token():
    api_url = "http://localhost:8080/api/visits"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(api_url, headers=headers)
    return (response.content.decode("utf-8"))


# ... Autres fonctions d'appel à l'API ...


def get_patient_details(patient_id, visit_id):
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
    details_window = Toplevel(root)

    # Création d'un fieldset pour les informations personnelles du patient
    personal_info_frame = CTkFrame(master=details_window, fg_color="#00CED1",
                                   corner_radius=10)  # Ajout de couleur et coins arrondis
    personal_info_frame.pack(pady=10, padx=20, fill=BOTH)

    # Ajout d'un titre au fieldset
    personal_info_title = Label(master=personal_info_frame, text="Informations personnelles du patient",
                                font=("Arial", 16), bg="#00CED1")
    personal_info_title.pack()

    # Création des labels pour chaque détail et ajout au fieldset
    firstname_label = Label(master=personal_info_frame, text=f"Prénom : {details['user']['firstname']}",
                            font=("Arial", 14), bg="#00CED1")
    firstname_label.pack()

    lastname_label = Label(master=personal_info_frame, text=f"Nom : {details['user']['lastname']}", font=("Arial", 14),
                           bg="#00CED1")
    lastname_label.pack()

    address_label = Label(master=personal_info_frame, text=f"Adresse : {details['adress']}", font=("Arial", 14),
                          bg="#00CED1")
    address_label.pack()

    for visit in details['visits']:
        startdate_label = CTkLabel(master=details_window, text=f"Date de début : {visit['startDate']}",
                                   font=("Arial", 14), text_color="blue")
        startdate_label.pack()

        enddate_label = CTkLabel(master=details_window, text=f"Date de fin : {visit['EndDate']}", font=("Arial", 14),
                                 text_color="blue")
        enddate_label.pack()

        reason_label = CTkLabel(master=details_window, text=f"Raison : {visit['reason']}", font=("Arial", 14),
                                text_color="blue")
        reason_label.pack()

    for prescription in details['prescriptions']:
        for medication in prescription['MedicationList']:
            drug_label = CTkLabel(master=details_window,
                                  text=f"Médicament : {medication['drug']['name']}, Dosage : {medication['dosage']}",
                                  font=("Arial", 14), text_color="blue")
            drug_label.pack()

        if prescription['opinion']:
            opinion_title_label = CTkLabel(master=details_window,
                                           text=f"Titre de l'opinion : {prescription['opinion']['title']}",
                                           font=("Arial", 14), text_color="blue")
            opinion_title_label.pack()

            opinion_description_label = CTkLabel(master=details_window,
                                                 text=f"Description de l'opinion : {prescription['opinion']['description']}",
                                                 font=("Arial", 14), text_color="blue")
            opinion_description_label.pack()
        else:
            no_opinion_label = CTkLabel(master=details_window,
                                        text="Aucune opinion disponible.", font=("Arial", 14), text_color="blue")
            no_opinion_label.pack()

    # Bouton pour revenir à l'affichage principal
    back_button = CTkButton(master=details_window, text="Retour", command=lambda: details_window.destroy())
    back_button.pack()
