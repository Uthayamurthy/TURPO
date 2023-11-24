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
from tkinter.filedialog import asksaveasfilename
from pathlib import Path
from ttkbootstrap.dialogs import dialogs
import datetime

class Backup_Frame(ttk.Frame):
    # lastBackupDate
    def __init__(self, main, pm, sm, mode):
        
        super().__init__(main)

        self.PM = pm
        self.SM = sm
        self.mode = mode

        self.path_var = ttk.StringVar()
        self.fname_var = ttk.StringVar()
        self.status_var = ttk.StringVar()
        self.last_backup = ttk.StringVar()

        if self.mode == 'e':
            self.last_backup.set(str(self.SM.retrieve('PB', 'lastEncyptedBackup')))
        if self.mode == 'u':
            self.last_backup.set(str(self.SM.retrieve('PB', 'lastUnencyptedBackup')))

        self.status_var.set('Ready to Start')
        self.fname_var.set(str(self.SM.retrieve('PB', 'defaultBackupFilename')))
        self.path_var.set(str(self.SM.retrieve('PB', 'defaultBackupLocation')))

        lbackup_lbl1 = ttk.Label(self, text='Last Backup :', font=('Helventica', 12, 'bold'))
        lbackup_lbl1.grid(row=0, column=0, padx=5, pady=5, sticky=NSEW)
        lbackup_lbl2 = ttk.Label(self, textvariable=self.last_backup, font=('Helventica', 12, 'bold'))
        lbackup_lbl2.grid(row=0, column=1, padx=5, pady=5, sticky=NSEW)

        fname_lbl = ttk.Label(self, text='File Name :', font=('Helventica', 12, 'bold'))
        fname_lbl.grid(row=1, column=0, padx=5, pady=5, sticky=NSEW)
        self.fname_txt = ttk.Entry(self, textvariable=self.fname_var, width=50, justify=CENTER)
        self.fname_txt.grid(row=1, column=1, padx=5, pady=5, sticky=NSEW)
        
        file_path = ttk.Label(self, text='File Path :', font=('Helventica', 12, 'bold'))
        file_path.grid(row=2, column=0, padx=5, pady=5, sticky=NSEW)
        self.path_txt = ttk.Entry(self, textvariable=self.path_var, width=50, justify=CENTER)
        self.path_txt.grid(row=2, column=1, padx=5, pady=5, sticky=NSEW)
        self.browse_btn = ttk.Button(self, text='Browse', bootstyle='secondary', command=self.browse)
        self.browse_btn.grid(row=2, column=2, padx=5, pady=5, sticky=NSEW)    

        self.include_date = ttk.IntVar()
        self.include_date.set(int(self.SM.retrieve('PB', 'includeDate')))
        self.date_lbl = ttk.Label(self, text='Include Date ?', font=('Helventica', 12, 'bold'))
        self.date_lbl.grid(row=3, column=0, padx=5, pady=5, sticky=NSEW)
        self.date_btn = ttk.Checkbutton(self, bootstyle='info-round-toggle', variable=self.include_date)
        self.date_btn.grid(row=3, column=1, padx=5, pady=5, sticky=NSEW)

        self.include_time = ttk.IntVar()
        self.include_time.set(int(self.SM.retrieve('PB', 'includeTime')))
        self.time_lbl = ttk.Label(self, text='Include Time ?', font=('Helventica', 12, 'bold'))
        self.time_lbl.grid(row=4, column=0, padx=5, pady=5, sticky=NSEW)
        self.time_btn = ttk.Checkbutton(self, bootstyle='info-round-toggle', variable=self.include_time)
        self.time_btn.grid(row=4, column=1, padx=5, pady=5, sticky=NSEW)

        self.status_lbl = ttk.Label(self, text='Status :', font=('Helventica', 12, 'bold'))
        self.status_lbl.grid(row=5, column=0, padx=5, pady=5, sticky=NSEW)
        status_txt = ttk.Label(self, textvariable=self.status_var, font=('Helventica', 12, 'bold'))
        status_txt.grid(row=5, column=1, padx=5, pady=5, sticky=NSEW)

        self.backup_btn = ttk.Button(self, text='Backup Now', bootstyle='primary', command=self.backup)
        self.backup_btn.grid(row=6, column=2, padx=5, pady=5, sticky=NSEW)

    def browse(self):
        self.fd = asksaveasfilename(initialfile = self.fname_var.get(), initialdir=self.path_var.get(), defaultextension="", filetypes=[("All Files","*.*")])
        f_name = Path(self.fd).name
        self.fname_var.set(f_name)
        f_path = Path(self.fd).parent
        self.path_var.set(f_path)
    
    def backup(self):
        self.status_var.set('Started !')

        try:
            fname = self.fname_var.get()
            now = datetime.datetime.now()
            date = now.strftime('-%d.%m.%Y')
            time = now.strftime('-%H.%M.%S')

            if self.include_date.get():
                fname += date
            if self.include_time.get():
                fname += time
            
            timestamp = date[1:] + ' ' + time[1:] + ' hrs'

            if self.mode=='e':
                self.PM.write(filename=fname, filepath=Path(self.path_var.get()))
                self.SM.set('PB', 'lastEncyptedBackup', timestamp)
                self.last_backup.set(timestamp)
                self.status_var.set('Backup Completed Successfully !')
            elif self.mode=='u':
                stat = self.PM.unencrypted_write(filename=fname, filepath=Path(self.path_var.get()))
                if stat: # If status True
                    self.SM.set('PB', 'lastUnencyptedBackup', timestamp)
                    self.last_backup.set(timestamp)
                    self.status_var.set('Backup Completed Successfully !')
                else:
                    self.status_var.set('Error - Prime Key Not Entered')

        except FileNotFoundError:
            self.status_var.set('Error - Invalid Path !')
        except:
            self.status_var.set('Some Error Occurred !')

