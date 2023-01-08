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

        if not contacts:
            return -1
        
        for contact in contacts:
            btn = tk.Button(self.contact_frame,text=contact[0],command=lambda name=contact[0]:self.show_contact(name))
            btn.place(height=50,width=376,y=y)
            y += 50
        rem = self.show_total - len(contacts)
        
        for i in range(rem):
            btn = tk.Button(self.contact_frame,state="disabled")
            
            btn.place(height=50,width=376,y=y)
            y += 50
    
    def show_contact(self,name):
        show_win = tk.Tk()
        show_win.title("Contact")
        res = self.conn.get_contact(name)
        if len(res) != 1:
            print("Some error occured!\n\nExiting...")
            exit(1)
        
        name_var = tk.StringVar(show_win)
        category_var = tk.StringVar(show_win)

        num_var_list = []

        contact = res[0]
        name = contact[0]
        category = contact[1]

        name_var.set(name)
        category_var.set(category)

        num_list = self.conn.get_numbers(name)  #list of tuples

        num_var_list = [tk.IntVar(show_win) for i in range(len(num_list))]

        count=0
        for var in num_var_list:
            var.set(num_list[count][0])
            count+=1

        tk.Label(show_win,text="Name").grid(row=0,column=0)
        tk.Entry(show_win,textvariable=name_var).grid(row=0,column=1)

        tk.Label(show_win,text="Category").grid(row=1,column=0)
        tk.Entry(show_win,textvariable=category_var).grid(row=1,column=1)

        for i in range(len(num_list)):
            tk.Entry(show_win,textvariable=num_var_list[i]).grid(row=2+i)
        
        data_dict_updated = {}
        data_dict_updated['name'] = name_var
        data_dict_updated['category'] = category_var
        data_dict_updated['num_var_list'] = num_var_list
        data_dict_updated['window'] = show_win

        tk.Button(show_win,text="Update",command=lambda data=data_dict_updated: self.update_contact(data)).grid(row=len(num_list) + 2 )


        show_win.mainloop()

    def update_contact(self,data_dict_updated):
        name = data_dict_updated['name'].get()
        category = data_dict_updated['category'].get()
        num_list = [var.get() for var in data_dict_updated['num_var_list']]

        data_dict = {}
        data_dict['name'] = name
        data_dict['category'] = category
        data_dict['num_list'] = num_list

        self.conn.update_contact(data_dict)
        data_dict_updated['window'].destroy()



    def prev_contacts(self):
        self.page -= 1
        if self.page < 0:
            self.page = 0
            return
        self.fill_contacts()

    def next_contacts(self):
        self.page += 1
        res = self.fill_contacts()
        if res==-1:
            self.page -= 1

        

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
    
    
    

def main():
    Window()




if __name__=="__main__":
    main()