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

# A Highly Modified and Adopted version of Configuration Manager - https://github.com/Uthayamurthy/ConfigManager-Micropython

# PasswdMgr class is used to save passwords and associated data in a file.

import re
import os
import shutil

try:
    from modules.AES import AESCipher
    import modules.passwdgen as passwdgen
except ModuleNotFoundError:
    from AES import AESCipher
    import passwdgen

class PasswdMgr:

    def __init__(self, filepath, filename, cipher_key=None):
        self.filename = filename
        self.filepath = filepath
        self.sections = []
        self.pw = {}
        self.cipher_key = cipher_key
        self.new_file = False # Used to track whether new file is created or not ...
        self.create_data_file()
        self.read()
        self.test_pwfile()
        if self.cipher_key != None:
            self.init_cipher()

    def init_cipher(self, passwd=None):
        if passwd == None: 
            passwd = self.cipher_key
        else:
            self.cipher_key = passwd
        self.cipher = AESCipher(passwd)
    
    def test_pwfile(self): # Check whether the pwfile is initialised.
        try:
            test_text = self.pw['main']['test_text']
        except KeyError:
            print('Password File not Initialised !')
            self.new_file = True

    def check_cipher(self, passwd):
        self.read()
        self.init_cipher(passwd)
        test_text = self.pw['main']['test_text']
        try:
            self.cipher.decrypt(test_text)
            return True
        except UnicodeDecodeError:
            return False
        
    def have_cipher(self): # Checks whether cipher is there and is correct.
        if self.cipher_key != None:
            return self.check_cipher(self.cipher_key)
        else:
            return False
        
    
    def init_pwfile(self, passwd):
        self.read()
        self.init_cipher(passwd)
        if self.pw == {}:
            self.sections= ['main']
            # pass_hash = self.gen_hash(passwd)
            test_text = self.cipher.encrypt(passwdgen.gen_random_password(18)) # Random encrypted text, useful later to check the key is right or not. 
            self.pw = {
                'main': {'test_text':test_text}
            }
            self.write()
            self.new_file = False
        else:
            print('Skipping Initialisation as the file is not empty.')

    def create_data_file(self):
        if not os.path.exists(self.filepath):
            print('Data directory doesn\'t exist, hence creating ...')
            os.mkdir(self.filepath)
        else:
            print('File directory exists, so skipping ...')
        
        if not os.path.exists(self.filepath / self.filename):
            print('Data file not found !!')
            with open(self.filepath / self.filename, 'w'): # Just Create A Empty File
                pass
            self.new_file = True
            print('Created a datafile.')
        else:
            print('File already exits, so skipping ...')


    def read(self, filepath=None, filename=None):
        sectionre = re.compile('\[(.*)\]')
        entryre = re.compile('(.*?)=(.*)')
        stringre = re.compile('"(.*)"')
        intre = re.compile('^[0-9]*$')
        commentre = re.compile('^#.*')

        if filepath == None: filepath = self.filepath
        if filename == None: filename = self.filename
        with open(filepath / filename, 'r') as pwfile:
            # Reset pw and sections
            self.pw = {} 
            self.sections = []  
            for line in pwfile:
                line = line.strip()
                if line == '' or line == ' ': continue
                if commentre.search(line): continue
                if sectionre.search(line):
                    section = sectionre.search(line).group(1)
                    if section not in self.sections: self.sections.append(section)
                    self.pw[section] = {}
                    current_section = section
                elif entryre.search(line):
                    entry = entryre.search(line)
                    entry_val = entry.group(2)
                    if stringre.search(entry_val):
                        entry_val = stringre.search(entry_val).group(1).strip()
                        if entry_val.startswith('!'):
                            entry_val = entry_val[1:].split(',')
                            entry_val = [a.strip() for a in entry_val]
                        
                    elif intre.search(entry_val):
                        entry_val = int(intre.search(entry_val.strip()).group(0))
                    self.pw[current_section][entry.group(1).strip()] = entry_val

    def reload(self):
        self.read()

    def write(self, pw=None, filepath=None, filename=None): # For saving general changes and taking backups.
        if pw == None: pw = self.pw
        if filename == None: filename = self.filename
        if filepath == None: filepath = self.filepath
        
        with open(filepath / f'{filename}_new', 'w') as pwfile: # Safe writing ... Write in new file and then rename it once successfully written.
            for section, entry in pw.items():
                pwfile.write(f'[{section}]')
                for key, value in entry.items():
                    if isinstance(value, str): value = f'"{value}"'
                    pwfile.write(f'\n{key}={value}')
                pwfile.write('\n\n')
        
        try:
            os.remove(filepath / filename) # Remove Old file
        except:
            print('No old file found to remove, so moving ahead to rename the file.')
        os.rename(filepath / f'{filename}_new', filepath / filename)

    def unencrypted_write(self, filepath, pw=None, filename=None): # For Unencrypted Backups, return -> True if password available and successfully saved else false.
        if pw == None: pw = self.pw
        if filename == None: filename = self.filename

        encrypted_fieldnames = ['password', 'username', 'pin', 'email']

        if self.have_cipher():
            with open(filepath / f'{filename}_new', 'w') as pwfile:
                for section, entry in pw.items():
                    if section == 'main': # Skip main section for backups
                        continue
                    pwfile.write(f'[{section}]')
                    for key, value in entry.items():
                        if key in encrypted_fieldnames:
                            value = self.cipher.decrypt(value) # Decrypt the value before saving.
                        if isinstance(value, str): value = f'"{value}"'
                        pwfile.write(f'\n{key}={value}')
                    pwfile.write('\n\n')
            
            os.rename(filepath / f'{filename}_new', filepath / filename)
            return True
        else:
            return False
        
    def change_prime_key(self, old_key, new_key):
        try:
            self.read()
            os.rename(self.filepath / self.filename, self.filepath / f'{self.filename}_old') # Backup
            old_cipher = AESCipher(old_key)
            new_cipher = AESCipher(new_key)
            encrypted_fieldnames = ['password', 'username', 'pin', 'email']

            test_text = new_cipher.encrypt(passwdgen.gen_random_password(18))

            self.pw['main'] = {'test_text':test_text}

            with open(self.filepath / self.filename, 'w') as pwfile:
                for section, entry in self.pw.items():
                    pwfile.write(f'[{section}]')

                    for key, value in entry.items():
                        if key in encrypted_fieldnames:
                            value = new_cipher.encrypt(old_cipher.decrypt(value)) # Encrypt with new password !
                        if isinstance(value, str): value = f'"{value}"'
                        pwfile.write(f'\n{key}={value}')
                    pwfile.write('\n\n')
            return True

        except:
            self.cipher_key = None
            print('Prime Key Change Failed ! Restoring the old file ...')
            os.rename(self.filepath / f'{self.filename}_old', self.filepath / self.filename)
            print('Done !')
            return False
        
    def check_integrity(self, filepath, filename, encrypted): # Check the integrity of the password file (Before restoring)
        try:
            if encrypted: # Check For Encrypted Files
                self.read(filepath, filename)
                test_text = self.pw['main']['test_text']
                if test_text != '' and test_text != ' ' and test_text != None:
                    return True
                else:
                    return False
            else: # Check for Unencrypted File
                self.read(filepath, filename)
                if len(self.sections) != 0:
                    return True
                else:
                    return False
        except:
            return False
        finally: # Cleanup
            self.read()

    def prepare_restore(self, passwd): # If credentials in pw are unencrypted, this method will encrypt them automatically, Used to encrypt Newly Restored Unencrypted Files. Also, add main test text.
        

        encrypted_fieldnames = ['password', 'username', 'pin', 'email']
        temp_cipher = AESCipher(passwd)
        
        self.sections.append('main')
        self.pw['main'] = {}

        test_text = passwdgen.gen_random_password(18)
        self.pw['main']['test_text'] = temp_cipher.encrypt(test_text)
        
        for section, entry in self.pw.items():
            if section == 'main':
                continue
            for key, value in entry.items():
                if key in encrypted_fieldnames:
                    self.pw[section][key] = temp_cipher.encrypt(value)

        
    def restore_backup(self, filepath, filename, encrypted=True, passwd=None):
        file_integrity = self.check_integrity(filepath, filename, encrypted)
        if file_integrity == True:
            try:
                os.rename(self.filepath / self.filename, self.filepath / f'{self.filename}_old') # For redundancy rename the current file rather than deleting it !
                if encrypted: # Restoring Encrypted Backup        
                    shutil.copyfile(filepath / filename, self.filepath / self.filename)
                    return True
                else: # Restoring Unencrypted Backup
                    if passwd == None: return False
                    self.read(filepath, filename)
                    self.prepare_restore(passwd)
                    self.write()
                    return True

            except:
                print('Encountered some error while trying to restore the backup.')
                print('Restoring the current file ...')
                os.rename(self.filepath / f'{self.filename}_old', self.filepath / self.filename)
                self.read()
                return False
        else:
            raise Exception('Password File Integrity Test Failed !')


    def set_section(self, section):
        self.sections.append(section)
        self.pw[section] = {}
    
    # Special method to save secrets (sensitive data) encrypted. 
    def set_secret(self, section, key, secret):
        if section not in self.sections: self.set_section(section)
        encrypted_passwd = self.cipher.encrypt(secret)
        self.pw[section][key] = encrypted_passwd

    # General method to save all the other stuff.
    def set_entry(self, section, key, value):
        if section not in self.sections: self.set_section(section)
        self.pw[section][key] = value

    # Returns a list of (name, type, date) to display
    def get_tree_data(self):
        tree_data = []
        for section in self.sections:
            if section == 'main': continue
            tree_data.append(('',section, self.pw[section]['type'], self.pw[section]['date']))
        return tree_data
    
    def remove_section(self, section):
        self.sections.remove(section)
        self.pw.pop(section)

    def remove_entry(self, section, key):
        self.pw[section].pop(key)

    def __repr__(self):
        return f'pw File Object : {self.filepath / self.filename}'
    
    def __len__(self):
        return len(self.sections)

    def __getitem__(self, conf):
        if len(conf) == 2:
            section, entry = conf
            return self.pw[section][entry]
        else:
            section = conf
            return self.pw[section]

    def __setitem__(self, sec_key, entry_val):
        section, entry_key = sec_key
        if section not in self.sections: self.sections.append(section)
        if section not in self.pw.keys(): self.pw[section] = {}
        self.pw[section][entry_key] = entry_val