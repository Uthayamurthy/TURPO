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
from ttkbootstrap.constants import *
from tkinter import ttk as ltk
from ttkbootstrap.dialogs import dialogs
from PIL import Image, ImageTk
# Other Windows
from passwd_input import Password_Request_Window
from passwd_set import Password_Set_Window
from passwd_view import *
from add_credential import Add_Credential

# Misc for testing and debugging
from datetime import datetime


class Manage(ttk.Frame):
    def __init__(self, main, app, PATH, pm, sm):
        super().__init__(main)
        self.main = main
        self.app = app
        self.pass_verified = False
        self.PATH = PATH
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(2, weight=10)
        
        self.PM = pm
        self.SM = sm
        
        try:
            # Setting variables 
            self.autoprompt = bool(int(self.SM.retrieve('PM', 'autoPrompt')))
            self.lockinterval = int(self.SM.retrieve('PM', 'autoLockInterval'))
        except TypeError: # Occurs for a new settings file ... will be automatically fixed once the user goes to Settings Window, temporarily set default value here -> better fix in future.
            print('Encountered type error while trying to intialise the setting variables so setting default values.')
            self.autoprompt = False
            self.lockinterval = 0

        # Header
        hdr_frame = ttk.Frame(self, padding=10)
        hdr_frame.grid(row=0, column=0, sticky=NSEW)

        hlbl = ttk.Label(master=hdr_frame, text='Manage Your Passwords', font=('Helvetica', 22, 'bold'))
        hlbl.pack(side=TOP, fill=X, padx=10, pady=10, anchor=CENTER)
        
        # Utility Buttons Frame
        self.utility_frame = ttk.Frame(self, padding=10)
        self.utility_frame.grid(row=1, column=0, sticky=EW)
        
        new_button = ttk.Button(self.utility_frame, text='Add New', command=self.add_credential, bootstyle='success-outline')
        new_button.pack(side=RIGHT, padx=5)
        self.init()        

    def init(self, refresh=False):
        self.PM.read()
        tree_data = self.PM.get_tree_data()

        img1 = Image.open(self.PATH / 'assets' / 'email.png')
        img2 = Image.open(self.PATH / 'assets' / 'phone.png')
        img3 = Image.open(self.PATH / 'assets' / 'social-media.png')
        img4 = Image.open(self.PATH / 'assets' / 'padlock-lock.png')
        img5 = Image.open(self.PATH / 'assets' / 'padlock-unlock.png')

        self.images = [
            ImageTk.PhotoImage(
            img1,
            name='email'
            ),
            ImageTk.PhotoImage(
            img2,
            name='phone'
            ),
            ImageTk.PhotoImage(
            img3,
            name='social-media'
            ),
            ImageTk.PhotoImage(
            img4,
            name='lock'
            ),
            ImageTk.PhotoImage(
            img5,
            name='unlock'
            )
        ]

        self.file_init() # If new file -> prompt to set password.
        self.prime_button = ttk.Button(self.utility_frame, image='lock', command=self.prime_key, bootstyle='light')
        self.prime_button.pack(side=LEFT, padx=2)
        self.prime_lbl = ttk.Label(self.utility_frame, text='Locked', font=('Helventica', 15, 'bold'))
        self.prime_lbl.pack(side=LEFT)

        self.prime_init() # Prime Key related initialisation

        if tree_data == [] : # No data, password file is Empty !
            self.guidance_widget = ttk.Label(self, text = "You have not saved any credential yet ! Click on Add New button to add one ...", font=('Helventica', 16, 'bold'))
            self.guidance_widget.grid(row=2, column=0, sticky=N)
        else:

            style = ttk.Style(theme="litera")
            style.configure("Manage.Treeview.Heading", font=('Helventica', 16, 'bold'), background='#4582EC', foreground='#FFFFFF')
            style.configure("Manage.Treeview", font=('Helventica', 12, 'bold'), rowheight=40)

            # Tree 
            columns = ('#0','name','type','date')
            self.tree = ttk.Treeview(self, columns=columns, show='headings' , padding=[0, 0, 0, 0], bootstyle='primary', selectmode='browse', style='Manage.Treeview')
            self.tree.grid(row=2, column=0, sticky=NSEW)

            self.verscrlbar = ttk.Scrollbar(self, orient ="vertical", command = self.tree.yview, bootstyle='secondary-round')
            self.verscrlbar.grid(row=2, column=1, sticky=NS)

            self.tree.configure(yscrollcommand = self.verscrlbar.set)
            
            self.tree['show'] = ('headings', 'tree',)
            self.tree.column("#0", anchor=CENTER, width=20, stretch=True)
            self.tree.column('name', anchor=CENTER)
            self.tree.column('type', anchor=CENTER)
            self.tree.column('date', anchor=CENTER)

            # define headings
            self.tree.heading('name', text='Name')
            self.tree.heading('type', text='Type')
            self.tree.heading('date', text='Date Added')


            # Name in config : Name of icon
            img_type_mappings = {
                'Email':'email',
                'Social Media':'social-media',
                'Phone Pin':'phone'
            }
            
            for section in tree_data:
                self.tree.insert('', END, open=True, text=section[0],image=img_type_mappings[section[2]],values=section)

            self.tree.bind('<<TreeviewSelect>>', self.item_selected)      

        # Doesn't seem to serve any purpose -> Will be removed after testing ...
        # if not self.PM.have_cipher() and refresh :
        #     print('Prompt 1 - ', self.autoprompt)
        #     prw = Password_Request_Window(self.app, self.PATH, self.PM)
    

    def refresh(self):
        try:
            del self.images
            self.prime_button.destroy()
            self.prime_lbl.destroy()
            for item in self.tree.get_children():
                self.tree.delete(item)
            self.tree.destroy()
            self.verscrlbar.destroy()
        except:
            print('Encountered Attribute Error ... tree probably doesn\'t exist')
            
        # Rerun Init
        self.init(refresh=True)
    
    def item_selected(self, event):
        for selected_item in self.tree.selection():
            item = self.tree.item(selected_item)
            view_type = item['values'][2]
            if self.PM.have_cipher():
                if view_type == 'Email':
                    Email_View(self, self.app, self.PATH, self.PM, item['values'][1])
                elif view_type == 'Social Media':
                    Social_Media_View(self, self.app, self.PATH, self.PM, item['values'][1])
                if view_type == 'Phone Pin':
                    Phone_Pin_View(self, self.app, self.PATH, self.PM, item['values'][1])
            else:
                dialogs.Messagebox.show_error('Please Unlock before you can view any credential.')    


    def add_credential(self):
        if self.PM.have_cipher():
            Add_Credential(self, self.PATH, self.PM)
        else:
            dialogs.Messagebox.show_error('Please Unlock before you add a new creadential.')
    
    def autolock(self):
        print('Running Autolock ... ', )
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time) 
        self.PM.cipher_key = None # Forget the password
        try:
            self.prime_button['image'] = 'lock'
            self.prime_lbl['text'] = 'Locked'
        except:
            print('Skipping updating widgets as not in Manage Window ...')

    def file_init(self): # Request user to set password for a new data file
        if self.PM.new_file:
            psw = Password_Set_Window(self.app, self.PATH, self.PM)

    def prime_init(self):
        if self.PM.have_cipher() == False: # If prime key wasn't entered before
            if self.autoprompt:
                prw = Password_Request_Window(self.app, self.PATH, self.PM)
            if self.PM.have_cipher():# If Prime Key is entered after request
                self.prime_button['image'] = 'unlock'
                self.prime_lbl['text'] = 'Unlocked'
                if self.lockinterval != 0:
                    print('Scheduling auto lock (0) ...')
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    print("Current Time =", current_time)
                    self.after(self.lockinterval*60*1000, self.autolock) # Schedule AutoLock
            else: # If Prime Key isn't entered after request 
                self.prime_button['image'] = 'lock'
                self.prime_lbl['text'] = 'Locked'
        else: # If prime key is already entered
            self.prime_button['image'] = 'unlock'
            self.prime_lbl['text'] = 'Unlocked'

    def prime_key(self):
        if not self.PM.have_cipher(): # If Prime Key isn't already entered
            prw = Password_Request_Window(self.app, self.PATH, self.PM)
            if self.PM.have_cipher():# If Prime Key is entered after request
                self.prime_button['image'] = 'unlock'
                self.prime_lbl['text'] = 'Unlocked'
                if self.lockinterval != 0:
                    print('Scheduling auto lock (1) ...')
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    print("Current Time =", current_time)
                    self.after(self.lockinterval*60*1000, self.autolock) # Schedule AutoLock
            else: # If Prime Key isn't entered after request 
                self.prime_button['image'] = 'lock'
                self.prime_lbl['text'] = 'Locked'
        else:
            self.prime_button['image'] = 'lock'
            self.prime_lbl['text'] = 'Locked'
            self.PM.cipher_key = None # Forget the password