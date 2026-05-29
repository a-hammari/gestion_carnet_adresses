from contact import Contact
from address_book import AddressBook

def main():
    carnet = AddressBook()
    
    while True:
        print("\n--- Menu Carnet d'Adresses ---")
        print("1. Ajouter un contact")
        print("2. Supprimer un contact")
        print("3. Afficher les contacts")
        print("4. Quitter")
        
        choix = input("Choisissez une option (1-4) : ")
        
        if choix == '1':
            nom = input("Nom : ")
            email = input("Email : ")
            tel = input("Téléphone : ")
            carnet.add_contact(Contact(nom, email, tel))
        elif choix == '2':
            nom = input("Nom du contact à supprimer : ")
            carnet.remove_contact(nom)
        elif choix == '3':
            carnet.display_contacts()
        elif choix == '4':
            print("Fermeture de l'application.")
            break
        else:
            print("Choix invalide.")

if __name__ == "__main__":
    main()