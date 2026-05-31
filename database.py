import sqlite3
import hashlib

class Database:
    def __init__(self, database_name="contacts.db"):
        self.database_name = database_name
        self.connection = sqlite3.connect(self.database_name)
        self.cursor = self.connection.cursor()
        self.create_tables()
        self.ensure_default_admin()

    def create_tables(self):
        """Crée les tables nécessaires si elles n'existent pas encore."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                phone TEXT NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            )
        """)
        self.connection.commit()

    # --- Gestion des Contacts ---
    def add_contact(self, name, email, phone):
        try:
            self.cursor.execute(
                "INSERT INTO contacts (name, email, phone) VALUES (?, ?, ?)",
                (name, email, phone)
            )
            self.connection.commit()
            return True, "Contact inséré avec succès."
        except sqlite3.IntegrityError as error:
            return False, f"Erreur d'intégrité : {error}"

    def remove_contact(self, name):
        self.cursor.execute("DELETE FROM contacts WHERE name = ?", (name,))
        self.connection.commit()
        return self.cursor.rowcount > 0

    def get_all_contacts(self):
        self.cursor.execute("SELECT name, email, phone FROM contacts ORDER BY name ASC")
        return self.cursor.fetchall()

    # --- Gestion de l'Authentification Security ---
    def hash_password(self, password):
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def add_admin(self, username, password):
        password_hash = self.hash_password(password)
        try:
            self.cursor.execute(
                "INSERT INTO admins (username, password_hash) VALUES (?, ?)",
                (username, password_hash)
            )
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def check_admin(self, username, password):
        password_hash = self.hash_password(password)
        self.cursor.execute(
            "SELECT id FROM admins WHERE username = ? AND password_hash = ?",
            (username, password_hash)
        )
        admin = self.cursor.fetchone()
        return admin is not None

    def ensure_default_admin(self):
        """Garantit la présence d'un compte admin par défaut (admin / admin)."""
        self.cursor.execute("SELECT id FROM admins WHERE username = ?", ("admin",))
        if self.cursor.fetchone() is None:
            self.add_admin("admin", "admin")

    def close(self):
        self.connection.close()