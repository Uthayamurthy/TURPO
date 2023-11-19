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
from modules.passwdgen import *
from modules.widgets import CopyField


class RandWordPassword(ttk.Frame):

    def __init__(self, main, PATH):
        super().__init__(main)       

        # Number of Words
        num_words_lbl = ttk.Label(self, text='Number Of Words : ', font=('Helventica', 12, 'bold'))
        num_words_lbl.grid(row=0, column=0, padx=5, pady=5, sticky=NSEW)
        
        self.num_words = ttk.IntVar(value=4)

        num_words_box = ttk.Spinbox(self, state="readonly", from_= 4, to=10, textvariable=self.num_words,justify=CENTER, width=8)
        num_words_box.grid(row=0, column=1, padx=5, pady=5, sticky=NSEW)
        
        # Seperator
        sep_lbl = ttk.Label(self, text='Seperator : ', font=('Helventica', 12, 'bold'))
        sep_lbl.grid(row=1, column=0, padx=5, pady=5, sticky=NSEW)
        
        self.sep = ttk.StringVar(value='None')
        sep_values = ['None', '-', '.', '_', ':', '!', '$']
        sep_values.reverse()

        sep_box = ttk.Spinbox(self, state="readonly", values=sep_values, textvariable=self.sep,justify=CENTER, width=8)
        sep_box.grid(row=1, column=1, padx=5, pady=5, sticky=NSEW)

        # Min Word Length
        min_len_lbl = ttk.Label(self, text='Minimum Word Length : ', font=('Helventica', 12, 'bold'))
        min_len_lbl.grid(row=2, column=0, padx=5, pady=5, sticky=NSEW)
        
        self.min_len = ttk.IntVar(value=4)

        min_len_box = ttk.Spinbox(self, state="readonly", from_= 3, to=5, textvariable=self.min_len,justify=CENTER, width=8)
        min_len_box.grid(row=2, column=1, padx=5, pady=5, sticky=NSEW)
        
        # Generate password Button

        gen_button = ttk.Button(self, text='Generate',bootstyle='success', command=self.generate)
        gen_button.grid(row=3, column=1, padx=5, pady=10, sticky=NSEW)

        result_head = ttk.Label(self, text='Generated Password', font=('Helventica', 16, 'bold'))
        result_head.grid(row=5, column=0, sticky=NSEW)


        self.result = ttk.StringVar(value='Click On Generate ')

        self.result_lbl = CopyField(self, PATH, self.result, True)
        self.result_lbl.grid(row=6, column=0, padx=10, pady=10, sticky=NSEW)

    def generate(self):
        self.result.set(gen_dict_password(self.num_words.get(), self.sep.get(), self.min_len.get()))
        self.result_lbl.reset()

class RandPassword(ttk.Frame):

    def __init__(self, main, PATH):
        super().__init__(main)

        # Number of Characters
        num_char_lbl = ttk.Label(self, text='Number Of Characters : ', font=('Helventica', 12, 'bold'))
        num_char_lbl.grid(row=0, column=0, padx=5, pady=5)
        
        self.num_chars = ttk.IntVar(value=12)

        num_char_box = ttk.Spinbox(self, state="readonly", from_= 10, to=25, textvariable=self.num_chars, justify=CENTER, width=8)
        num_char_box.grid(row=0, column=1, padx=5, pady=5)
        
        # Generate password Button

        gen_button = ttk.Button(self, text='Generate', bootstyle='success', command=self.generate)
        gen_button.grid(row=1, column=1, padx=5, pady=10)

        # Result
        result_frame = ttk.Frame(self)
        result_frame.grid(row=2, column=0, columnspan=2, sticky=NSEW)

        result_head = ttk.Label(result_frame, text='Generated Password', font=('Helventica', 16, 'bold'))
        result_head.grid(row=0, column=0, sticky=NSEW)


        self.result = ttk.StringVar(value='Click On Generate ')

        self.result_lbl = CopyField(result_frame, PATH, self.result, True)
        self.result_lbl.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky=NSEW)

    def generate(self):
        self.result.set(gen_random_password(self.num_chars.get()))
        self.result_lbl.reset()

