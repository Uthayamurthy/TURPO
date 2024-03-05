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
from tkinter.filedialog import askopenfilename
from pathlib import Path
from ttkbootstrap.tooltip import ToolTip

class Passwd_Restore(ttk.Toplevel):
    def __init__(self, parent, app, PATH, PM):
        self.PM = PM
        self.parent = parent
        self.app = app
        self.PATH = PATH

        icon = Image.open(PATH / 'assets' / 'restore.png')

        self.images = [
            ImageTk.PhotoImage(
               icon,
               name='restore'
            )
                ]
        
        super().__init__(master=app, title='Credentials Restore Tool')
        super().geometry('650x600')

        self.grab_set()

        self.heading_label = ttk.Label(self, text='Restore Your Credentials', font=('Helvetica', 18, 'bold'))
        self.heading_label.pack(side='top', padx=10, pady=10)
        self.icon_lbl = ttk.Label(self, image='restore')
        self.icon_lbl.pack(side='top', padx=10, pady=10)
        
        self.warning = ttk.Label(self, text = 'Warning : Your Current Credentials will be Replaced !', bootstyle='danger', font=('Helvetica', 12, 'bold'))
        self.warning.pack(side='top', padx=10, pady=10, fill=BOTH)
        
        body_frame = ttk.Frame(self)
        body_frame.pack(side='top', padx=10, pady=10, fill=BOTH)

        lbl1 = ttk.Label(body_frame, text='Backup File Type :', font=('Helvetica', 13, 'bold'))
        lbl1.grid(row=0, column=0, sticky=NSEW)

        self.type_choice = ttk.IntVar()

        rb_group = ttk.Frame(body_frame, padding=10)
        rb_group.grid(row=0, column=1, sticky=NW)

        choice1 = ttk.Radiobutton(rb_group, text='Encrypted', variable=self.type_choice, command=self.disable_passwd_field, value=0, bootstyle="success-outline-toolbutton")
        choice1.pack(side=LEFT, expand=YES, padx=10)
        
        choice2 = ttk.Radiobutton(rb_group, text='Unencrypted', variable=self.type_choice, command=self.enable_passwd_field, value=1, bootstyle="success-outline-toolbutton")
        choice2.pack(side=LEFT, expand=YES, padx=10)

        self.path_var = ttk.StringVar()
        self.path_var.set('No File Selected !')

        lbl2 = ttk.Label(body_frame, text='File Path :', font=('Helvetica', 13, 'bold'))
        lbl2.grid(row=1, column=0, padx=5, pady=5, sticky=NSEW)

        path_txt = ttk.Entry(body_frame, textvariable=self.path_var, width=40, justify=CENTER)
        path_txt.grid(row=1, column=1, padx=5, pady=5, sticky=NSEW)

        browse_btn = ttk.Button(body_frame, text='Browse', bootstyle='secondary', command=self.browse)
        browse_btn.grid(row=1, column=2, padx=5, pady=5, sticky=NSEW)

        self.passwd_var = ttk.StringVar()

        passwd_lbl = ttk.Label(body_frame, text='Set the Prime Key :', font=('Helvetica', 13, 'bold'))
        passwd_lbl.grid(row=2, column=0, padx=5, pady=10, sticky=NSEW)

        self.passwd_txt = ttk.Entry(body_frame, textvariable=self.passwd_var, width=40, justify=CENTER)
        self.passwd_txt.grid(row=2, column=1, padx=5, pady=10, sticky=NSEW)

        ToolTip(self.passwd_txt, 'Only Required For Unencrypted Backups. For Encrypted Backup, the original prime key (set before backup) should be used.')

        self.disable_passwd_field()

        restore_btn = ttk.Button(body_frame, text='Restore', bootstyle='primary', command=self.restore)
        restore_btn.grid(row=3, column=1, padx=5, pady=10, sticky=NSEW)

    def browse(self):
        self.grab_release()
        fd = askopenfilename(parent=self, initialdir=self.PATH, defaultextension="", filetypes=[("All Files","*.*")])
        self.grab_set()
        f_path = Path(fd)
        self.path_var.set(f_path) 

    def enable_passwd_field(self):
        self.passwd_txt.config(state='normal')

    def disable_passwd_field(self):
        self.passwd_txt.config(state='disabled')

    def restore(self):
        stat = False
        
        if self.path_var.get() != 'No File Selected !' and len(self.path_var.get()) != 0:
            try:
                if self.type_choice.get() == 0: # Encypted Backup Restore
                    stat = self.PM.restore_backup(self.PM.filepath / self.PM.filename ,self.path_var.get())
                    self.PM.cipher_key = None

                elif self.type_choice.get() == 1: # Unencypted Backup Restore
                    if len(self.passwd_var.get()):
                        stat = self.PM.restore_backup(self.PM.filepath / self.PM.filename ,self.path_var.get(), False, self.passwd_var.get())
                        self.PM.cipher_key = None
                    else:
                        dialogs.Messagebox.show_error(parent=self, message='Please Enter the Prime Key')
            except:
                dialogs.Messagebox.show_error(parent=self, message='Integrity Test Failed ! \nPlease Select Valid File')

            if stat:
                dialogs.Messagebox.show_info(parent=self, message='Restore Successful !')
                self.destroy()
            else:
                dialogs.Messagebox.show_error(parent=self, message='Restore Failed !')
            
            

        else:
            dialogs.Messagebox.show_error(parent=self, message='Please Select a File to Restore !')



        
