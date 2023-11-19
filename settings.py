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

class Gen_Settings(ttk.Frame): # Generalised settings class
    
    def __init__(self, main, app, PATH, pm, sm):
        super().__init__(main)

        self.app = app
        self.PATH = PATH
        self.PM = pm
        self.SM = sm
        self.cat = None # Assign for individual classes ! Eg :- 'PM'

        self.body = ttk.Frame(self)
        self.body.grid(row=0, column=0)

        self.footer = ttk.Frame(self)
        self.footer.grid(row=1, column=0)

        self.discard_btn = ttk.Button(self.footer, text='Discard', bootstyle='danger-outline', command=self.discard_setting)
        self.discard_btn.grid(row=0, column=0, padx=5, pady=50, sticky=W)

        self.save_btn = ttk.Button(self.footer, text='Save', bootstyle='success-outline', command=self.update_setting)
        self.save_btn.grid(row=0, column=1, padx=40, pady=50, sticky=N)


        self.settings_index = {} # key:value :: 'setting_name': (setting_var, display_type)

    def update_setting(self):
            for setting_name, settings in self.settings_index.items():
                self.SM.set(self.cat, setting_name, str(settings[0].get()))
            dialogs.Messagebox.show_info(message='Settings saved successfully !', title='Saved Settings')
    
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

    def conv_type(self, val, typ):
        if typ == 'int':
            return int(val)
        elif typ == 'str':
            return str(val)
        elif typ == 'bool':
            return bool(val)
        
    def discard_setting(self):
        dialogs.Messagebox.show_warning(message='Are you sure you want to discard the changes ?', title='Discard Settings ?')


class PM_Settings(Gen_Settings): # Password Management Settings
    def __init__(self, main, app, PATH, pm, sm):
        super().__init__(main, app, PATH, pm, sm)

        self.cat = 'PM'

        self.init_setting('autoPrompt', '1', 'int')
        self.set1_lbl = ttk.Label(self.body, text='Prompt Password Automatically on starting Manage Window ?', font=('Helventica', 12, 'bold'))
        self.set1_lbl.grid(row=0, column=0, padx=5, pady=5, sticky=NSEW)
        self.set1_btn = ttk.Checkbutton(self.body, bootstyle='info-round-toggle', variable=self.settings_index['autoPrompt'][0])
        self.set1_btn.grid(row=0, column=1, padx=40, pady=5, sticky=N)
        ToolTip(self.set1_btn, 'If Enabled, TURPO will prompt you for password (if not entered before or forgotten) whenever Manage window is opened.')

        self.init_setting('autoLockInterval', '0', 'int')
        self.set2_lbl = ttk.Label(self.body, text='Automatically Lock Interval (in minutes)', font=('Helventica', 12, 'bold'))
        self.set2_lbl.grid(row=1, column=0, padx=5, pady=5, sticky=NSEW)
        self.set2_box = ttk.Spinbox(self.body, state="readonly", from_= 0, to=10, textvariable=self.settings_index['autoLockInterval'][0], justify=CENTER, width=8)
        self.set2_box.grid(row=1, column=1, padx=40, pady=5, sticky=NSEW)
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
        self.set1_lbl = ttk.Label(self.body, text='Default Password Generation Type', font=('Helventica', 14, 'bold'))
        self.set1_lbl.grid(row=0, column=0, padx=5, pady=5, sticky=NSEW)
        passwd_type_options = ['','Random Word Password', 'Random Character Password', 'Random Pin']
        self.set1_btn = ttk.OptionMenu(self.body, self.settings_index['defaultPasswdType'][0], *passwd_type_options, bootstyle='outline')
        self.set1_btn.grid(row=0, column=1, padx=70, pady=5, sticky=N)

        sep1 = ttk.Separator(self.body)
        sep1.grid(row=1, column=0, columnspan=2, pady=20,sticky=NSEW)

        lbl1 = ttk.Label(self.body, text='Random Word Password Generation Settings', font=('Helventica', 14, 'bold')) 
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

        lbl2 = ttk.Label(self.body, text='Random Character Password Generation Settings', font=('Helventica', 14, 'bold')) 
        lbl2.grid(row=7, column=0, padx=5, pady=5, sticky=NSEW)

        self.init_setting('randPassLength', '12', 'int') 
        self.set3A_lbl = ttk.Label(self.body, text='Number Of Characters :', font=('Helventica', 12, 'bold'))
        self.set3A_lbl.grid(row=8, column=0, padx=5, pady=5, sticky=NSEW)
        self.set3A_btn = ttk.Spinbox(self.body, state="readonly", from_= 10, to=25, textvariable=self.settings_index['randPassLength'][0], justify=CENTER, width=8)
        self.set3A_btn.grid(row=8, column=1, padx=70, pady=5, sticky=N)

        sep3 = ttk.Separator(self.body)
        sep3.grid(row=9, column=0, columnspan=2, pady=20,sticky=NSEW)

        lbl3 = ttk.Label(self.body, text='Numerical Pin Generation Settings', font=('Helventica', 14, 'bold')) 
        lbl3.grid(row=10, column=0, padx=5, pady=5, sticky=NSEW)

        self.init_setting('numPinLength', '4', 'int') 
        self.set4A_lbl = ttk.Label(self.body, text='Pin Length : ', font=('Helventica', 12, 'bold'))
        self.set4A_lbl.grid(row=11, column=0, padx=5, pady=5, sticky=NSEW)
        self.set4A_btn = ttk.Spinbox(self.body, state="readonly", from_= 4, to=16, textvariable=self.settings_index['numPinLength'][0], justify=CENTER, width=8)
        self.set4A_btn.grid(row=11, column=1, padx=70, pady=5, sticky=N)

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
        elif choice == 1:
            self.sub_frame = PG_Settings(self.body_frame, self.app, self.PATH, self.PM, self.SM)

        self.sub_frame.grid(row=3, column=0, pady=20, sticky=NSEW)