class RandPin(ttk.Frame):

    def __init__(self, main, PATH):
        super().__init__(main)

        # Number of Characters
        num_char_lbl = ttk.Label(self, text='Pin Length : ', font=('Helventica', 12, 'bold'))
        num_char_lbl.grid(row=0, column=0, padx=5, pady=5)
        
        self.num_chars = ttk.IntVar(value=4)

        num_char_box = ttk.Spinbox(self, state="readonly", from_= 4, to=16, textvariable=self.num_chars, justify=CENTER, width=8)
        num_char_box.grid(row=0, column=1, padx=5, pady=5)
        
        # Generate password Button

        gen_button = ttk.Button(self, text='Generate', bootstyle='success', command=self.generate)
        gen_button.grid(row=1, column=1, padx=5, pady=10)

        # Result
        result_frame = ttk.Frame(self)
        result_frame.grid(row=2, column=0, columnspan=4, sticky=NSEW)

        result_head = ttk.Label(result_frame, text='Generated Password', font=('Helventica', 16, 'bold'))
        result_head.grid(row=0, column=0, sticky=NSEW)


        self.result = ttk.StringVar(value='Click On Generate ')

        self.result_lbl = CopyField(result_frame, PATH, self.result, True)
        self.result_lbl.grid(row=1, column=0, padx=10, pady=10, sticky=NSEW)


    def generate(self):
        self.result.set(gen_pin(self.num_chars.get()))
        self.result_lbl.reset()

class Generate(ttk.Frame):
    
    def __init__(self, main, PATH):
        super().__init__(main)


        self.PATH = PATH
        load_dictionary(self.PATH) # Load the common words dictionary

        self.param_frame = None
        
        self.columnconfigure(0, weight=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)

        # Header
        hdr_frame = ttk.Frame(self)
        hdr_frame.grid(row=0, column=0, sticky=NSEW)

        hlbl = ttk.Label(master=hdr_frame, text='Generate Passwords', font=('Helvetica', 22, 'bold'))
        hlbl.pack(side=TOP, fill=X, padx=10, pady=10, anchor=CENTER)

        # Body Frame
        self.body_frame = ttk.Frame(self, padding=10)
        self.body_frame.grid(row=1, column=0, sticky=NSEW)

        lbl1 = ttk.Label(master=self.body_frame,text='Password Type', font=('Helvetica', 16, 'bold'))
        lbl1.grid(row=0, column=0, sticky=NW)
        
        pass_choices = ['Random Character Password', 'Random Word Password', 'Numerical Pin']
        self.pass_choices_description = ['Generates password that has random characters.', 'Generates password that has random easy to remember words.', 'Generates random numerical pin (Ideal for phone pin).']
        
        rb_group = ttk.Frame(self.body_frame, padding=10)
        rb_group.grid(row=1, column=0, sticky=NW)

        self.pass_choice = ttk.IntVar()

        choice1 = ttk.Radiobutton(rb_group, text=pass_choices[0], variable=self.pass_choice, value=0, command=self.handle_pass_choice, bootstyle="success-outline-toolbutton")
        choice1.pack(side=LEFT, expand=YES, padx=10)
        
        choice2 = ttk.Radiobutton(rb_group, text=pass_choices[1], variable=self.pass_choice, value=1, command=self.handle_pass_choice, bootstyle="success-outline-toolbutton")
        choice2.pack(side=LEFT, expand=YES, padx=10)

        choice3 = ttk.Radiobutton(rb_group, text=pass_choices[2], variable=self.pass_choice, value=2, command=self.handle_pass_choice, bootstyle="success-outline-toolbutton")
        choice3.pack(side=LEFT, expand=YES, padx=10)

        self.description_lbl = ttk.Label(self.body_frame, font=('Helventica', 12, 'bold'))
        self.description_lbl.grid(row=2, column=0, pady=15, sticky=NW)

        hdr = ttk.Label(self.body_frame, text='Password Parameters', font=('Helventica', 16, 'bold'))
        hdr.grid(row=3, column=0, sticky=NSEW)

        choice1.invoke()   


    def clear_param_frame(self): # Removes all the Widgets in main
        if self.param_frame != None:
            for widget in self.param_frame.winfo_children():
                widget.destroy()
    
    def handle_pass_choice(self):
        choice = self.pass_choice.get()
        self.description_lbl.config(text = 'Description: \n' +  self.pass_choices_description[choice])

        self.clear_param_frame()

        if choice == 0:
            self.param_frame = RandPassword(self.body_frame, self.PATH)
        elif choice==1:
            self.param_frame = RandWordPassword(self.body_frame, self.PATH)
        elif choice==2:
            self.param_frame = RandPin(self.body_frame, self.PATH)
                
        self.param_frame.grid(row=4, column=0, sticky=NSEW)

        
