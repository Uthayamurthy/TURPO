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
from pathlib import Path
from ttkbootstrap.tooltip import ToolTip

class Passwd_Change(ttk.Toplevel):
    def __init__(self, parent, app, PATH, PM):
        self.PM = PM
        self.parent = parent
        self.app = app
        self.PATH = PATH

        super().__init__(master=app, title='Prime Key Change Tool')
        super().geometry('650x400')

        self.grab_set()

        self.heading_label = ttk.Label(self, text='Change Your Prime Key', font=('Helvetica', 18, 'bold'))
        self.heading_label.pack(side='top', padx=10, pady=15)

        self.warning = ttk.Label(self, text = 'Warning : Change is immediate, Don\'t Forget the new key !', bootstyle='danger', font=('Helvetica', 12, 'bold'))
        self.warning.pack(side='top', padx=10, pady=10, fill=BOTH)

        body_frame = ttk.Frame(self)
        body_frame.pack(side='top', padx=10, pady=10, fill=BOTH)

        lbl1 = ttk.Label(body_frame, text='Current Prime Key :', font=('Helvetica', 13, 'bold'))
        lbl1.grid(row=0, column=0, padx=5, pady=5, sticky=NSEW)

        self.old_key = ttk.StringVar()

        old_entry = ttk.Entry(body_frame, textvariable=self.old_key, show='*', width=30, justify=CENTER)
        old_entry.grid(row=0, column=1, padx=5, pady=5, sticky=NSEW)

        lbl2 = ttk.Label(body_frame, text='New Prime Key :', font=('Helvetica', 13, 'bold'))
        lbl2.grid(row=1, column=0, padx=5, pady=5, sticky=NSEW)

        self.new_key = ttk.StringVar()

        new_entry = ttk.Entry(body_frame, textvariable=self.new_key, width=30, justify=CENTER)
        new_entry.grid(row=1, column=1, padx=5, pady=5, sticky=NSEW)

        change_btn = ttk.Button(self, text='Change', bootstyle='primary', command=self.change_key)
        change_btn.pack(side='top', padx=10, pady=15)

    def change_key(self):
        old_key = self.old_key.get()
        new_key = self.new_key.get()

        try:
            if len(old_key):
                if len(new_key):
                    stat = self.PM.change_prime_key(old_key, new_key)
                    if stat:
                        dialogs.Messagebox.show_info(parent=self, message='Prime Key Changed Successful !')
                        self.destroy()
                    else:
                        dialogs.Messagebox.show_error(parent=self, message='Password Change Failed ! Check Your Current Prime Key !')

                else:
                    dialogs.Messagebox.show_error(parent=self, message='Please Enter the New Prime Key')
            else:
                dialogs.Messagebox.show_error(parent=self, message='Please Enter the Current Prime Key')
        except:
            dialogs.Messagebox.show_error(parent=self, message='Password Change Failed !')
