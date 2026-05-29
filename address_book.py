from contact import Contact

class AddressBook:
    def __init__(self):
        self.contacts = []

    def add_contact(self, contact):
        self.contacts.append(contact)
        print(f"Contact {contact.nom} ajouté avec succès.")

    def remove_contact(self, nom):
        for contact in self.contacts:
            if contact.nom == nom:
                self.contacts.remove(contact)
                print(f"Contact {nom} supprimé.")
                return
        print("Contact introuvable.")

    def display_contacts(self):
        if not self.contacts:
            print("Le carnet est vide.")
        else:
            for contact in self.contacts:
                print(contact)