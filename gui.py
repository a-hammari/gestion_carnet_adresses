import tkinter as tk
from tkinter import messagebox
import re
from address_book import AddressBook
from contact import Contact

class ContactApp:
    def __init__(self, root):
        self.carnet = AddressBook()
        
        self.root = root
        self.root.title("Gestion de Carnet d'Adresses (v1.1.0)")
        self.root.geometry("500x550")
        self.root.resizable(False, False)
        
        # --- 1. frameH : Zone de Saisie (Haut) ---
        self.frameH = tk.LabelFrame(self.root, text=" Informations du Contact ", padx=15, pady=10)
        self.frameH.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(self.frameH, text="Nom :").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_nom = tk.Entry(self.frameH, width=35)
        self.entry_nom.grid(row=0, column=1, pady=5, padx=10)
        
        tk.Label(self.frameH, text="Email :").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_email = tk.Entry(self.frameH, width=35)
        self.entry_email.grid(row=1, column=1, pady=5, padx=10)
        
        tk.Label(self.frameH, text="Téléphone :").grid(row=2, column=0, sticky="w", pady=5)
        self.entry_tel = tk.Entry(self.frameH, width=35)
        self.entry_tel.grid(row=2, column=1, pady=5, padx=10)
        
        # --- 2. frameM : Zone d'Affichage (Milieu) ---
        self.frameM = tk.LabelFrame(self.root, text=" Contacts Enregistrés (Base SQLite) ", padx=15, pady=10)
        self.frameM.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)
        
        self.scrollbar = tk.Scrollbar(self.frameM, orient=tk.VERTICAL)
        self.listbox = tk.Listbox(self.frameM, yscrollcommand=self.scrollbar.set, width=60, font=("Courier", 9))
        
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # --- 3. frameB : Zone des Boutons (Bas) ---
        self.frameB = tk.Frame(self.root, pady=15)
        self.frameB.pack(fill=tk.X, padx=15)
        
        self.btn_ajouter = tk.Button(self.frameB, text="Ajouter", width=12, bg="#4CAF50", fg="white", font=("Arial", 9, "bold"), command=self.ajouter_contact)
        self.btn_ajouter.pack(side=tk.LEFT, padx=5)
        
        self.btn_supprimer = tk.Button(self.frameB, text="Supprimer", width=12, bg="#F44336", fg="white", font=("Arial", 9, "bold"), command=self.supprimer_contact)
        self.btn_supprimer.pack(side=tk.LEFT, padx=5)
        
        self.btn_quitter = tk.Button(self.frameB, text="Quitter", width=12, bg="#9E9E9E", fg="white", command=self.root.quit)
        self.btn_quitter.pack(side=tk.RIGHT, padx=5)

        # Chargement initial depuis SQLite
        self.rafraichir_liste()

    def valider_email(self, email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return bool(re.match(pattern, email))

    def valider_telephone(self, tel):
        return tel.isdigit() and len(tel) >= 10

    def rafraichir_liste(self):
        self.listbox.delete(0, tk.END)
        for c in self.carnet.contacts:
            affichage_aligne = f"{c.nom:<15} | {c.telephone:<13} | {c.email}"
            self.listbox.insert(tk.END, affichage_aligne)

    def ajouter_contact(self):
        nom = self.entry_nom.get().strip()
        email = self.entry_email.get().strip()
        tel = self.entry_tel.get().strip()
        
        if not nom or not email or not tel:
            messagebox.showwarning("Champs requis", "Tous les champs doivent être renseignés.")
            return
        
        if not self.valider_email(email):
            messagebox.showerror("Erreur", "L'adresse email est invalide.")
            return
        if not self.valider_telephone(tel):
            messagebox.showerror("Erreur", "Le téléphone doit contenir uniquement des chiffres (min 10).")
            return
            
        for c in self.carnet.contacts:
            if c.nom.lower() == nom.lower():
                messagebox.showerror("Doublon", f"Le contact '{nom}' existe déjà.")
                return

        nouveau_contact = Contact(nom, email, tel)
        if self.carnet.add_contact(nouveau_contact):
            self.rafraichir_liste()
            self.nettoyer_champs()
            messagebox.showinfo("Succès", "Contact enregistré dans SQLite.")
        else:
            messagebox.showerror("Erreur", "Impossible d'insérer le contact.")

    def supprimer_contact(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Erreur", "Veuillez sélectionner un contact à supprimer.")
            return
        
        index = selection[0]
        ligne_texte = self.listbox.get(index)
        nom_selectionne = ligne_texte.split('|')[0].strip()
        
        if messagebox.askyesno("Confirmation", f"Supprimer '{nom_selectionne}' de la base SQLite ?"):
            if self.carnet.remove_contact(nom_selectionne):
                self.rafraichir_liste()
                messagebox.showinfo("Supprimé", "Le contact a été retiré de la base de données.")

    def nettoyer_champs(self):
        self.entry_nom.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_tel.delete(0, tk.END)