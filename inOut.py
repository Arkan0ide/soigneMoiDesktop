from customtkinter import *
from datetime import datetime
import api_calls
import json


def creer_main_frame(root, username):
    main_frame = CTkFrame(master=root)
    main_frame.pack(fill=BOTH, expand=True)

    # Ajout du titre
    title_label = CTkLabel(master=main_frame, text="Entrée(s) et sortie(s) du jour", font=("Arial", 20))
    title_label.pack(pady=10)

    visitsListJson = api_calls.call_api_with_token()  # Récupérer le JSON de l'API
    visitsList = json.loads(visitsListJson)  # Décoder le JSON en une liste Python
    # Création d'un frame pour chaque visite
    for visit in visitsList:
        visit_frame = CTkFrame(master=main_frame, fg_color="white", corner_radius=10)
        visit_frame.pack(pady=10, padx=20)

        # Utilisation de CTkLabel pour un style plus moderne
        firstname_label = CTkLabel(master=visit_frame, text=f"{visit['patient']['user']['firstname']}",
                                   text_color="black", width=50)
        lastname_label = CTkLabel(master=visit_frame, text=f"{visit['patient']['user']['lastname']}",
                                  text_color="black", width=50)
        startdate = datetime.strptime(visit['startDate'], "%Y-%m-%dT%H:%M:%S%z")
        enddate = datetime.strptime(visit['EndDate'], "%Y-%m-%dT%H:%M:%S%z")

        # Formater les dates
        formatted_startdate = startdate.strftime("%d/%m/%Y")
        formatted_enddate = enddate.strftime("%d/%m/%Y")

        date_label = CTkLabel(master=visit_frame,
                              text=f"Date du séjour : {formatted_startdate}  -  {formatted_enddate}",
                              text_color="black", width=60)
        patient_button = CTkButton(master=visit_frame, text="Accéder au dossier du patient", fg_color="#007bff",
                                   command=lambda visit_id=visit['id'],
                                                  patient_id=visit['patient']['id']: api_calls.print_patient_details(
                                       visit_id, patient_id, root))

        patient_button.grid(row=0, column=visit_frame.grid_size()[0] + 1, padx=10, pady=5,
                            sticky='w')  # Utilisation de 'w' pour aligner le bouton à gauche

        # Disposition des labels en grille
        for label in [firstname_label, lastname_label, date_label]:
            label.grid(row=0, column=visit_frame.grid_size()[0], padx=10, pady=5,
                       sticky='w')  # Utilisation de 'w' pour aligner les labels à gauche
            visit_frame.grid_columnconfigure(visit_frame.grid_size()[0], weight=1)  # Étalement des labels

    return main_frame
