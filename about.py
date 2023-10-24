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
from ttkbootstrap.scrolled import ScrolledText
# from PIL import Image, ImageTk
from _version import __version__

class About(ttk.Frame):
    
    def __init__(self, main, PATH):
        super().__init__(main)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)

        self.path = PATH
        
        # Header
        hdr_frame = ttk.Frame(self, padding=10)
        hdr_frame.grid(row=0, column=0, sticky=NSEW)
        hlbl = ttk.Label(master=hdr_frame, text='About', font=('Helvetica', 22, 'bold'))
        hlbl.pack(side=TOP, fill=X, padx=10, pady=10, anchor=CENTER)

        # Body Frame
        body_frame = ttk.Frame(self, padding=10)
        body_frame.grid(row=1, column=0, sticky=NSEW)

        self.app_lbl = ttk.Label(master=body_frame, text='T.U.R.P.O (Trustworthy Utility for Reliable Password Organisation) ', font=('Helvetica', 16, 'bold'))
        self.app_lbl.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)

        self.version_lbl = ttk.Label(master=body_frame, text=f'Version : V{__version__}', font=('Helvetica', 12, 'bold'))
        self.version_lbl.grid(row=1, column=0, padx=10, pady=10, sticky=NSEW)

        self.author_lbl = ttk.Label(master=body_frame, text=f'Author : R Uthaya Murthy (Email : uthayamurthy2006@gmail.com)', font=('Helvetica', 12, 'bold'))
        self.author_lbl.grid(row=2, column=0, padx=10, pady=10, sticky=NSEW)

        self.license_lbl = ttk.Label(master=body_frame, text=f'License : GNU General Public License (GPLv3)', font=('Helvetica', 12, 'bold'))
        self.license_lbl.grid(row=3, column=0, padx=10, pady=10, sticky=NSEW)

        self.license_lbl = ttk.Button(master=body_frame, text='Read Full License', bootstyle='primary-outline', command=self.display_license)
        self.license_lbl.grid(row=3, column=1, padx=10, pady=10, sticky=NSEW)
    
    def display_license(self):
        license_window = ttk.Toplevel(self, topmost=True)
        license_window.geometry('500x700')
        license_window.title('T.U.R.P.O License')

        with open(self.path / 'LICENSE.txt', 'r') as l:
            license_txt = l.read()

        license_txt_area = ScrolledText(license_window, padding=5, height=10, autohide=True)
        license_txt_area.pack(fill=BOTH, expand=YES)
        license_txt_area.insert(END, license_txt)