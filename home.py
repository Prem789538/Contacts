import tkinter as tk
from tkinter import ttk
from dbase import Dbass




class Window:
    def __init__(self):
        self.conn = Dbass()
        self.addwin = None
        self.root = tk.Tk()
        self.root.geometry('400x600')
        self.root.title('Address Book')


        self.srchVar = tk.StringVar(self.root)
        
        


        self.design()


        self.root.mainloop()


    def __del__(self):
        self.conn.disconnect()
        
    
    def design(self):
        srchBox = tk.Entry(self.root,textvariable=self.srchVar)
        srchBox.pack(side=tk.TOP)
        addBtn = tk.Button(self.root,text="Add",command=self.add_window)
        addBtn.pack(side=tk.TOP)

    def add_window(self):
        self.addwin = tk.Tk()
        self.addwin.geometry('300x400')
        self.addwin.title('New Contact')

        self.nameVar = tk.StringVar(self.addwin)
        self.numVar = tk.IntVar(self.addwin)

        
        tk.Label(self.addwin,text="Full Name").grid(row=0,column=0)
        tk.Entry(self.addwin,textvariable=self.nameVar).grid(row=0,column=1)
        tk.Label(self.addwin,text="Ph. Number").grid(row=1,column=0)
        tk.Entry(self.addwin,textvariable=self.numVar).grid(row=1,column=1)
        tk.Button(self.addwin,text="Save",command=self.save_new).grid(row=2)

        #self.addwin.mainloop()

    def save_new(self):
        name = self.nameVar.get()
        num = self.numVar.get()
        print(name)
        print(num)
        self.addwin.destroy()
    

def main():
    Window()




if __name__=="__main__":
    main()