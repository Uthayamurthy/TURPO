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
from ttkbootstrap.dialogs import dialogs
from ttkbootstrap.tooltip import ToolTip

class PM_Settings(ttk.Frame):
    def __init__(self, main, app, PATH, pm, sm):
        super().__init__(main)

        self.app = app
        self.PATH = PATH
        self.PM = pm
        self.SM = sm

        self.set1_var = ttk.IntVar()
        self.set1_var.set(int(self.init_retrieve('autoPrompt', '1')))
        self.set1_lbl = ttk.Label(self, text='Prompt Password Automatically on starting Manage Window ?', font=('Helventica', 12, 'bold'))
        self.set1_lbl.grid(row=0, column=0, padx=5, pady=5, sticky=NSEW)
        self.set1_btn = ttk.Checkbutton(self, bootstyle='info-round-toggle', variable=self.set1_var)
        self.set1_btn.grid(row=0, column=1, padx=40, pady=5, sticky=N)
        ToolTip(self.set1_btn, 'If Enabled, TURPO will prompt you for password (if not entered before or forgotten) whenever Manage window is opened.')

        self.set2_var = ttk.IntVar()
        self.set2_var.set(int(self.init_retrieve('autoLockInterval', '0')))
        self.set2_lbl = ttk.Label(self, text='Automatically Lock Interval (in minutes)', font=('Helventica', 12, 'bold'))
        self.set2_lbl.grid(row=1, column=0, padx=5, pady=5, sticky=NSEW)
        self.set2_box = ttk.Spinbox(self, state="readonly", from_= 0, to=10, textvariable=self.set2_var, justify=CENTER, width=8)
        self.set2_box.grid(row=1, column=1, padx=40, pady=5, sticky=NSEW)
        ToolTip(self.set2_box, 'How long do you want TURPO to remember your Prime Key before automatically forgetting it (hence, locking it) ? It\'s a security feature.')

        self.discard_btn = ttk.Button(self, text='Discard', bootstyle='danger-outline', command=self.discard_setting)
        self.discard_btn.grid(row=5, column=0, padx=5, pady=50, sticky=W)

        self.save_btn = ttk.Button(self, text='Save', bootstyle='success-outline', command=self.update_setting)
        self.save_btn.grid(row=5, column=2, padx=40, pady=50, sticky=N)
        

    
    def update_setting(self):
        self.SM.set('PM', 'autoPrompt', str(self.set1_var.get()))
        self.SM.set('PM', 'autoLockInterval', str(self.set2_var.get()))
        dialogs.Messagebox.show_info(message='Settings saved successfully !', title='Saved Settings')


    def init_retrieve(self, setting, default): # Initial Retrieve, In case setting doesn't exist insert the default value and return the same.
        val = self.SM.retrieve('PM', setting)
        if val != None:
            return val
        else:
            self.SM.set('PM', setting, default)
            return default


    def discard_setting(self):
        dialogs.Messagebox.show_warning(message='Are you sure you want to discard the changes ?', title='Discard Settings ?')

class Settings(ttk.Frame):
    
    def __init__(self, main, app, PATH, pm, sm):
        super().__init__(main)

        self.app = app
        self.PATH = PATH
        self.PM = pm
        self.SM = sm

        self.sub_frame = None

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)
        
        # Header
        hdr_frame = ttk.Frame(self, padding=10)
        hdr_frame.grid(row=0, column=0, sticky=NSEW)

        hlbl = ttk.Label(master=hdr_frame, text='Settings', font=('Helvetica', 22, 'bold'))
        hlbl.pack(side=TOP, fill=X, padx=10, pady=10, anchor=CENTER)

        # Body Frame
        self.body_frame = ttk.Frame(self, padding=10)
        self.body_frame.grid(row=1, column=0, sticky=NSEW)

        lbl1 = ttk.Label(master=self.body_frame,text='Settings Category', font=('Helvetica', 16, 'bold'))
        lbl1.grid(row=0, column=0, sticky=NW)

        category_choices = ['Password Management', 'Password Generation', 'Password Backups', 'Password Tools']
        
        rb_group = ttk.Frame(self.body_frame, padding=10)
        rb_group.grid(row=1, column=0, sticky=NW)

        self.category_choice = ttk.IntVar()

        choice1 = ttk.Radiobutton(rb_group, text=category_choices[0], variable=self.category_choice, value=0, command=self.handle_category_choice, bootstyle="success-outline-toolbutton")
        choice1.pack(side=LEFT, expand=YES, padx=10)
        
        choice2 = ttk.Radiobutton(rb_group, text=category_choices[1], variable=self.category_choice, value=1, command=self.handle_category_choice, bootstyle="success-outline-toolbutton")
        choice2.pack(side=LEFT, expand=YES, padx=10)

        choice3 = ttk.Radiobutton(rb_group, text=category_choices[2], variable=self.category_choice, value=2, command=self.handle_category_choice, bootstyle="success-outline-toolbutton")
        choice3.pack(side=LEFT, expand=YES, padx=10)

        choice4 = ttk.Radiobutton(rb_group, text=category_choices[3], variable=self.category_choice, value=3, command=self.handle_category_choice, bootstyle="success-outline-toolbutton")
        choice4.pack(side=LEFT, expand=YES, padx=10)

        choice1.invoke()

        sep = ttk.Separator(self.body_frame)
        sep.grid(row=2, column=0, pady=30,sticky=NSEW)

    def clear_sub_frame(self):
        if self.sub_frame != None:
            for widget in self.sub_frame.winfo_children():
                widget.destroy()

    def handle_category_choice(self):

        choice = self.category_choice.get()

        self.clear_sub_frame()

        if choice == 0:
            self.sub_frame = PM_Settings(self.body_frame, self.app, self.PATH, self.PM, self.SM)
        
        self.sub_frame.grid(row=3, column=0, pady=20, sticky=NSEW)