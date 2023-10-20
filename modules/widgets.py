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

# Contains some sweet widgets to make life easier !
# Use Geometry Managers as per requirement.


import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import pyperclip as pc
from PIL import Image, ImageTk

class CopyButton(ttk.Frame):
    
    def __init__(self, main, PATH, cp_txt, t_var=False, autoreset=False, font_size=15, img_size=(20, 20)):
        super().__init__(main)
        
        self.cp_txt = cp_txt
        self.t_var = t_var

        img1 = Image.open(PATH / 'assets' / 'copy.png')
        img2 = Image.open(PATH / 'assets' / 'copy-success.png')
        self.images = [ImageTk.PhotoImage(img1.resize(img_size), name='copy'), ImageTk.PhotoImage(img2.resize(img_size), name='copy_success')]
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=10)

        
        self.autoreset = autoreset

        self.btn = ttk.Button(self, image='copy', bootstyle='light', command=self.copy)
        self.btn.grid(row=0, column=0, padx=5, pady=5)

        self.lbl = ttk.Label(self, text='Copy', font=('Helventica', font_size, 'bold'))
        self.lbl.grid(row=0, column=1, padx=5, pady=5)

    def copy(self):
        self.btn.config(image='copy_success')
        self.lbl.config(text='Copied !')
        if self.t_var: # If tkinter variable
            pc.copy(self.cp_txt.get())
        else:
            pc.copy(self.cp_txt)
        if self.autoreset:
            self.after(2000, self.reset)
    
    def reset(self):
        self.btn.config(image='copy')
        self.lbl.config(text='Copy')

class ShowHideButton(ttk.Frame):
    
    def __init__(self, main, PATH, field, show_text=False, font_size=15, img_size=(20, 20)):
        super().__init__(main)
        
        self.field = field

        self.show_text = show_text

        img1 = Image.open(PATH / 'assets' / 'show.png')
        img2 = Image.open(PATH / 'assets' / 'hide.png')
        self.images = [ImageTk.PhotoImage(img1.resize(img_size), name='show'), ImageTk.PhotoImage(img2.resize(img_size), name='hide')]
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=10)

        self.btn = ttk.Button(self, image='show', bootstyle='light', command=self.btn_control)
        self.btn.grid(row=0, column=0, padx=5, pady=5)

        if show_text:
            self.lbl = ttk.Label(self, text='Show', font=('Helventica', font_size, 'bold'))
            self.lbl.grid(row=0, column=1, padx=5, pady=5)
        
        self.field.configure(show="*")
        self.mode = 'hide'

    def btn_control(self):
        if self.mode == 'hide':
            self.show()
            self.mode='show'
        elif self.mode == 'show':
            self.hide()
            self.mode='hide'

    def show(self):
        self.btn.config(image='hide')
        if self.show_text:
            self.lbl.config(text='Hide')
        self.field.configure(show="")
    
    def hide(self):
        self.btn.config(image='show')
        if self.show_text:
            self.lbl.config(text='Show')
        self.field.configure(show="*")


class CopyField(ttk.Frame):

    def __init__(self, main, PATH, cp_txt, t_var=False, font_size=15, img_size=(20, 20)):
        super().__init__(main)

        self.columnconfigure(0, weight=10)
        self.columnconfigure(1, weight=1)


        if t_var:
            self.lbl = ttk.Label(self, textvariable=cp_txt, font=('Helventica', font_size, 'bold'))
            self.lbl.grid(row=0, column=0, padx=8, pady=5)
        else:
            self.lbl = ttk.Label(self, text=cp_txt, font=('Helventica', font_size, 'bold'))
            self.lbl.grid(row=0, column=0, padx=8, pady=5)

        self.btn = CopyButton(self, PATH, cp_txt, t_var, False, font_size, img_size)
        self.btn.grid(row=0, column=1, padx=8, pady=5)

    def reset(self):
        self.btn.reset()

class CopyPassField(ttk.Frame):

    def __init__(self, main, PATH, cp_txt, t_var=False, font_size=15, img_size=(20, 20)):
        super().__init__(main)

        self.columnconfigure(0, weight=10)
        self.columnconfigure(1, weight=1)


        if t_var:
            self.lbl = ttk.Label(self, textvariable=cp_txt, font=('Helventica', font_size, 'bold'))
            self.lbl.grid(row=0, column=0, padx=8, pady=5)
        else:
            self.lbl = ttk.Label(self, text=cp_txt, font=('Helventica', font_size, 'bold'))
            self.lbl.grid(row=0, column=0, padx=8, pady=5)

        self.cp_btn = CopyButton(self, PATH, cp_txt, t_var, False, font_size, img_size)
        self.cp_btn.grid(row=0, column=1, padx=8, pady=5)

    def reset(self):
        self.cp_btn.reset()

class CopyEntry(ttk.Frame):

    def __init__(self, main, PATH, initial_txt, autoreset=True, font_size=15, img_size=(20, 20)):
        super().__init__(main)

        self.columnconfigure(0, weight=10)
        self.columnconfigure(1, weight=1)

        self.entry = ttk.Entry(self, font=('Helventica', font_size, 'bold'))
        self.entry.insert(0, initial_txt)
        self.entry.grid(row=0, column=0, padx=8, pady=5)
        self.disable_entry()

        self.btn = CopyButton(self, PATH, self.entry, True, autoreset, font_size, img_size)
        self.btn.grid(row=0, column=1, padx=8, pady=5)

    def reset(self):
        self.btn.reset()
    
    def disable_entry(self):
        self.entry.config(state= "disabled")
    
    def enable_entry(self):
        self.entry.config(state= "normal")

    def get(self):
        return self.entry.get()