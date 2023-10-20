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
from PIL import Image, ImageTk
from pathlib import Path
from turpo import TURPO
from _version import __version__

PATH = Path(__file__).parent

if __name__ == '__main__':

    app = ttk.Window(f"T.U.R.P.O (Trustworthy Utility for Reliable Password Organisation) V{__version__}", "litera", minsize=(800, 650))
    width = app.winfo_screenwidth()
    height = app.winfo_screenheight()
    app.geometry(f'{width}x{height}')
    ico = Image.open(PATH / 'assets' / 'logo.png')
    photo = ImageTk.PhotoImage(ico)
    app.wm_iconphoto(False, photo)
    TURPO(app, PATH)
    
    app.mainloop()