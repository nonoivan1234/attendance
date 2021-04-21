import sqlite3

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS parts (id INTEGER PRIMARY KEY, date_ text, zero text, zeroo text, one text, two text, three text, four text, five text, six text, seven text, eight text)")
        self.conn.commit()
        
    def fetch(self):
        self.cur.execute("SELECT * FROM parts")
        rows = self.cur.fetchall()
        return rows
        
    def insert(self, date_, zero, zeroo, one, two, three, four, five, six, seven, eight):
        self.cur.execute("INSERT INTO parts VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (date_, zero, zeroo, one, two, three, four, five, six, seven, eight))
        self.conn.commit()
        
db = Database('absent.db')