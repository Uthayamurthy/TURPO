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

# SettingsMgr class handles all the sql stuff to save settings and gives a pythonic method to retrieve and save settings.

import sqlite3 as sql
import os

class SettingsMgr:

    def __init__(self, dbname, path, cat):
        
        self.filepath = path
        self.dbname = dbname
        
        self.create_settings_file() # Creates settings folder and settings file if it doesn't exist.
        
        self.conn = sql.connect(path / dbname)
        self.cur = self.conn.cursor()

        self.cat = cat
        
        try:
            # Try to access the tables
            for cat in self.cat:
                self.cur.execute('SELECT * FROM "{}"'.format(cat))
        except:
            # In case they don't exist ... Create them
            self.init_db()

    def create_settings_file(self):
        if not os.path.exists(self.filepath):
            print('Settings directory doesn\'t exist, hence creating ...')
            os.mkdir(self.filepath)
        else:
            print('File directory exists, so skipping ...')
        
        if not os.path.exists(self.filepath / self.dbname):
            print('Settings file not found !!')
            with open(self.filepath / self.dbname, 'w'): # Just Create A Empty File
                pass
            self.new_file = True
            print('Created a settingsfile.')
        else:
            print('File already exits, so skipping ...')

    def init_db(self):
        for cat in self.cat:
            self.cur.execute('CREATE TABLE IF NOT EXISTS "{}" (setting str, value str)'.format(cat))

    def retrieve(self, cat, setting):
        cols = self.get_columns(cat)
        if setting in cols:
            res = self.cur.execute('SELECT value FROM "{}" where setting=?'.format(cat), (setting, ))
            r = res.fetchall()
            
            return r[0][0]

    def get_columns(self, table):
        res = self.cur.execute('SELECT setting from "{}" '.format(table))
        columns = []
        for col in res.fetchall():
            columns.append(col[0])
        return columns
    
    def set(self, cat, setting, value):
        cols = self.get_columns(cat)
        if setting in cols:
            self.cur.execute('UPDATE "{}" SET value = ? where setting=?'.format(cat), (value, setting))
        else:
            self.cur.execute('INSERT INTO "{}" VALUES(?, ?)'.format(cat), (setting, value))
        self.conn.commit()
    
    def delete(self, cat, setting):
        self.cur.execute('DELETE FROM {} WHERE setting=?'.format(cat), (setting, ))
        self.conn.commit()