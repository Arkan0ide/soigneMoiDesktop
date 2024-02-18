import customtkinter as ct
import api_calls

ct.set_appearance_mode("dark")  # Modes: system (default), light, dark (default), light, dark

message_label = None  # Déclaration globale
def handle_login(username, password):
    isLog = api_calls.login(username, password, message_label)

    if isLog:
        message_label.configure(text="Connexion réussie!", text_color="green")
        username_entry.delete(0, ct.END)
        password_entry.delete(0, ct.END)

        # Importer la fonction depuis le fichier inOut.py
        from inOut import creer_main_frame

        # Créer le nouveau frame en utilisant la fonction importée
        main_frame = creer_main_frame(root, username)

        # Détruire le frame de connexion
        login_frame.destroy()

        # Afficher le nouveau frame
        main_frame.pack()



root = ct.CTk()
root.title("SoigneMoi - Secrétariat")
root.geometry("1920x1080")

# Création d'un frame pour le formulaire de connexion
login_frame = ct.CTkFrame(master=root, bg_color="#343a40")
login_frame.pack(fill=ct.BOTH, expand=True)

# Ajout du titre
title_label = ct.CTkLabel(master=login_frame, text="Connectez-vous", font=("Arial", 20))
title_label.pack(pady=10)

# Identifiant
username_label = ct.CTkLabel(master=login_frame, text="E-mail:")
username_label.pack()
username_entry = ct.CTkEntry(master=login_frame, width=600, height=30)
username_entry.pack()

# Password
password_label = ct.CTkLabel(master=login_frame, text="Mot de passe:")
password_label.pack()
password_entry = ct.CTkEntry(master=login_frame, width=600, height=30, show="*")
password_entry.pack()

# Bouton de connexion
login_button = ct.CTkButton(master=login_frame, text="Se connecter", fg_color="#007bff",
                            command=lambda: handle_login(username_entry.get(), password_entry.get()))
login_button.pack(pady=10)

# Message d'erreur ou de succès
message_label = ct.CTkLabel(master=login_frame, text=" ", font=("Arial", 10))
message_label.pack()

root.mainloop()
