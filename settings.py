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
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.dialogs import dialogs
from tkinter.filedialog import askdirectory
from pathlib import Path
from ttkbootstrap.tooltip import ToolTip

# Import Tools 
from passwd_restore import Passwd_Restore
from passwd_change import Passwd_Change

class Gen_Settings(ttk.Frame): # Generalised settings class
    
    def __init__(self, main, app, PATH, pm, sm):
        super().__init__(main)

        self.app = app
        self.PATH = PATH
        self.PM = pm
        self.SM = sm
        self.cat = None # Assign for individual classes ! Eg :- 'PM'

        self.changed = False

        self.body = ttk.Frame(self)
        self.body.grid(row=0, column=0)

        self.footer = ttk.Frame(self)
        self.footer.grid(row=1, column=0)

        self.discard_btn = ttk.Button(self.footer, text='Discard', bootstyle='danger-outline', command=self.discard_setting)
        self.discard_btn.grid(row=0, column=0, padx=5, pady=50, sticky=W)
        self.discard_btn.config(state='disabled')

        self.save_btn = ttk.Button(self.footer, text='Save', bootstyle='success-outline', command=self.update_setting)
        self.save_btn.grid(row=0, column=1, padx=40, pady=50, sticky=N)
        self.save_btn.config(state='disabled')

        self.settings_index = {} # key:value :: 'setting_name': (setting_var, display_type)

    def set_change(self, var, index, mode):
        print("Traced variable {}".format(var))
        
        if not self.changed:
            self.changed = True
            self.save_btn.config(state='enabled')
            self.discard_btn.config(state='enabled')
        
    def update_setting(self):
        for setting_name, settings in self.settings_index.items():
            self.SM.set(self.cat, setting_name, str(settings[0].get()))
        self.changed = False
        try:
            self.discard_btn.config(state='disabled')
            self.save_btn.config(state='disabled')
            dialogs.Messagebox.show_info(message='Settings saved successfully !', title='Saved Settings')
        except:
            print("Avoiding disabling buttons because they don't exist !")

    def init_setting(self, setting, default, display_type): # Create a setting variable, check for value in db, if it doesn't exist create one ! Else return the existing one.
        if display_type == 'int':
            var = ttk.IntVar()
        elif display_type == 'str':
            var = ttk.StringVar()
        elif display_type == 'bool':
            var = ttk.BooleanVar()

        self.settings_index[setting] = (var, display_type)

        val = self.SM.retrieve(self.cat, setting)
        
        if val != None:
            var.set(self.conv_type(val, display_type))
        else:
            self.SM.set(self.cat, setting, default)
            var.set(self.conv_type(default, display_type))
        
        var.trace_add('write', self.set_change)


    def conv_type(self, val, typ):
        if typ == 'int':
            return int(val)
        elif typ == 'str':
            return str(val)
        elif typ == 'bool':
            return bool(val)
    
    def restore_values(self): 
        for setting_name, settings in self.settings_index.items():
            prev_setting = self.SM.retrieve(self.cat, setting_name)
            settings[0].set(prev_setting)     

    def discard_setting(self):
        response = dialogs.Messagebox.show_question(message='Are you sure you want to discard the changes ?', title='Discard Settings ?', buttons=['No:secondary', 'Yes:primary'])
        if response == 'Yes':
            self.restore_values()
            self.changed = False
            self.save_btn.config(state='disabled')
            self.discard_btn.config(state='disabled')

    def destroy(self):
        if self.changed:
            response = dialogs.Messagebox.show_question(message='Are you sure you want to discard the changes ?', title='Discard Settings ?', buttons=['No, Save:success', 'Discard:danger'])
            if response != 'Discard':
                self.update_setting()
        super().destroy()
        
