import sqlite3
import os
import shutil

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
        
        
    def get_audio(self, audio_id=None):
        if audio_id is None:
            self.cursor.execute("SELECT * FROM audio")
            return self.cursor.fetchall()
        else:
            self.cursor.execute("SELECT * FROM audio WHERE id = ?", (audio_id,))
            return self.cursor.fetchone()    
    
    
    def update_audio_name(self, audio_id, name):
        self.cursor.execute("UPDATE audio SET name = ? WHERE id = ?", (name, audio_id))
        self.conn.commit()
        
    def delete_audio(self, audio_id=None):
        if audio_id is None:
            # Delete from database
            self.cursor.execute("SELECT filepath FROM audio")
            rows = self.cursor.fetchall()
            self.cursor.execute("DELETE FROM audio")
            
            # Delete from folder
            for (file_path,) in rows:
                if os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                elif os.path.isfile(file_path):
                    os.remove(file_path)        
        else:
            self.cursor.execute("SELECT filepath FROM audio WHERE id = ?", (audio_id,))
            row = self.cursor.fetchone()
            
            if row:
                file_path = row[0]
                if os.path.exists(file_path):
                    os.remove(file_path)
                    
            self.cursor.execute("DELETE FROM audio WHERE id = ?", (audio_id,))
                
        self.conn.commit()
        
    def close(self):
        self.conn.close()