import customtkinter as ct
import api_calls

ct.set_appearance_mode("dark")  # Modes: system (default), light, dark (default), light, dark

message_label = None  # Déclaration globale
def handle_login(username, password):
    isLog = api_calls.login(username, password)
    # using a database or other secure method
    if isLog:
        # Successful login
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
    else:
        # Invalid credentials
        message_label.configure(text="Nom d'utilisateur ou mot de passe incorrect.", text_color="red")


root = ct.CTk()
root.title("SoigneMoi - Secrétariat")
root.geometry("1280x720")

# Create a custom frame for the login form
login_frame = ct.CTkFrame(master=root)
login_frame.pack(fill=ct.BOTH, expand=True)

# Title label
title_label = ct.CTkLabel(master=login_frame, text="Connectez-vous", font=("Arial", 20))
title_label.pack(pady=10)

# Username label and entry
username_label = ct.CTkLabel(master=login_frame, text="E-mail:")
username_label.pack()
username_entry = ct.CTkEntry(master=login_frame, width=300)
username_entry.pack()

# Password label and entry (conceal password)
password_label = ct.CTkLabel(master=login_frame, text="Mot de passe:")
password_label.pack()
password_entry = ct.CTkEntry(master=login_frame, width=300, show="*")
password_entry.pack()

# Remember me checkbox (add functionality as needed)
remember_me_var = ct.IntVar()
remember_me_checkbox = ct.CTkCheckBox(master=login_frame, text="Se souvenir de moi", variable=remember_me_var)
remember_me_checkbox.pack()

# Login button
login_button = ct.CTkButton(master=login_frame, text="Se connecter",
                            command=lambda: handle_login(username_entry.get(), password_entry.get()))
login_button.pack(pady=10)

# Message label for displaying success/error messages
message_label = ct.CTkLabel(master=login_frame, text=" ", font=("Arial", 10))
message_label.pack()

root.mainloop()
message_label.pack()

root.mainloop()