class PM_Settings(Gen_Settings): # Password Management Settings
    def __init__(self, main, app, PATH, pm, sm):
        super().__init__(main, app, PATH, pm, sm)

        self.cat = 'PM'

        self.init_setting('autoPrompt', '1', 'int')
        self.set1_lbl = ttk.Label(self.body, text='Prompt Password Automatically on starting Manage Window ?', font=('Helventica', 13, 'bold'))
        self.set1_lbl.grid(row=0, column=0, padx=5, pady=8, sticky=NSEW)
        self.set1_btn = ttk.Checkbutton(self.body, bootstyle='info-round-toggle', variable=self.settings_index['autoPrompt'][0])
        self.set1_btn.grid(row=0, column=1, padx=70, pady=8, sticky=N)
        ToolTip(self.set1_btn, 'If Enabled, TURPO will prompt you for password (if not entered before or forgotten) whenever Manage window is opened.')

        self.init_setting('autoLockInterval', '0', 'int')
        self.set2_lbl = ttk.Label(self.body, text='Automatically Lock Interval (in minutes)', font=('Helventica', 13, 'bold'))
        self.set2_lbl.grid(row=1, column=0, padx=5, pady=8, sticky=NSEW)
        self.set2_box = ttk.Spinbox(self.body, state="readonly", from_= 0, to=10, textvariable=self.settings_index['autoLockInterval'][0], justify=CENTER, width=8)
        self.set2_box.grid(row=1, column=1, padx=70, pady=8, sticky=NSEW)
        ToolTip(self.set2_box, 'How long do you want TURPO to remember your Prime Key before automatically forgetting it (hence, locking it) ? It\'s a security feature.')

class PG_Settings(Gen_Settings):
    '''
    Password Generation - Settings Available:
    'defaultPasswdType' : Can take "Random Word Password", "Random Character Password", "Random Pin" (Default : "word")
    '''
    def __init__(self, main, app, PATH, pm, sm):

        super().__init__(main, app, PATH, pm, sm)

        self.cat = 'PG'

        self.init_setting('defaultPasswdType', 'Random Word Password', 'str')
        self.set1_lbl = ttk.Label(self.body, text='Default Password Generation Type', font=('Helventica', 13, 'bold'))
        self.set1_lbl.grid(row=0, column=0, padx=5, pady=5, sticky=NSEW)
        passwd_type_options = ['','Random Word Password', 'Random Character Password', 'Random Pin']
        self.set1_btn = ttk.OptionMenu(self.body, self.settings_index['defaultPasswdType'][0], *passwd_type_options, bootstyle='outline')
        self.set1_btn.grid(row=0, column=1, padx=70, pady=5, sticky=N)

        sep1 = ttk.Separator(self.body)
        sep1.grid(row=1, column=0, columnspan=2, pady=20,sticky=NSEW)

        lbl1 = ttk.Label(self.body, text='Random Word Password Generation Settings', font=('Helventica', 13, 'bold')) 
        lbl1.grid(row=2, column=0, padx=5, pady=5, sticky=NSEW)

        self.init_setting('wordPasswdSeperator', '-', 'str') 
        self.set2A_lbl = ttk.Label(self.body, text='Default Seperator', font=('Helventica', 12, 'bold'))
        self.set2A_lbl.grid(row=3, column=0, padx=5, pady=5, sticky=NSEW)
        sep_values = ['None', '-', '.', '_', ':', '!', '$']
        self.set2A_btn = ttk.Spinbox(self.body, state="readonly", values=sep_values, textvariable=self.settings_index['wordPasswdSeperator'][0], justify=CENTER, width=8)
        self.set2A_btn.grid(row=3, column=1, padx=70, pady=5, sticky=N)

        self.init_setting('wordPasswdNoWord', '4', 'int') 
        self.set2B_lbl = ttk.Label(self.body, text='Default Number of Words', font=('Helventica', 12, 'bold'))
        self.set2B_lbl.grid(row=4, column=0, padx=5, pady=5, sticky=NSEW)
        self.set2B_btn = ttk.Spinbox(self.body, state="readonly", from_=4, to=10, textvariable=self.settings_index['wordPasswdNoWord'][0], justify=CENTER, width=8)
        self.set2B_btn.grid(row=4, column=1, padx=70, pady=5, sticky=N)

        self.init_setting('wordPasswdLength', '4', 'int') 
        self.set2C_lbl = ttk.Label(self.body, text='Minimum Word Length', font=('Helventica', 12, 'bold'))
        self.set2C_lbl.grid(row=5, column=0, padx=5, pady=5, sticky=NSEW)
        self.set2C_btn = ttk.Spinbox(self.body, state="readonly", from_= 3, to=5, textvariable=self.settings_index['wordPasswdLength'][0], justify=CENTER, width=8)
        self.set2C_btn.grid(row=5, column=1, padx=70, pady=5, sticky=N)

        sep2 = ttk.Separator(self.body)
        sep2.grid(row=6, column=0, columnspan=2, pady=20,sticky=NSEW)

        lbl2 = ttk.Label(self.body, text='Random Character Password Generation Settings', font=('Helventica', 13, 'bold')) 
        lbl2.grid(row=7, column=0, padx=5, pady=5, sticky=NSEW)

        self.init_setting('randPassLength', '12', 'int') 
        self.set3A_lbl = ttk.Label(self.body, text='Number Of Characters :', font=('Helventica', 12, 'bold'))
        self.set3A_lbl.grid(row=8, column=0, padx=5, pady=5, sticky=NSEW)
        self.set3A_btn = ttk.Spinbox(self.body, state="readonly", from_= 10, to=25, textvariable=self.settings_index['randPassLength'][0], justify=CENTER, width=8)
        self.set3A_btn.grid(row=8, column=1, padx=70, pady=5, sticky=N)

        sep3 = ttk.Separator(self.body)
        sep3.grid(row=9, column=0, columnspan=2, pady=20,sticky=NSEW)

        lbl3 = ttk.Label(self.body, text='Numerical Pin Generation Settings', font=('Helventica', 13, 'bold')) 
        lbl3.grid(row=10, column=0, padx=5, pady=5, sticky=NSEW)

        self.init_setting('numPinLength', '4', 'int') 
        self.set4A_lbl = ttk.Label(self.body, text='Pin Length : ', font=('Helventica', 12, 'bold'))
        self.set4A_lbl.grid(row=11, column=0, padx=5, pady=5, sticky=NSEW)
        self.set4A_btn = ttk.Spinbox(self.body, state="readonly", from_= 4, to=16, textvariable=self.settings_index['numPinLength'][0], justify=CENTER, width=8)
        self.set4A_btn.grid(row=11, column=1, padx=70, pady=5, sticky=N)

