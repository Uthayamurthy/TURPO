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


class Password_Request_Window(ttk.Toplevel):
    def __init__(self, main, PATH, PM):
        self.main = main
        
        self.pm = PM

        icon = Image.open(PATH / 'assets' / 'key.png')

        self.images = [
            ImageTk.PhotoImage(
               icon,
               name='key'
            )
                ]
        super().__init__(master=main, title='Enter the Prime Key')
        super().geometry('550x400')

        self.grab_set()
        self.icon_lbl = ttk.Label(self, image='key')
        self.icon_lbl.pack(side='top', padx=10, pady=10)

        self.lbl = ttk.Label(self, text='Enter the Prime Key : ', font=('Helvetica', 15, 'bold'))
        self.lbl.pack(side='left', padx=10, pady=10)
        
        self.passfield = ttk.Entry(self, show='*', bootstyle='success')
        self.passfield.pack(side='left', padx=10, pady=10)
        
        self.submit = ttk.Button(self, text='Ok', command=self.validate, bootstyle='success-outline')
        self.submit.pack(side='bottom', padx=10, pady=10)

        self.bind('<Return>', self.validate)
        self.protocol("WM_DELETE_WINDOW", self.passwdless_warning)
        
        self.wait_window()

    def validate(self, event=None):
        passwd = self.passfield.get()
        valid = self.pm.check_cipher(passwd)
        if valid:
            self.destroy()
        else:
            self.invalid_passwd_msg_box()
            self.wm_transient()

    def invalid_passwd_msg_box(self):
        def close_all():
            toplevel.destroy()
            self.grab_set()
        self.grab_release()
        toplevel = ttk.Toplevel(self.main)
        toplevel.grab_set()
    
        toplevel.title("Invalid Password")
        x_position = 300
        y_position = 300
        toplevel.geometry(f"400x100+{x_position}+{y_position}")
    
        l1=ttk.Label(toplevel, image="::tk::icons::error")
        l1.grid(row=0, column=0, pady=(7, 0), padx=(10, 30), sticky="e")
        l2=ttk.Label(toplevel, text="Invalid Prime Key, please try again", font=('Helvetica', 12, 'bold'))
        l2.grid(row=0, column=1, columnspan=3, pady=(7, 10), sticky="w")
    
        b2 = ttk.Button(toplevel, text="Ok", command=close_all, width=10, bootstyle='danger-outline')
        b2.grid(row=1, column=1, padx=(2, 35), sticky="e")

    def passwdless_warning(self): # Give a warning to users if they close without entering the password.
        def close_all():
            toplevel2.destroy()
            self.destroy()

        if not self.pm.have_cipher():
            self.grab_release()
            toplevel2 = ttk.Toplevel(self.main)
            toplevel2.grab_set()
        
            toplevel2.title("Prime Key not Entered")
            x_position = 350
            y_position = 350
            toplevel2.geometry(f"750x100+{x_position}+{y_position}")
        
            l1=ttk.Label(toplevel2, image="::tk::icons::warning")
            l1.grid(row=0, column=0, pady=(7, 0), padx=(10, 30), sticky="e")
            l2=ttk.Label(toplevel2, text="You haven't entered the Prime Key, so you won't be able to view sensitive data.", font=('Helvetica', 12, 'bold'))
            l2.grid(row=0, column=1, columnspan=3, pady=(7, 10), sticky="w")
        
            b2 = ttk.Button(toplevel2, text="Ok, Got it", command=close_all, width=10, bootstyle='danger-outline')
            b2.grid(row=1, column=1, padx=(2, 35), sticky="e")