import sqlite3
from pathlib import Path
from modules.constants import DEFAULT_DATABESE_PATH

class Repository:
    def __init__(self, path=DEFAULT_DATABESE_PATH):
        file_path = Path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.touch(exist_ok=True)

        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()
    
    def __del__(self):
        if hasattr(self, 'connection'):
            self.connection.close()
    
    def migrate(self):
        self.cursor.execute('DROP TABLE IF EXISTS Documents')
        self.cursor.execute('''
                    CREATE TABLE Documents (
                    id integer primary key,
                    document text
                    )''')
        self.connection.commit()

    def add(self, data):
        for id, text in data.items():
            self.cursor.execute('''
            INSERT INTO Documents (id, document)
            VALUES (?, ?)
            ''', (id, text))
        self.connection.commit()

    def get(self, id):
        self.cursor.execute('''
            SELECT document
            FROM Documents
            WHERE id = ?
            ''', (str(id),))
        result = self.cursor.fetchone()

        return result[0]
