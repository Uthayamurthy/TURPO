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

# Contains the window to input password.

import ttkbootstrap as ttk
from ttkbootstrap import dialogs
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from ttkbootstrap.tooltip import ToolTip

class Password_Set_Window(ttk.Toplevel):
    def __init__(self, main, PATH, pm):
        self.main = main
        
        self.PM = pm

        icon = Image.open(PATH / 'assets' / 'key.png')

        self.images = [
            ImageTk.PhotoImage(
               icon,
               name='key'
            )
                ]
        super().__init__(master=main, title='Set your Prime Key')
        super().geometry('550x400')

        self.grab_set()
        
        self.info_lbl = ttk.Label(self, text='Welcome to TURPO !', font=('Helvetica', 16, 'bold'), bootstyle='info')
        self.info_lbl.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.icon_lbl = ttk.Label(self, image='key')
        self.icon_lbl.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        
        self.info_lbl = ttk.Label(self, text='Looks like you haven\'t set a Prime Key yet. \nSo, just setup one ...', font=('Helvetica', 11, 'bold'), bootstyle='secondary')
        self.info_lbl.grid(row=2, column=0, columnspan=2, padx=5, pady=10)
        
        self.lbl = ttk.Label(self, text='Enter the Prime Key : ', font=('Helvetica', 15, 'bold'))
        self.lbl.grid(row=3, column=0, padx=10, pady=10)
        
        self.passfield = ttk.Entry(self, show='*', bootstyle='success')
        self.passfield.grid(row=3, column=1, padx=10, pady=10)
        
        ToolTip(self.passfield, 'Keep it secure and Never Ever Forget it !!')

        self.submit = ttk.Button(self, text='Ok', command=self.set_password, bootstyle='success-outline')
        self.submit.grid(row=4, column=1, padx=10, pady=10)

        self.bind('<Return>', self.set_password)
        self.protocol("WM_DELETE_WINDOW", self.passwdless_warning)
        
        self.wait_window()

    def set_password(self, event=None):
        passwd = self.passfield.get()
        if passwd != None and not passwd.isspace():
            self.PM.init_pwfile(passwd)
            dialogs.Messagebox.show_info(message='Prime Key Set Successfully !', title='Prime Key Set !')
            self.destroy()
        else:
            dialogs.Messagebox.show_warning(message='Prime Key Cannot be Empty !', title='Warning !!')

    def passwdless_warning(self): # Give a warning to users if they close without setting the password.
        def close_all():
            toplevel2.destroy()
            self.destroy()

        if not self.PM.have_cipher():
            self.grab_release()
            toplevel2 = ttk.Toplevel(self.main)
            toplevel2.grab_set()
        
            toplevel2.title("Prime Key not Entered")
            x_position = 350
            y_position = 350
            toplevel2.geometry(f"750x100+{x_position}+{y_position}")
        
            l1=ttk.Label(toplevel2, image="::tk::icons::warning")
            l1.grid(row=0, column=0, pady=(7, 0), padx=(10, 30), sticky="e")
            l2=ttk.Label(toplevel2, text="You haven't set a Prime Key, so you won't be able to save any data.", font=('Helvetica', 12, 'bold'))
            l2.grid(row=0, column=1, columnspan=3, pady=(7, 10), sticky="w")
        
            b2 = ttk.Button(toplevel2, text="Ok, Got it", command=close_all, width=10, bootstyle='danger-outline')
            b2.grid(row=1, column=1, padx=(2, 35), sticky="e")