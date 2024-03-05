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
import webbrowser
from _version import __version__

class About(ttk.Frame):
    
    def __init__(self, main, PATH):
        super().__init__(main)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)

        self.path = PATH
        
        self.source_url = 'https://github.com/Uthayamurthy/TURPO'
        self.dev_url = 'https://github.com/Uthayamurthy'
        self.roadmap_url = 'https://github.com/Uthayamurthy/TURPO/blob/development/ROADMAP.md'
        self.release_url = 'https://github.com/Uthayamurthy/TURPO/releases'

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

        self.version_btn = ttk.Button(master=body_frame, text='What\'s New ?', bootstyle='primary-outline', command=self.open_release)
        self.version_btn.grid(row=1, column=1, padx=10, pady=10, sticky=NSEW)

        self.dev_lbl = ttk.Label(master=body_frame, text=f'Developer : R Uthaya Murthy', font=('Helvetica', 12, 'bold'))
        self.dev_lbl.grid(row=2, column=0, padx=10, pady=10, sticky=NSEW)

        self.dev_btn = ttk.Button(master=body_frame, text='Developer Details', bootstyle='primary-outline', command=self.open_dev)
        self.dev_btn.grid(row=2, column=1, padx=10, pady=10, sticky=NSEW)

        self.license_lbl = ttk.Label(master=body_frame, text=f'License : GNU General Public License (GPLv3)', font=('Helvetica', 12, 'bold'))
        self.license_lbl.grid(row=3, column=0, padx=10, pady=10, sticky=NSEW)

        self.license_btn = ttk.Button(master=body_frame, text='Read Full License', bootstyle='primary-outline', command=self.display_license)
        self.license_btn.grid(row=3, column=1, padx=10, pady=10, sticky=NSEW)

        self.source_lbl = ttk.Label(master=body_frame, text=f'Source : {self.source_url}', font=('Helvetica', 12, 'bold'))
        self.source_lbl.grid(row=4, column=0, padx=10, pady=10, sticky=NSEW)

        self.source_btn = ttk.Button(master=body_frame, text='View Source', bootstyle='primary-outline', command=self.open_source)
        self.source_btn.grid(row=4, column=1, padx=10, pady=10, sticky=NSEW)

        self.roadmap_lbl = ttk.Label(master=body_frame, text=f'Curious about the Current Developement Progress ? ', font=('Helvetica', 13, 'bold'))
        self.roadmap_lbl.grid(row=5, column=0, padx=10, pady=50, sticky=NSEW)

        self.roadmap_btn = ttk.Button(master=body_frame, text='View Roadmap', bootstyle='primary', command=self.open_roadmap)
        self.roadmap_btn.grid(row=5, column=1, padx=10, pady=50, sticky=NSEW)
        
        
    
    def display_license(self):
        license_window = ttk.Toplevel(self, topmost=True)
        license_window.geometry('500x700')
        license_window.title('T.U.R.P.O License')

        with open(self.path / 'LICENSE.txt', 'r') as l:
            license_txt = l.read()

        license_txt_area = ScrolledText(license_window, padding=5, height=10, autohide=True)
        license_txt_area.pack(fill=BOTH, expand=YES)
        license_txt_area.insert(END, license_txt)
    
    def open_source(self):
        webbrowser.open_new_tab(self.source_url)
    
    def open_dev(self):
        webbrowser.open_new_tab(self.dev_url)
    
    def open_roadmap(self):
        webbrowser.open_new_tab(self.roadmap_url)
    
    def open_release(self):
        webbrowser.open_new_tab(self.release_url)