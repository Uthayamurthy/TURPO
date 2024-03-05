'''
T.U.R.P.O (Trustworthy Utility for Reliable Password Organisation) - A simple to use, feature-rich password management software. 

    Copyright (C) 2023  R Uthaya Murthy

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

Contact Author : uthayamurthy2006@gmail.com
'''

import ttkbootstrap as ttk
from ttkbootstrap import dialogs
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from datetime import date

class Create_Email(ttk.Frame):

    def __init__(self, main, pm, master):
        super().__init__(main)
        self.master = master
        self.PM = pm
        
        cname_lbl = ttk.Label(self, text='Credential Name : ', font=('Helventica', 15, 'bold'))
        cname_lbl.grid(row=0, column=0, padx=5, pady=20, sticky=NSEW)

        self.cname_entry = ttk.Entry(self, font=('Helventica', 15, 'bold'))
        self.cname_entry.grid(row=0, column=1, padx=5, pady=20, sticky=NSEW)
        
        uname_lbl = ttk.Label(self, text='Username : ', font=('Helventica', 15, 'bold'))
        uname_lbl.grid(row=1, column=0, padx=5, pady=20, sticky=NSEW)

        self.uname_entry = ttk.Entry(self, font=('Helventica', 15, 'bold'))
        self.uname_entry.grid(row=1, column=1, padx=5, pady=20, sticky=NSEW)

        email_lbl = ttk.Label(self, text='Email : ', font=('Helventica', 15, 'bold'))
        email_lbl.grid(row=2, column=0, padx=5, pady=20, sticky=NSEW)

        self.email_entry = ttk.Entry(self, font=('Helventica', 15, 'bold'))
        self.email_entry.grid(row=2, column=1, padx=5, pady=20, sticky=NSEW)

        password_lbl = ttk.Label(self, text='Password : ', font=('Helventica', 15, 'bold'))
        password_lbl.grid(row=3, column=0, padx=5, pady=20, sticky=NSEW)

        self.password_entry = ttk.Entry(self, font=('Helventica', 15, 'bold'))
        self.password_entry.grid(row=3, column=1, padx=5, pady=20, sticky=NSEW)

        self.save_btn = ttk.Button(self, text='Save', bootstyle='outline-success', command=self.save_credentials)
        self.save_btn.grid(row=4, column=2, padx=5, pady=20, sticky=NSEW)

    def save_credentials(self):
        section = self.cname_entry.get()
        self.PM.set_section(section)
        self.PM.set_entry(section, 'type', 'Email')
        self.PM.set_secret(section, 'email', self.email_entry.get())
        self.PM.set_secret(section, 'username', self.uname_entry.get())
        self.PM.set_secret(section, 'password', self.password_entry.get())
        today = date.today()
        d = today.strftime("%d/%m/%Y")
        self.PM.set_entry(section, 'date', d)
        self.PM.write()
        self.master.kill_window()

class Create_Social_Media(ttk.Frame):

    def __init__(self, main, pm, master):
        super().__init__(main)
        self.master = master
        self.PM = pm
        
        cname_lbl = ttk.Label(self, text='Credential Name : ', font=('Helventica', 15, 'bold'))
        cname_lbl.grid(row=0, column=0, padx=5, pady=20, sticky=NSEW)

        self.cname_entry = ttk.Entry(self, font=('Helventica', 15, 'bold'))
        self.cname_entry.grid(row=0, column=1, padx=5, pady=20, sticky=NSEW)
        
        uname_lbl = ttk.Label(self, text='Username : ', font=('Helventica', 15, 'bold'))
        uname_lbl.grid(row=1, column=0, padx=5, pady=20, sticky=NSEW)

        self.uname_entry = ttk.Entry(self, font=('Helventica', 15, 'bold'))
        self.uname_entry.grid(row=1, column=1, padx=5, pady=20, sticky=NSEW)

        password_lbl = ttk.Label(self, text='Password : ', font=('Helventica', 15, 'bold'))
        password_lbl.grid(row=2, column=0, padx=5, pady=20, sticky=NSEW)

        self.password_entry = ttk.Entry(self, font=('Helventica', 15, 'bold'))
        self.password_entry.grid(row=2, column=1, padx=5, pady=20, sticky=NSEW)

        self.save_btn = ttk.Button(self, text='Save', bootstyle='outline-success', command=self.save_credentials)
        self.save_btn.grid(row=3, column=2, padx=5, pady=20, sticky=NSEW)

    def save_credentials(self):
        section = self.cname_entry.get()
        self.PM.set_section(section)
        self.PM.set_entry(section, 'type', 'Social Media')
        self.PM.set_secret(section, 'username', self.uname_entry.get())
        self.PM.set_secret(section, 'password', self.password_entry.get())
        today = date.today()
        d = today.strftime("%d/%m/%Y")
        self.PM.set_entry(section, 'date', d)
        self.PM.write()
        self.master.kill_window()

