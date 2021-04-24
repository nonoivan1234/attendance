import sqlite3

class Database:
    def __init__(self, db): 
        # create the table if not exists and delete the curerent database
        
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS tb (id INTEGER PRIMARY KEY, date_ text, zero text, morning text, one text, two text, three text, four text, five text, six text, seven text, eight text)")
        self.cur.execute('DELETE FROM tb;',)
        self.conn.commit()
        
    def fetch(self):        
        # fetch the rows and return back
        
        self.cur.execute("SELECT * FROM tb")
        rows = self.cur.fetchall()
        return rows
        
    def insert(self, date_, zero, morning, one, two, three, four, five, six, seven, eight):
        # insert the data to the database
        
        self.cur.execute("INSERT INTO tb VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (date_, zero, morning, one, two, three, four, five, six, seven, eight))
        self.conn.commit()
        
    def count_item(self, column):
        # count every item, append in the list, and return back the list
        
        c = []
        self.cur.execute('SELECT COUNT(%s) FROM tb WHERE %s = "遲";'%(column, column))
        c.append(self.cur.fetchone()[0])
        self.cur.execute('SELECT COUNT(%s) FROM tb WHERE %s = "公";'%(column, column))
        c.append(self.cur.fetchone()[0])
        self.cur.execute('SELECT COUNT(%s) FROM tb WHERE %s = "曠";'%(column, column))
        c.append(self.cur.fetchone()[0])
        self.cur.execute('SELECT COUNT(%s) FROM tb WHERE %s = "病";'%(column, column))
        c.append(self.cur.fetchone()[0])
        self.cur.execute('SELECT COUNT(%s) FROM tb WHERE %s = "事";'%(column, column))
        c.append(self.cur.fetchone()[0])
        return c