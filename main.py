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
from snap_build import SNAP_BUILD
from _version import __version__
import os
import shutil
import filecmp

if SNAP_BUILD:
    print('Snap Build !')
    data_var = os.environ['SNAP_USER_DATA']
    PATH = Path(f'{data_var}/')
    print('PATH :', PATH)
    snap_path = Path(os.environ['SNAP'])
    # Copy Assets if not exists (For New Installations !)
    if not os.path.exists(PATH / 'assets'): 
        print('Assets does not exist ! So copying it to user data directory ...')
        shutil.copytree(snap_path / '_internal' / 'assets', PATH / 'assets')
        print('Done copying !')
    if not os.path.exists(PATH / 'LICENSE.txt'):
        print('LICENSE.txt does not exist ! So copying it to user data directory ...')
        shutil.copy(snap_path / '_internal' / 'LICENSE.txt', PATH)
        print('Done copying !')
    # Update Assets for the users updating their Installation, Only if necessary ...
    cmp = filecmp.dircmp(snap_path / '_internal' / 'assets', PATH / 'assets')
    print('Checking whether assets needs to be updated ...')
    if cmp.left_only or cmp.right_only:
        print('Updating Assets ...')
        shutil.rmtree(PATH / 'assets')
        shutil.copytree(snap_path / '_internal' / 'assets', PATH / 'assets')
        print('Done !')
    else:
        print('No need to update the assets !')
    
else:
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