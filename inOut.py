from customtkinter import *
import api_calls
import json

def creer_main_frame(root, username):
    main_frame = CTkFrame(master=root)
    main_frame.pack(fill=BOTH, expand=True)

    welcome_label = CTkLabel(master=main_frame, text=f"Bienvenue, {username}!")
    welcome_label.pack()

    visitsListJson = api_calls.call_api_with_token()  # Récupérer le JSON de l'API
    visitsList = json.loads(visitsListJson)  # Décoder le JSON en une liste Python
    print(visitsList)
    # Créer un frame pour chaque visite
    for visit in visitsList:
        visit_frame = CTkFrame(master=main_frame, fg_color="gray",
                                   corner_radius=10)  # Ajout de couleur et coins arrondis
        visit_frame.pack(pady=10, padx=20)  # Augmentation de l'espacement

        # Utilisation de CTkLabel pour un style plus moderne
        firstname_label = CTkLabel(master=visit_frame, text=f"Prénom : {visit['patient']['user']['firstname']}",
                                       text_color="black")
        lastname_label = CTkLabel(master=visit_frame, text=f"Nom : {visit['patient']['user']['lastname']}",
                                      text_color="black")
        startdate_label = CTkLabel(master=visit_frame, text=f"Date de début : {visit['startDate']}",
                                       text_color="black")
        enddate_label = CTkLabel(master=visit_frame, text=f"Date de fin : {visit['EndDate']}", text_color="black")

        # Disposition des labels en grille
        for label in [firstname_label, lastname_label, startdate_label, enddate_label]:
            label.grid(row=0, column=visit_frame.grid_size()[0], padx=10, pady=5)
            visit_frame.grid_columnconfigure(visit_frame.grid_size()[0], weight=1)  # Étalement des labels

    return main_frame
