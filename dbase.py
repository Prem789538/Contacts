import sqlite3

class Dbass:
    def __init__(self):
        self.con = sqlite3.connect('mydb.db')
        if self.con:
            print("Connected to database successfully!")
        else:
            print("Can't connect to database! \n\nExiting...")
            exit(1)
        self.create_contact_table()
    
    def create_contact_table(self):
        cursorObj = self.con.cursor()
        cursorObj.execute("""CREATE TABLE IF NOT EXISTS contact_table(cntct_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL, category TEXT, last_updated TIMESTAMP)""")
        self.con.commit()
    
    def disconnect(self):
        self.con.close()
        print("Disconnected from database successfully!")