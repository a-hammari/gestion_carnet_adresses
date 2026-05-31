from database import Database
from contact import Contact

class AddressBook:
    def __init__(self):
        # Initialise la connexion via le gestionnaire SQLite
        self.db = Database()

    def add_contact(self, contact):
        """Transmet l'ajout directement à la base de données SQLite."""
        success, message = self.db.add_contact(contact.nom, contact.email, contact.telephone)
        return success

    def remove_contact(self, nom):
        """Demande la suppression d'une entrée par son nom dans SQLite."""
        return self.db.remove_contact(nom)

    @property
    def contacts(self):
        """Récupère dynamiquement la liste fraîche de tous les contacts depuis la BDD."""
        rows = self.db.get_all_contacts()
        return [Contact(row[0], row[1], row[2]) for row in rows]