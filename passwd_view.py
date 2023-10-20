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
# from passwd_input import Password_Request_Window
from modules.widgets import CopyEntry

class Email_View(ttk.Toplevel):
    def __init__(self, parent, app, PATH, PM, section):

        self.PM = PM
        self.parent = parent
        self.app = app

        data = self.PM.pw[section]

        icon = Image.open(PATH / 'assets' / 'email_big.png')

        self.images = [
            ImageTk.PhotoImage(
               icon,
               name='icon'
            )
                ]
        
        self.section = section
        
        self.mode_var = ttk.StringVar()
        self.mode_var.set('Read')
        
        t = self.section + '\'s credentials'
        
        super().__init__(title=t)
        super().geometry('1000x700')
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=5)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=5)

        # if not self.PM.have_cipher():
        #     prw = Password_Request_Window(self.app, PATH, self.PM)
        #     if not self.PM.have_cipher():
        #         self.destroy()

        # Header
        hdr1_frame = ttk.Frame(self, padding=0, bootstyle=DARK)
        hdr1_frame.grid(row=0, column=0, sticky=NSEW)

        hdr2_frame = ttk.Frame(self, padding=0, bootstyle=DARK)
        hdr2_frame.grid(row=0, column=1, sticky=NSEW)

        hdr_label = ttk.Label(
            master=hdr1_frame,
            image='icon',
            bootstyle=(INVERSE, DARK)
        )
        hdr_label.pack(side=RIGHT)

        logo_text = ttk.Label(
            master=hdr2_frame,
            text=self.section,
            font=('Helventica', 30),
            bootstyle=(INVERSE, DARK)
        )

        logo_text.pack(side=TOP, fill=BOTH, expand=True, padx=10)

        body_frame = ttk.Frame(self, padding=10)
        body_frame.grid(row=1, column=1, pady=40, sticky=NSEW)

        mode_frame = ttk.Frame(body_frame, padding=0, bootstyle=DARK)
        mode_frame.grid(row=0, column=0, columnspan=3, padx=5, pady=20, sticky=NSEW)

        mode_lbl = ttk.Label(mode_frame, text='Current Mode : ', font=('Helventica', 14, 'bold'), bootstyle=(INVERSE, DARK))
        mode_lbl.pack(side=LEFT, padx=10, pady=5)

        mode = ttk.Label(mode_frame, textvariable=self.mode_var, font=('Helventica', 14, 'bold'), bootstyle=(INVERSE, DARK))
        mode.pack(side=LEFT, padx=10, pady=5)

        self.delete = ttk.Button(mode_frame, text='Delete', bootstyle='danger', command=self.delete_credentials)
        self.delete.pack(side=RIGHT, padx=10, pady=5)

        self.mode_btn = ttk.Button(mode_frame, text='Edit', bootstyle='info', command=self.change_mode)
        self.mode_btn.pack(side=RIGHT, padx=10, pady=5)

        uname_lbl = ttk.Label(body_frame, text='Username : ', font=('Helventica', 15, 'bold'))
        uname_lbl.grid(row=1, column=0, padx=5, pady=20, sticky=NSEW)

        self.uname_entry = CopyEntry(body_frame, PATH, self.PM.cipher.decrypt(data['username']))
        self.uname_entry.grid(row=1, column=1, padx=5, pady=20, sticky=NSEW)

        email_lbl = ttk.Label(body_frame, text='Email : ', font=('Helventica', 15, 'bold'))
        email_lbl.grid(row=2, column=0, padx=5, pady=20, sticky=NSEW)

        self.email_entry = CopyEntry(body_frame, PATH, self.PM.cipher.decrypt(data['email']))
        self.email_entry.grid(row=2, column=1, padx=5, pady=20, sticky=NSEW)

        password_lbl = ttk.Label(body_frame, text='Password : ', font=('Helventica', 15, 'bold'))
        password_lbl.grid(row=3, column=0, padx=5, pady=20, sticky=NSEW)

        self.password_entry = CopyEntry(body_frame, PATH, self.PM.cipher.decrypt(data['password']))
        self.password_entry.grid(row=3, column=1, padx=5, pady=20, sticky=NSEW)

        date_lbl = ttk.Label(body_frame, text='Date of Modification : ', font=('Helventica', 15, 'bold'))
        date_lbl.grid(row=4, column=0, padx=5, pady=20, sticky=NSEW)

        date_display = ttk.Label(body_frame, text=data['date'], font=('Helventica', 15, 'bold'))
        date_display.grid(row=4, column=1, padx=5, pady=20, sticky=NSEW)

        self.save_btn = ttk.Button(body_frame, text='Save', bootstyle='outline-success', command=self.save_credentials)
        self.save_btn.grid(row=5, column=2, padx=5, pady=20, sticky=NSEW)
        self.save_btn["state"] = "disabled"

        self.wait_window()

    def change_mode(self):
        if self.mode_var.get() == 'Read': # If current mode is read, change it to edit mode
            self.mode_var.set('Edit')
            self.mode_btn['text'] = 'Read'
            self.save_btn["state"] = "normal"
            self.uname_entry.enable_entry()
            self.email_entry.enable_entry()
            self.password_entry.enable_entry()
        else:
            self.mode_var.set('Read')
            self.mode_btn['text'] = 'Edit'
            self.save_btn["state"] = "disabled"
            self.uname_entry.disable_entry()
            self.email_entry.disable_entry()
            self.password_entry.disable_entry()

    def save_credentials(self):
        self.PM.set_secret(self.section, 'username', self.uname_entry.get())
        self.PM.set_secret(self.section, 'email', self.email_entry.get())
        self.PM.set_secret(self.section, 'password', self.password_entry.get())
        self.PM.write()
        self.change_mode()
    
    def delete_credentials(self):
        choice = dialogs.Messagebox.show_question('Are you sure you want to delete the credentials ?', parent=self, buttons=['No:Secondary', 'Yes:Danger'])
        if choice == 'Yes':
            print(self.parent)
            self.PM.remove_section(self.section)
            self.PM.write()
            self.parent.refresh()
            self.destroy()
            
        self.wait_window()
        

