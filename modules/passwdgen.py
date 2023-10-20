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

# Provides Functions to generate passwords

import random
from pathlib import Path

# Type - 1 : Random Characters

small_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y','z']
capital_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O','P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['1', '2', '3','4', '5', '6', '7', '8', '9', '0']
special_chars = ['!', '@', '#', '$', '%', '^', '&', '*', '-', '+', '_', '<', '>', ';', ':', '/', '?', '|', '~']
chars = small_letters + capital_letters + numbers + special_chars

# Uses Characters to generate password

def gen_random_password(length):
    password = ''
    for i in range(length):
        password += random.choice(chars)
    return password


# Type - 2 : Random Words

word_dict = []


def load_dictionary(PATH):
    dict_file = PATH / 'assets' / 'word_lists/wordlist.txt'
    global word_dict
    with open(dict_file, 'r') as file:
        for word in file:
            word = word.strip()
            word_dict.append(word)

# Uses a dictionary of words to generate password
# Uses modified version of - https://gist.github.com/deekayen/4148741

def choose_until_length(length):
    word = random.choice(word_dict)
    while len(word) < length:
        word = random.choice(word_dict)
    word = word.capitalize()
    return word

def gen_dict_password(num_words, seperator='-', min_word_length=3):
    password = ''
    if seperator == 'None':
        seperator = ''
    for i in range(num_words):
        password += choose_until_length(min_word_length) + seperator

    if seperator != 'None':
        password = password[:-1]
    return password

# Type - 3 : Numerical Pin

def gen_pin(num):
    pin = ''
    for i in range(num):
        pin += random.choice(numbers)
    return pin