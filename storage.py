import sqlite3

class Storage:
    def __init__(self, db_name="database.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()
        
    def create_table(self):
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS audio (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL,
                                length TEXT NOT NULL,
                                date TEXT NOT NULL,
                                filepath TEXT NOT NULL
                            )
                            """)
        self.conn.commit()
        
    def add_audio(self, name, length, date, filepath):
        self.cursor.execute(
            "INSERT INTO audio (name, length, date, filepath) VALUES (?, ?, ?, ?)", 
            (name, length, date, filepath)
        )
        self.conn.commit()
        
        
    def get_audio(self):
        self.cursor.execute("SELECT * FROM audio")
        return self.cursor.fetchall()
    
    def get_audio(self, audio_id):
        self.cursor.execute("SELECT * FROM audio WHERE id = ?", (audio_id))
        return self.cursor.fetchone()
    
    
    def update_audio(self, audio_id, name, length, date, filepath):
        self.cursor.execute(
            "UPDATE audio SET name = ?, length = ?, date =?, filepath =? WHERE id = ?", (name, length, date, filepath, audio_id)
            )
        self.conn.commit()
        
    
    def delete_audio(self, audio_id):
        self.cursor.execute("DELETE FROM audio WHERE id = ?", (audio_id))
        self.conn.commit()
        
    def close(self):
        self.conn.close()