class Backup(ttk.Frame):
    def __init__(self, main, pm, sm):
        super().__init__(main)
        self.PM = pm
        self.SM = sm

        self.param_frame = None

        self.columnconfigure(0, weight=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)

        # Header
        hdr_frame = ttk.Frame(self)
        hdr_frame.grid(row=0, column=0, sticky=NSEW)

        hlbl = ttk.Label(master=hdr_frame, text='Backup Your Passwords', font=('Helvetica', 22, 'bold'))
        hlbl.pack(side=TOP, fill=X, padx=10, pady=10, anchor=CENTER)

        # Body Frame
        self.body_frame = ttk.Frame(self, padding=10)
        self.body_frame.grid(row=1, column=0, sticky=NSEW)

        lbl1 = ttk.Label(master=self.body_frame,text='Backup Type', font=('Helvetica', 17, 'bold'))
        lbl1.grid(row=0, column=0, sticky=NW)

        backup_choices = ['Encrypted TURPO File Backup', 'Unencrypted Text File Backup']
        self.backup_choices_description = ['Your Backup is Encrypted, so you (or anybody else !) can\'t view the sensitive data without Prime Key and TURPO to open the password file.', 'Your Backup is Unencrypted and saved as text file, so you (or anybody else !) can view the sensitive data without Prime Key or TURPO. Take this at your own risk.']
        
        rb_group = ttk.Frame(self.body_frame, padding=10)
        rb_group.grid(row=1, column=0, sticky=NW)

        self.backup_choice = ttk.IntVar()

        choice1 = ttk.Radiobutton(rb_group, text=backup_choices[0], variable=self.backup_choice, value=0, command=self.handle_pass_choice, bootstyle="success-outline-toolbutton")
        choice1.pack(side=LEFT, expand=YES, padx=10)
        
        choice2 = ttk.Radiobutton(rb_group, text=backup_choices[1], variable=self.backup_choice, value=1, command=self.handle_pass_choice, bootstyle="danger-outline-toolbutton")
        choice2.pack(side=LEFT, expand=YES, padx=10)

        self.description_lbl = ttk.Label(self.body_frame, font=('Helventica', 12, 'bold'))
        self.description_lbl.grid(row=2, column=0, pady=15, sticky=NW)

        hdr = ttk.Label(self.body_frame, text='Backup Parameters', font=('Helventica', 16, 'bold'))
        hdr.grid(row=3, column=0, sticky=NSEW)

        default_type = self.SM.retrieve('PB', 'defaultBackupType')
        
        if default_type == 'Unencrypted Backup':
            choice2.invoke()
        else:
            choice1.invoke()
    
    def clear_param_frame(self): # Removes all the Widgets in main
        if self.param_frame != None:
            for widget in self.param_frame.winfo_children():
                widget.destroy()

    def handle_pass_choice(self):
        choice = self.backup_choice.get()
        self.description_lbl.config(text = 'Description: \n' +  self.backup_choices_description[choice])        

        self.clear_param_frame()

        if choice == 0:
            self.param_frame = Backup_Frame(self.body_frame, self.PM, self.SM, mode='e')
        elif choice == 1:
            self.param_frame = Backup_Frame(self.body_frame, self.PM, self.SM, mode='u')

                
        self.param_frame.grid(row=4, column=0, sticky=NSEW)