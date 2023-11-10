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

class Passwd_View(ttk.Toplevel):
    def __init__(self, field_type, parent, app, PATH, PM, section):
        self.PM = PM
        self.parent = parent
        self.app = app
        self.field_type = field_type # For now ... Can be "email", "social" or "phone"

        self.data = self.PM.pw[section]
        self.path = PATH

        email_icon = Image.open(self.path / 'assets' / 'email_big.png')
        social_icon = Image.open(self.path / 'assets' / 'social-media_big.png')
        phone_icon =  Image.open(self.path / 'assets' / 'phone_big.png')

        self.images = [
            ImageTk.PhotoImage(email_icon, name='email_big'),
            ImageTk.PhotoImage(social_icon, name='social_big'),
            ImageTk.PhotoImage(phone_icon, name='phone_big'),
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

        self.init()

    def init(self):
        # Header
        hdr1_frame = ttk.Frame(self, padding=0, bootstyle=DARK)
        hdr1_frame.grid(row=0, column=0, sticky=NSEW)

        hdr2_frame = ttk.Frame(self, padding=0, bootstyle=DARK)
        hdr2_frame.grid(row=0, column=1, sticky=NSEW)

        hdr_label = ttk.Label(
            master=hdr1_frame,
            image=self.field_type+'_big',
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

        self.body_frame = ttk.Frame(self, padding=10)
        self.body_frame.grid(row=1, column=1, pady=40, sticky=NSEW)

        mode_frame = ttk.Frame(self.body_frame, padding=0, bootstyle=DARK)
        mode_frame.grid(row=0, column=0, columnspan=3, padx=5, pady=20, sticky=NSEW)

        mode_lbl = ttk.Label(mode_frame, text='Current Mode : ', font=('Helventica', 14, 'bold'), bootstyle=(INVERSE, DARK))
        mode_lbl.pack(side=LEFT, padx=10, pady=5)

        mode = ttk.Label(mode_frame, textvariable=self.mode_var, font=('Helventica', 14, 'bold'), bootstyle=(INVERSE, DARK))
        mode.pack(side=LEFT, padx=10, pady=5)

        self.delete = ttk.Button(mode_frame, text='Delete', bootstyle='danger', command=self.delete_credentials)
        self.delete.pack(side=RIGHT, padx=10, pady=5)

        self.mode_btn = ttk.Button(mode_frame, text='Edit', bootstyle='info', command=self.change_mode)
        self.mode_btn.pack(side=RIGHT, padx=10, pady=5)

        if self.field_type == 'email': self.email_field()
        if self.field_type == 'social': self.social_field()
        if self.field_type == 'phone': self.phone_field()

        self.footer_frame = ttk.Frame(self)
        self.footer_frame.grid(row=2, column=1, padx=5, pady=10, sticky=NE)

        self.save_btn = ttk.Button(self.footer_frame, text='Save', bootstyle='outline-success', command=self.save_credentials)
        self.save_btn.grid(row=0, column=0, padx=15, pady=10, sticky=NE)
        self.save_btn["state"] = "disabled"

        self.wait_window()

    def email_field(self):
        
        uname_lbl = ttk.Label(self.body_frame, text='Username : ', font=('Helventica', 15, 'bold'))
        uname_lbl.grid(row=1, column=0, padx=5, pady=20, sticky=NSEW)

        self.uname_entry = CopyEntry(self.body_frame, self.path, self.PM.cipher.decrypt(self.data['username']))
        self.uname_entry.grid(row=1, column=1, padx=5, pady=20, sticky=NSEW)

        email_lbl = ttk.Label(self.body_frame, text='Email : ', font=('Helventica', 15, 'bold'))
        email_lbl.grid(row=2, column=0, padx=5, pady=20, sticky=NSEW)

        self.email_entry = CopyEntry(self.body_frame, self.path, self.PM.cipher.decrypt(self.data['email']))
        self.email_entry.grid(row=2, column=1, padx=5, pady=20, sticky=NSEW)

        password_lbl = ttk.Label(self.body_frame, text='Password : ', font=('Helventica', 15, 'bold'))
        password_lbl.grid(row=3, column=0, padx=5, pady=20, sticky=NSEW)

        self.password_entry = CopyEntry(self.body_frame, self.path, self.PM.cipher.decrypt(self.data['password']))
        self.password_entry.grid(row=3, column=1, padx=5, pady=20, sticky=NSEW)

        date_lbl = ttk.Label(self.body_frame, text='Date of Modification : ', font=('Helventica', 15, 'bold'))
        date_lbl.grid(row=4, column=0, padx=5, pady=20, sticky=NSEW)

        date_display = ttk.Label(self.body_frame, text=self.data['date'], font=('Helventica', 15, 'bold'))
        date_display.grid(row=4, column=1, padx=5, pady=20, sticky=NSEW)

        self.fields = {'username':self.uname_entry, 'email':self.email_entry, 'password':self.password_entry}

    def social_field(self):
        uname_lbl = ttk.Label(self.body_frame, text='Username : ', font=('Helventica', 15, 'bold'))
        uname_lbl.grid(row=1, column=0, padx=5, pady=20, sticky=NSEW)

        self.uname_entry = CopyEntry(self.body_frame, self.path, self.PM.cipher.decrypt(self.data['username']))
        self.uname_entry.grid(row=1, column=1, padx=5, pady=20, sticky=NSEW)

        password_lbl = ttk.Label(self.body_frame, text='Password : ', font=('Helventica', 15, 'bold'))
        password_lbl.grid(row=2, column=0, padx=5, pady=20, sticky=NSEW)

        self.password_entry = CopyEntry(self.body_frame, self.path, self.PM.cipher.decrypt(self.data['password']))
        self.password_entry.grid(row=2, column=1, padx=5, pady=20, sticky=NSEW)

        date_lbl = ttk.Label(self.body_frame, text='Date of Modification : ', font=('Helventica', 15, 'bold'))
        date_lbl.grid(row=3, column=0, padx=5, pady=20, sticky=NSEW)

        date_display = ttk.Label(self.body_frame, text=self.data['date'], font=('Helventica', 15, 'bold'))
        date_display.grid(row=3, column=1, padx=5, pady=20, sticky=NSEW)

        self.fields = {'username':self.uname_entry, 'password':self.password_entry}
    
    def phone_field(self):

        pin_lbl = ttk.Label(self.body_frame, text='Pin : ', font=('Helventica', 15, 'bold'))
        pin_lbl.grid(row=1, column=0, padx=5, pady=20, sticky=NSEW)

        self.pin_entry = CopyEntry(self.body_frame, self.path, self.PM.cipher.decrypt(self.data['pin']))
        self.pin_entry.grid(row=1, column=1, padx=5, pady=20, sticky=NSEW)

        date_lbl = ttk.Label(self.body_frame, text='Date of Modification : ', font=('Helventica', 15, 'bold'))
        date_lbl.grid(row=2, column=0, padx=5, pady=20, sticky=NSEW)

        date_display = ttk.Label(self.body_frame, text=self.data['date'], font=('Helventica', 15, 'bold'))
        date_display.grid(row=2, column=1, padx=5, pady=20, sticky=NSEW)

        self.fields = {'pin':self.pin_entry}

    def change_mode(self):
        if self.mode_var.get() == 'Read': # If current mode is read, change it to edit mode
            self.mode_var.set('Edit')
            self.mode_btn['text'] = 'Read'
            self.save_btn["state"] = "normal"
            for field in self.fields.values():
                field.enable_entry()
        else:
            self.mode_var.set('Read')
            self.mode_btn['text'] = 'Edit'
            self.save_btn["state"] = "disabled"
            for field in self.fields.values():
                field.disable_entry()

    def save_credentials(self):
        for field_name, field in self.fields.items():
            self.PM.set_secret(self.section, field_name, field.get())
        self.PM.write()
        self.change_mode()
    
    def delete_credentials(self):
        choice = dialogs.Messagebox.show_question('Are you sure you want to delete the credentials ?', parent=self, buttons=['No:Secondary', 'Yes:Danger'])
        if choice == 'Yes':
            self.PM.remove_section(self.section)
            self.PM.write()
            self.parent.refresh()
            self.destroy()
            
        self.wait_window()        