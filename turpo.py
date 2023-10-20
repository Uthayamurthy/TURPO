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
from PIL import Image, ImageTk
from modules.passwdmgr import PasswdMgr
from modules.settingsmgr import SettingsMgr
# Import Other Frames
from manage import Manage
from generate import Generate
from backup import Backup
from settings import Settings
from about import About

class TURPO(ttk.Frame):

    def __init__(self, main, PATH):
        super().__init__(main, bootstyle='Light')
        self.pack(fill=BOTH, expand=YES)

        self.app = main

        self.PATH = PATH

        self.current_window = 'home'

        self.setting_cats = ['PM', 'PG', 'PB', 'PT'] # Setting Categories 

        # Images

        logo = Image.open(PATH / 'assets' / 'logo.png')

        img1 = Image.open(PATH / 'assets' / 'manage.png')
        img2 = Image.open(PATH / 'assets' / 'generate.png')
        img3 = Image.open(PATH / 'assets' / 'backup.png')
        img4 = Image.open(PATH / 'assets' / 'settings.png')
        img5 = Image.open(PATH / 'assets' / 'about.png')

        self.images = [
            ImageTk.PhotoImage(
                logo.resize((64, 64)),
                name='logo',
            ),
            ImageTk.PhotoImage(
               img1,
               name='manage'
            ),
            ImageTk.PhotoImage(
               img2,
               name='generate'
            ),
            ImageTk.PhotoImage(
               img3,
               name='backup'
            ),
            ImageTk.PhotoImage(
               img4,
               name='settings'
            ),
            ImageTk.PhotoImage(
               img5,
               name='about'
            ),
        ]

        # Configure Rows and Columns

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=10)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)
        
        # Header
        hdr1_frame = ttk.Frame(self, padding=0, bootstyle=DARK)
        hdr1_frame.grid(row=0, column=0, sticky=NSEW)

        hdr2_frame = ttk.Frame(self, padding=0, bootstyle=DARK)
        hdr2_frame.grid(row=0, column=1, sticky=NSEW)
        

        hdr_label = ttk.Label(
            master=hdr1_frame,
            image='logo',
            bootstyle=(INVERSE, DARK)
        )
        hdr_label.pack(side=RIGHT)

        logo_text = ttk.Label(
            master=hdr2_frame,
            text='T.U.R.P.O',
            font=('Helventica', 30),
            bootstyle=(INVERSE, DARK)
        )
        logo_text.pack(side=LEFT, fill=BOTH, expand=True, padx=10)

        # Action Buttons

        action_frame = ttk.Frame(self, bootstyle=INFO)
        action_frame.grid(row=1, column=0, sticky=NSEW)

        manage_btn = ttk.Button(
            master=action_frame,
            image='manage',
            text='Manage Passwords',
            compound=TOP,
            bootstyle=INFO,
            command=self.on_manage
        )
        manage_btn.pack(side=TOP, fill=BOTH, ipadx=10, ipady=10)

        gen_btn = ttk.Button(
            master=action_frame,
            image='generate',
            text='Generate New Password',
            compound=TOP,
            bootstyle=INFO,
            command=self.on_generate
        )
        gen_btn.pack(side=TOP, fill=BOTH, ipadx=10, ipady=10)

        backup_btn = ttk.Button(
            master=action_frame,
            image='backup',
            text='Backup Your Passwords',
            compound=TOP,
            bootstyle=INFO,
            command=self.on_backup
        )
        backup_btn.pack(side=TOP, fill=BOTH, ipadx=10, ipady=10)

        settings_btn = ttk.Button(
            master=action_frame,
            image='settings',
            text='Settings',
            compound=TOP,
            bootstyle=INFO,
            command=self.on_settings
        )
        settings_btn.pack(side=TOP, fill=BOTH, ipadx=10, ipady=10)

        about_btn = ttk.Button(
            master=action_frame,
            image='about',
            text='About',
            compound=TOP,
            bootstyle=INFO,
            command=self.on_about
        )
        about_btn.pack(side=TOP, fill=BOTH, ipadx=10, ipady=10)


        # # Main Frame
        self.main_frame = ttk.Frame(self, bootstyle=LIGHT)
        self.main_frame.grid(row=1, column=1, sticky=NSEW)


        # Home Page Development - Reserved for later versions.
        # lblh = ttk.Label(self.main_frame, text='Home Page Stuff', font=('Helventica', 22, 'bold'))
        # lblh.pack(fill=BOTH)
        
        self.PM = PasswdMgr(PATH / 'data', 'pwfile')
        self.PM.read()
        self.SM = SettingsMgr('settings.db', PATH / 'settings', self.setting_cats)
        manage_btn.invoke() # Start Manage Screen

    def clear_main_frame(self): # Removes all the Widgets in main
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def on_manage(self):
        if self.current_window != 'manage':
            self.clear_main_frame()
            self.main_frame = Manage(self, self.app, self.PATH, self.PM, self.SM)
            self.main_frame.grid(row=1, column=1, sticky=NSEW)
            self.current_window = 'manage'
    
    def on_generate(self):
        if self.current_window != 'generate':
            self.clear_main_frame()
            self.main_frame = Generate(self, self.PATH)
            self.main_frame.grid(row=1, column=1, columnspan=3, sticky=NSEW)
            self.current_window = 'generate'

    def on_backup(self):
        if self.current_window != 'backup':
            self.clear_main_frame()
            self.main_frame = Backup(self, self.PM)
            self.main_frame.grid(row=1, column=1, sticky=NSEW)
            self.current_window = 'backup'

    def on_about(self):
        if self.current_window != 'about':
            self.clear_main_frame()
            self.main_frame = About(self, self.PATH)
            self.main_frame.grid(row=1, column=1, sticky=NSEW)
            self.current_window = 'about'

    def on_settings(self):
        if self.current_window != 'settings':
            self.clear_main_frame()
            self.main_frame = Settings(self, self.app, self.PATH, self.PM, self.SM)
            self.main_frame.grid(row=1, column=1, sticky=NSEW)
            self.current_window = 'settings'