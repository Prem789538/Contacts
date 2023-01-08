import sqlite3
import datetime

class Dbass:
    def __init__(self):
        self.con = sqlite3.connect('mydb.db')
        if self.con:
            print("Connected to database successfully!")
        else:
            print("Can't connect to database! \n\nExiting...")
            exit(1)

        self.create_contact_table()
        self.create_number_table()
    
    def create_contact_table(self):
        cursorObj = self.con.cursor()
        cursorObj.execute("""CREATE TABLE IF NOT EXISTS contact_table(
        name TEXT PRIMARY KEY, category TEXT, last_updated TIMESTAMP)""")
        self.con.commit()
        cursorObj.close()
    
    def create_number_table(self):
        cursorObj = self.con.cursor()
        cursorObj.execute("""CREATE TABLE IF NOT EXISTS number_table(cntct_id TEXT , number INTEGER NOT NULL, 
        FOREIGN KEY(cntct_id) REFERENCES contact_table(name) )""")
        self.con.commit()
        cursorObj.close()


    def add_contact(self,data_dict): #returns 0 when success else -1
        cursorObj = self.con.cursor()
        if self.get_contact(data_dict['name']):
            print("Contact name already exists!")
            return -1

        sql = """INSERT INTO contact_table (name,category,last_updated) VALUES (?,?,?)"""
        timestamp = datetime.datetime.now()
        name = data_dict.get('name')
        data = (name,data_dict.get('category','default'),timestamp)
        cursorObj.execute(sql,data)

        
        sql = """INSERT INTO number_table VALUES (?,?) """
        data = []
        for num in data_dict['num_list']:
            data.append((name,num))

        cursorObj.executemany(sql,data)
        
        self.con.commit()
        cursorObj.close()

    def get_contact(self,name):
        cursorObj = self.con.cursor()
        sql = """SELECT * FROM contact_table where name = ?"""
        cursorObj.execute(sql,(name,))
        res = cursorObj.fetchall()
        cursorObj.close()
        return res
    
    def get_limit_contacts(self,offset,count):
        cursorObj = self.con.cursor()
        sql = """SELECT * FROM contact_table ORDER BY name ASC LIMIT ?,?"""
        cursorObj.execute(sql,(offset,count))
        data = cursorObj.fetchall()
        cursorObj.close()
        return data


    def disconnect(self):
        self.con.close()
        print("Disconnected from database successfully!")