class Social_Media_View(ttk.Toplevel):
    def __init__(self, parent, app, PATH, PM, section):

        self.parent = parent
        self.PM = PM
        self.app = app

        data = self.PM.pw[section]

        icon = Image.open(PATH / 'assets' / 'social-media_big.png')

        self.images = [
            ImageTk.PhotoImage(
               icon,
               name='icon'
            )
                ]
        
        self.section = section
        
        self.mode_var = ttk.StringVar()
        self.mode_var.set('Read')
        
        t = self.section + '\'s credentials'
        
        super().__init__(title=t)
        super().geometry('1000x700')
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=5)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=5)

        # if not self.PM.have_cipher():
        #     prw = Password_Request_Window(self.app, PATH, self.PM)
        #     if not self.PM.have_cipher():
        #         self.destroy()

        # Header
        hdr1_frame = ttk.Frame(self, padding=0, bootstyle=DARK)
        hdr1_frame.grid(row=0, column=0, sticky=NSEW)

        hdr2_frame = ttk.Frame(self, padding=0, bootstyle=DARK)
        hdr2_frame.grid(row=0, column=1, sticky=NSEW)

        hdr_label = ttk.Label(
            master=hdr1_frame,
            image=self.images[0],
            bootstyle=(INVERSE, DARK)
        )
        hdr_label.pack(side=RIGHT)

        logo_text = ttk.Label(
            master=hdr2_frame,
            text=self.section,
            font=('Helventica', 30),
            bootstyle=(INVERSE, DARK)
        )

        logo_text.pack(side=TOP, fill=BOTH, expand=True, padx=10)

        body_frame = ttk.Frame(self, padding=10)
        body_frame.grid(row=1, column=1, pady=40, sticky=NSEW)

        mode_frame = ttk.Frame(body_frame, padding=0, bootstyle=DARK)
        mode_frame.grid(row=0, column=0, columnspan=3, padx=5, pady=20, sticky=NSEW)

        mode_lbl = ttk.Label(mode_frame, text='Current Mode : ', font=('Helventica', 14, 'bold'), bootstyle=(INVERSE, DARK))
        mode_lbl.pack(side=LEFT, padx=10, pady=5)

        mode = ttk.Label(mode_frame, textvariable=self.mode_var, font=('Helventica', 14, 'bold'), bootstyle=(INVERSE, DARK))
        mode.pack(side=LEFT, padx=10, pady=5)

        self.delete = ttk.Button(mode_frame, text='Delete', bootstyle='danger', command=self.delete_credentials)
        self.delete.pack(side=RIGHT, padx=10, pady=5)

        self.mode_btn = ttk.Button(mode_frame, text='Edit', bootstyle='info', command=self.change_mode)
        self.mode_btn.pack(side=RIGHT, padx=10, pady=5)


        uname_lbl = ttk.Label(body_frame, text='Username : ', font=('Helventica', 15, 'bold'))
        uname_lbl.grid(row=1, column=0, padx=5, pady=20, sticky=NSEW)

        self.uname_entry = CopyEntry(body_frame, PATH, self.PM.cipher.decrypt(data['username']))
        self.uname_entry.grid(row=1, column=1, padx=5, pady=20, sticky=NSEW)

        password_lbl = ttk.Label(body_frame, text='Password : ', font=('Helventica', 15, 'bold'))
        password_lbl.grid(row=2, column=0, padx=5, pady=20, sticky=NSEW)

        self.password_entry = CopyEntry(body_frame, PATH, self.PM.cipher.decrypt(data['password']))
        self.password_entry.grid(row=2, column=1, padx=5, pady=20, sticky=NSEW)

        date_lbl = ttk.Label(body_frame, text='Date of Modification : ', font=('Helventica', 15, 'bold'))
        date_lbl.grid(row=3, column=0, padx=5, pady=20, sticky=NSEW)

        date_display = ttk.Label(body_frame, text=data['date'], font=('Helventica', 15, 'bold'))
        date_display.grid(row=3, column=1, padx=5, pady=20, sticky=NSEW)

        self.save_btn = ttk.Button(body_frame, text='Save', bootstyle='outline-success', command=self.save_credentials)
        self.save_btn.grid(row=4, column=2, padx=5, pady=20, sticky=NSEW)
        
        self.save_btn["state"] = "disabled"

        self.wait_window()

    def change_mode(self):
        if self.mode_var.get() == 'Read': # If current mode is read, change it to edit mode
            self.mode_var.set('Edit')
            self.mode_btn['text'] = 'Read'
            self.save_btn["state"] = "normal"
            self.uname_entry.enable_entry()
            self.password_entry.enable_entry()
        else:
            self.mode_var.set('Read')
            self.mode_btn['text'] = 'Edit'
            self.save_btn["state"] = "disabled"
            self.uname_entry.disable_entry()
            self.password_entry.disable_entry()

    def save_credentials(self):
        self.PM.set_secret(self.section, 'username', self.uname_entry.get())
        self.PM.set_secret(self.section, 'password', self.password_entry.get())
        self.PM.write()
        self.change_mode()
    
    def delete_credentials(self):
        choice = dialogs.Messagebox.show_question('Are you sure you want to delete the credentials ?', parent=self, buttons=['No:Secondary', 'Yes:Danger'])
        if choice == 'Yes':
            print(self.parent)
            self.PM.remove_section(self.section)
            self.PM.write()
            self.parent.refresh()
            self.destroy()
            
        self.wait_window()