class Create_Phone_Pin(ttk.Frame):

    def __init__(self, main, pm, master):
        super().__init__(main)
        self.master = master
        self.PM = pm
        
        cname_lbl = ttk.Label(self, text='Credential Name : ', font=('Helventica', 15, 'bold'))
        cname_lbl.grid(row=0, column=0, padx=5, pady=20, sticky=NSEW)

        self.cname_entry = ttk.Entry(self, font=('Helventica', 15, 'bold'))
        self.cname_entry.grid(row=0, column=1, padx=5, pady=20, sticky=NSEW)
        
        pin_lbl = ttk.Label(self, text='Pin : ', font=('Helventica', 15, 'bold'))
        pin_lbl.grid(row=3, column=0, padx=5, pady=20, sticky=NSEW)

        self.pin_entry = ttk.Entry(self, font=('Helventica', 15, 'bold'))
        self.pin_entry.grid(row=3, column=1, padx=5, pady=20, sticky=NSEW)

        self.save_btn = ttk.Button(self, text='Save', bootstyle='outline-success', command=self.save_credentials)
        self.save_btn.grid(row=4, column=2, padx=5, pady=20, sticky=NSEW)

    def save_credentials(self):
        section = self.cname_entry.get()
        self.PM.set_section(section)
        self.PM.set_entry(section, 'type', 'Phone Pin')
        self.PM.set_secret(section, 'pin', self.pin_entry.get())
        today = date.today()
        d = today.strftime("%d/%m/%Y")
        self.PM.set_entry(section, 'date', d)
        self.PM.write()
        self.master.kill_window()

class Add_Credential(ttk.Toplevel):

    def __init__(self,  parent, PATH, PM):

        self.parent = parent
        self.PM = PM
        self.PATH = PATH

        super().__init__(title='Add New Credentials')
        super().geometry('1000x750')

        self.grab_set()
        
        self.creation_frame = None

        # Header
        hdr_frame = ttk.Frame(self)
        hdr_frame.grid(row=0, column=0, sticky=NSEW)

        hlbl = ttk.Label(master=hdr_frame, text='Add New Credential', font=('Helvetica', 22, 'bold'))
        hlbl.pack(side=TOP, fill=X, padx=10, pady=10, anchor=CENTER)

        # Body Frame
        self.body_frame = ttk.Frame(self, padding=10)
        self.body_frame.grid(row=1, column=0, sticky=NSEW)

        lbl1 = ttk.Label(master=self.body_frame,text='Credential Type', font=('Helvetica', 16, 'bold'))
        lbl1.grid(row=0, column=0, sticky=NW)
        
        pass_choices = ['Email', 'Social Media', 'Phone Pin']
        self.pass_choices_description = ['Online Email Accounts like Gmail, Outlook, Yahoo, Proton Mail, etc', 'Online Accounts like Facebook, Twitter, Instagram, etc', 'Your Android or IPhone Pin']
        
        rb_group = ttk.Frame(self.body_frame, padding=10)
        rb_group.grid(row=1, column=0, sticky=NW)

        self.pass_choice = ttk.IntVar()

        choice1 = ttk.Radiobutton(rb_group, text=pass_choices[0], variable=self.pass_choice, value=0, command=self.handle_pass_choice, bootstyle="success-outline-toolbutton")
        choice1.pack(side=LEFT, expand=YES, padx=10)
        
        choice2 = ttk.Radiobutton(rb_group, text=pass_choices[1], variable=self.pass_choice, value=1, command=self.handle_pass_choice, bootstyle="success-outline-toolbutton")
        choice2.pack(side=LEFT, expand=YES, padx=10)

        choice3 = ttk.Radiobutton(rb_group, text=pass_choices[2], variable=self.pass_choice, value=2, command=self.handle_pass_choice, bootstyle="success-outline-toolbutton")
        choice3.pack(side=LEFT, expand=YES, padx=10)

        self.description_lbl = ttk.Label(self.body_frame, font=('Helventica', 12, 'bold'))
        self.description_lbl.grid(row=2, column=0, pady=15, sticky=NW)

        hdr = ttk.Label(self.body_frame, text='Credentials', font=('Helventica', 17, 'bold'))
        hdr.grid(row=3, column=0, sticky=NSEW)

        choice1.invoke()   
        self.wait_window()

    def kill_window(self):
        self.destroy()
        self.parent.refresh()

    def clear_creation_frame(self): # Removes all the Widgets in main
        if self.creation_frame != None:
            for widget in self.creation_frame.winfo_children():
                widget.destroy()
    
    def handle_pass_choice(self):
        choice = self.pass_choice.get()
        self.description_lbl.config(text = 'Description: \n' +  self.pass_choices_description[choice])

        self.clear_creation_frame()

        if choice == 0:
            self.creation_frame = Create_Email(self.body_frame, self.PM, self)
        elif choice==1:
            self.creation_frame = Create_Social_Media(self.body_frame, self.PM, self)
        elif choice==2:
            self.creation_frame = Create_Phone_Pin(self.body_frame, self.PM, self)
                
        self.creation_frame.grid(row=4, column=0, sticky=NSEW)