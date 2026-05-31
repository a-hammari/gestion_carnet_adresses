import tkinter as tk
from tkinter import messagebox
from database import Database

class LoginWindow:
    def __init__(self):
        self.database = Database()
        self.window = tk.Tk()
        self.window.title("Authentification - Gestion de Carnet d'Adresses (v1.1.0)")
        self.window.geometry("400x250")
        self.window.resizable(False, False)

        # --- 1. frame_auth : Zone de formulaire (Haut/Milieu) ---
        self.frame_auth = tk.LabelFrame(self.window, text=" Connexion Sécurisée ", padx=20, pady=15)
        self.frame_auth.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Champ Utilisateur
        tk.Label(self.frame_auth, text="Nom d'utilisateur :").grid(row=0, column=0, sticky="w", pady=10)
        self.username_entry = tk.Entry(self.frame_auth, width=25, font=("Arial", 10))
        self.username_entry.grid(row=0, column=1, pady=10, padx=10)

        # Champ Mot de passe
        tk.Label(self.frame_auth, text="Mot de passe :").grid(row=1, column=0, sticky="w", pady=10)
        self.password_entry = tk.Entry(self.frame_auth, width=25, font=("Arial", 10), show="*")
        self.password_entry.grid(row=1, column=1, pady=10, padx=10)

        # --- 2. frame_buttons : Zone d'actions (Bas) ---
        self.frame_buttons = tk.Frame(self.window, pady=5)
        self.frame_buttons.pack(fill=tk.X, padx=15)

        self.btn_login = tk.Button(self.frame_buttons, text="Se connecter", width=14, bg="#4A90D9", fg="white", font=("Arial", 9, "bold"), command=self.login)
        self.btn_login.pack(side=tk.RIGHT, padx=5)

        self.btn_annuler = tk.Button(self.frame_buttons, text="Quitter", width=12, bg="#9E9E9E", fg="white", command=self.window.quit)
        self.btn_annuler.pack(side=tk.LEFT, padx=5)

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if self.database.check_admin(username, password):
            messagebox.showinfo("Succès", "Connexion réussie.")
            self.window.destroy()  # Ferme la fenêtre d'authentification
            
            # Lancement immédiat de l'interface graphique du carnet d'adresses
            from gui import ContactApp
            root = tk.Tk()
            app = ContactApp(root)
            root.mainloop()
        else:
            messagebox.showerror("Erreur", "Identifiant ou mot de passe incorrect.")

    def run(self):
        self.window.mainloop()