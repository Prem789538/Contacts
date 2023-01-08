import tkinter as tk
from tkinter import messagebox
from dbase import Dbass




class Window:
    def __init__(self):
        self.page = 0 #1st page
        self.show_total = 10
        self.conn = Dbass()
        self.addwin = None
        self.root = tk.Tk()
        self.root.geometry('400x600')
        self.root.title('Address Book')


        self.srchVar = tk.StringVar(self.root)
        
        


        self.design()
        self.fill_contacts()

        self.root.mainloop()


    def __del__(self):
        self.conn.disconnect()
        
    
    def design(self):
        srchBox = tk.Entry(self.root,textvariable=self.srchVar)
        srchBox.pack(side=tk.TOP)
        addBtn = tk.Button(self.root,text="Add",command=self.add_window)
        addBtn.pack(side=tk.TOP)

        self.btn_frame = tk.Frame(self.root,width=380,height=50)
        self.btn_frame.pack(side=tk.TOP)
        tk.Button(self.btn_frame,text="Prev",command=self.prev_contacts).pack(side=tk.LEFT)
        tk.Button(self.btn_frame,text="Next",command=self.next_contacts).pack(side=tk.RIGHT)

        self.contact_frame = tk.Frame(self.root,highlightbackground="black",highlightthickness=2,width=380,height=500)
        self.contact_frame.pack(side=tk.BOTTOM)
    
    def fill_contacts(self):
        contacts = self.conn.get_limit_contacts(self.page * self.show_total,self.show_total)
        y=0
        print(contacts)
        for contact in contacts:
            btn = tk.Button(self.contact_frame,text=contact[0])
            btn.place(height=50,width=376,y=y)
            y += 50
        rem = self.show_total - len(contacts)
        
        for i in range(rem):
            btn = tk.Button(self.contact_frame,state="disabled")
            
            btn.place(height=50,width=376,y=y)
            y += 50
    
    def prev_contacts(self):
        self.page -= 1
        if self.page < 0:
            self.page = 0
            return
        self.fill_contacts()

    def next_contacts(self):
        self.page += 1
        self.fill_contacts()
        

    def add_window(self):
        self.addwin = tk.Tk()
        self.addwin.geometry('300x400')
        self.addwin.title('New Contact')

        self.nameVar = tk.StringVar(self.addwin)
        self.numVar = tk.IntVar(self.addwin)

        self.numVar.set("")
        tk.Label(self.addwin,text="Full Name").grid(row=0,column=0)
        tk.Entry(self.addwin,textvariable=self.nameVar).grid(row=0,column=1)
        tk.Label(self.addwin,text="Ph. Number").grid(row=1,column=0)
        tk.Entry(self.addwin,textvariable=self.numVar).grid(row=1,column=1)
        tk.Button(self.addwin,text="Save",command=self.save_new).grid(row=2)

        self.addwin.mainloop()

    def save_new(self):
        name = self.nameVar.get()
        num = self.numVar.get()
        data_dict = {}
        data_dict['name'] = name
        data_dict['category'] = 'default'
        data_dict['num_list'] = [num]

        res = self.conn.add_contact(data_dict)
        if res == -1:
            messagebox.showerror("NOOO","Contact already exists!!!",parent=self.addwin)
        else:
            self.addwin.destroy()
    
    def update_contact(self):
        pass
    

def main():
    Window()




if __name__=="__main__":
    main()