class PB_Settings(Gen_Settings): # Password Backup Settings
    def __init__(self, main, app, PATH, pm, sm):
        super().__init__(main, app, PATH, pm, sm)

        self.cat = 'PB'

        self.init_setting('lastEncyptedBackup', 'No Backup Yet', 'str')
        self.set1_lbl = ttk.Label(self.body, text='Last Encrypted Backup', font=('Helventica', 13, 'bold'))
        self.set1_lbl.grid(row=0, column=0, padx=5, pady=8, sticky=NSEW)
        self.set1_lbl2 = ttk.Label(self.body, textvariable=self.settings_index['lastEncyptedBackup'][0], font=('Helventica', 12, 'bold'))
        self.set1_lbl2.grid(row=0, column=1, padx=70, pady=8, sticky=N)

        self.init_setting('lastUnencyptedBackup', 'No Backup Yet', 'str')
        self.set1_lbl = ttk.Label(self.body, text='Last Unencrypted Backup', font=('Helventica', 13, 'bold'))
        self.set1_lbl.grid(row=1, column=0, padx=5, pady=8, sticky=NSEW)
        self.set1_lbl2 = ttk.Label(self.body, textvariable=self.settings_index['lastUnencyptedBackup'][0], font=('Helventica', 12, 'bold'))
        self.set1_lbl2.grid(row=1, column=1, padx=70, pady=8, sticky=N)

        self.init_setting('defaultBackupType', 'Encrypted Backup', 'str')
        self.set2_lbl = ttk.Label(self.body, text='Default Password Backup Type', font=('Helventica', 13, 'bold'))
        self.set2_lbl.grid(row=2, column=0, padx=5, pady=8, sticky=NSEW)
        passwd_type_options = ['','Encrypted Backup', 'Unencrypted Backup']
        self.set2_btn = ttk.OptionMenu(self.body, self.settings_index['defaultBackupType'][0], *passwd_type_options, bootstyle='outline')
        self.set2_btn.grid(row=2, column=1, padx=70, pady=8, sticky=N)

        sep1 = ttk.Separator(self.body)
        sep1.grid(row=3, column=0, columnspan=2, pady=20,sticky=NSEW)

        self.init_setting('defaultBackupFilename', 'TURPO_Credentials_Backup', 'str')
        self.set3_lbl = ttk.Label(self.body, text='Default Backup File Name', font=('Helventica', 13, 'bold'))
        self.set3_lbl.grid(row=4, column=0, padx=5, pady=8, sticky=NSEW)
        self.set3_lbl2 = ttk.Entry(self.body, textvariable=self.settings_index['defaultBackupFilename'][0], width=50, justify=CENTER)
        self.set3_lbl2.grid(row=4, column=1, padx=70, pady=8, sticky=N)
        
        self.init_setting('defaultBackupLocation', str(PATH / 'backups'), 'str')
        self.set4_lbl = ttk.Label(self.body, text='Default Password Backup Location', font=('Helventica', 13, 'bold'))
        self.set4_lbl.grid(row=5, column=0, padx=5, pady=8, sticky=NSEW)
        self.set4_lbl2 = ttk.Label(self.body, textvariable=self.settings_index['defaultBackupLocation'][0], font=('Helventica', 12, 'bold'))   
        self.set4_lbl2.grid(row=5, column=1, padx=70, pady=8, sticky=N)
        self.set4_btn = ttk.Button(self.body, text='Browse', bootstyle='secondary', command=self.browse)
        self.set4_btn.grid(row=5, column=3, padx=10, pady=8, sticky=NSEW)

        self.init_setting('includeDate', '1', 'int')
        self.set5_lbl = ttk.Label(self.body, text='Include the Date with Filename by Default ?', font=('Helventica', 13, 'bold'))
        self.set5_lbl.grid(row=6, column=0, padx=5, pady=8, sticky=NSEW)
        self.set5_btn = ttk.Checkbutton(self.body, bootstyle='info-round-toggle', variable=self.settings_index['includeDate'][0])
        self.set5_btn.grid(row=6, column=1, padx=70, pady=8, sticky=N)

        self.init_setting('includeTime', '1', 'int')
        self.set6_lbl = ttk.Label(self.body, text='Include the Time with Filename by Default ?', font=('Helventica', 13, 'bold'))
        self.set6_lbl.grid(row=7, column=0, padx=5, pady=8, sticky=NSEW)
        self.set6_btn = ttk.Checkbutton(self.body, bootstyle='info-round-toggle', variable=self.settings_index['includeTime'][0])
        self.set6_btn.grid(row=7, column=1, padx=70, pady=8, sticky=N)
    
    def browse(self):
        self.fd = askdirectory(initialdir = self.settings_index['defaultBackupLocation'][0].get(), title='Select Default Backup Location')
        f_path = Path(self.fd)
        if str(f_path) != '.':
            self.settings_index['defaultBackupLocation'][0].set(str(f_path))