class Phone_Pin_View(ttk.Toplevel):
    def __init__(self, parent, app, PATH, PM, section):
        
        self.parent = parent
        self.PM = PM
        self.app = app

        data = self.PM.pw[section]

        icon = Image.open(PATH / 'assets' / 'phone_big.png')

        self.images = [
            ImageTk.PhotoImage(
               icon,
               name='icon'
            )
                ]
        
        self.section = section
        
        self.mode_var = ttk.StringVar()
        self.mode_var.set('Read')
        
        t = self.section + '\'s credentials'
        
        super().__init__(title=t)
        super().geometry('1000x500')
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=5)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=5)

        # if not self.PM.have_cipher():
        #     prw = Password_Request_Window(self.app, PATH, self.PM)
        #     if not self.PM.have_cipher():
        #         self.destroy()

        # Header
        hdr1_frame = ttk.Frame(self, padding=0, bootstyle=DARK)
        hdr1_frame.grid(row=0, column=0, sticky=NSEW)

        hdr2_frame = ttk.Frame(self, padding=0, bootstyle=DARK)
        hdr2_frame.grid(row=0, column=1, sticky=NSEW)

        hdr_label = ttk.Label(
            master=hdr1_frame,
            image='icon',
            bootstyle=(INVERSE, DARK)
        )
        hdr_label.pack(side=RIGHT)

        logo_text = ttk.Label(
            master=hdr2_frame,
            text=self.section,
            font=('Helventica', 30),
            bootstyle=(INVERSE, DARK)
        )

        logo_text.pack(side=TOP, fill=BOTH, expand=True, padx=10)

        body_frame = ttk.Frame(self, padding=10)
        body_frame.grid(row=1, column=1, pady=40, sticky=NSEW)

        mode_frame = ttk.Frame(body_frame, padding=0, bootstyle=DARK)
        mode_frame.grid(row=0, column=0, columnspan=3, padx=5, pady=20, sticky=NSEW)

        mode_lbl = ttk.Label(mode_frame, text='Current Mode : ', font=('Helventica', 14, 'bold'), bootstyle=(INVERSE, DARK))
        mode_lbl.pack(side=LEFT, padx=10, pady=5)

        mode = ttk.Label(mode_frame, textvariable=self.mode_var, font=('Helventica', 14, 'bold'), bootstyle=(INVERSE, DARK))
        mode.pack(side=LEFT, padx=10, pady=5)

        self.delete = ttk.Button(mode_frame, text='Delete', bootstyle='danger', command=self.delete_credentials)
        self.delete.pack(side=RIGHT, padx=10, pady=5)

        self.mode_btn = ttk.Button(mode_frame, text='Edit', bootstyle='info', command=self.change_mode)
        self.mode_btn.pack(side=RIGHT, padx=10, pady=5)

        pin_lbl = ttk.Label(body_frame, text='Pin : ', font=('Helventica', 15, 'bold'))
        pin_lbl.grid(row=2, column=0, padx=5, pady=20, sticky=NSEW)

        self.pin_entry = CopyEntry(body_frame, PATH, self.PM.cipher.decrypt(data['pin']))
        self.pin_entry.grid(row=2, column=1, padx=5, pady=20, sticky=NSEW)

        date_lbl = ttk.Label(body_frame, text='Date of Modification : ', font=('Helventica', 15, 'bold'))
        date_lbl.grid(row=3, column=0, padx=5, pady=20, sticky=NSEW)

        date_display = ttk.Label(body_frame, text=data['date'], font=('Helventica', 15, 'bold'))
        date_display.grid(row=3, column=1, padx=5, pady=20, sticky=NSEW)

        self.save_btn = ttk.Button(body_frame, text='Save', bootstyle='outline-success', command=self.save_credentials)
        self.save_btn.grid(row=4, column=2, padx=5, pady=20, sticky=NSEW)
        
        self.save_btn["state"] = "disabled"

        self.wait_window()

    def change_mode(self):
        if self.mode_var.get() == 'Read': # If current mode is read, change it to edit mode
            self.mode_var.set('Edit')
            self.mode_btn['text'] = 'Read'
            self.save_btn["state"] = "normal"
            self.pin_entry.enable_entry()
        else:
            self.mode_var.set('Read')
            self.mode_btn['text'] = 'Edit'
            self.save_btn["state"] = "disabled"
            self.pin_entry.disable_entry()

    def save_credentials(self):
        self.PM.set_secret(self.section, 'pin', self.pin_entry.get())
        self.PM.write()
        self.change_mode()
    
    def delete_credentials(self):
        choice = dialogs.Messagebox.show_question('Are you sure you want to delete the credentials ?', parent=self, buttons=['No:Secondary', 'Yes:Danger'])
        if choice == 'Yes':
            print(self.parent)
            self.PM.remove_section(self.section)
            self.PM.write()
            self.parent.refresh()
            self.destroy()
        self.wait_window() 
        