class Passwd_Tools(ttk.Frame): # Password Tools class
    
    def __init__(self, main, app, PATH, pm, sm):
        super().__init__(main)

        self.app = app
        self.PATH = PATH
        self.PM = pm
        self.SM = sm

        self.tool1_lbl = ttk.Label(self, text='Restore Your Backup', font=('Helventica', 13, 'bold'))
        self.tool1_lbl.grid(row=0, column=0, padx=5, pady=5, sticky=NSEW)
        self.tool1_btn = ttk.Button(self, text='Restore Tool', bootstyle='primary-outline', command=self.restore_window)
        self.tool1_btn.grid(row=0, column=1, padx=80, pady=5, sticky=NSEW)

        self.tool2_lbl = ttk.Label(self, text='Change Your Password', font=('Helventica', 13, 'bold'))
        self.tool2_lbl.grid(row=1, column=0, padx=5, pady=5, sticky=NSEW)
        self.tool2_btn = ttk.Button(self, text='Change Password Tool', bootstyle='primary-outline', command=self.change_window)
        self.tool2_btn.grid(row=1, column=1, padx=80, pady=5, sticky=NSEW)

    def restore_window(self):
        restore = Passwd_Restore(self, self.app, self.PATH, self.PM)
    
    def change_window(self):
        change = Passwd_Change(self, self.app, self.PATH, self.PM)

class Settings(ScrolledFrame):
    
    def __init__(self, main, app, PATH, pm, sm):
        super().__init__(main, autohide=True)

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
            self.sub_frame.destroy()
            self.sub_frame = None

    def handle_category_choice(self):

        choice = self.category_choice.get()

        self.clear_sub_frame()

        if choice == 0:
            self.sub_frame = PM_Settings(self.body_frame, self.app, self.PATH, self.PM, self.SM)
        elif choice == 1:
            self.sub_frame = PG_Settings(self.body_frame, self.app, self.PATH, self.PM, self.SM)
        elif choice == 2:
            self.sub_frame = PB_Settings(self.body_frame, self.app, self.PATH, self.PM, self.SM)
        elif choice == 3:
            self.sub_frame = Passwd_Tools(self.body_frame, self.app, self.PATH, self.PM, self.SM)
        
        try:
            self.sub_frame.grid(row=3, column=0, pady=20, sticky=NSEW)
        except:
            pass