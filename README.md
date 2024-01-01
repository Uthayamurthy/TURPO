# T.U.R.P.O - Trustworthy Utility for Reliable Password Organisation

## A simple to use, feature-rich, free and Open-Source Password Management Software for Linux and Windows.

> Currently in Beta Phase, some of the features might be missing or unstable, use it for testing and fun only !

### Features :-

- **AES256 bit Encryption** on plane text file - secure and future proof (no proprietary/strange custom file type)
- **Completely Private and Offline** - Doesn't need Internet to work. No data is collected. Your credentials belong to you and you only !
- **Simple** to use UI
- For now, supports **3 types of Credentials - Email, Social Media, Phone Pin**
- Has a **Powerful Password Generator** tool with support to 3 different types of  passwords (Random Character, Random Word and Random Number).
- Has both **Encrypted and Unencrypted Backup** option

### Installation and Usage Instructions
> For now, automatic updates are available only for the snap version.
#### 1. Install the snap package (Linux Users only !! Recommended ) ####

T.U.R.P.O is now available as a snap package !!

[![Get Turpo from the Snap Store](https://snapcraft.io/static/images/badges/en/snap-store-black.svg)](https://snapcraft.io/turpo-app)

To install just run :

```
sudo snap install turpo-app --beta
```

#### 2. Install from binaries (Windows and Linux) ####

1. Go to Releases Page - https://github.com/Uthayamurthy/TURPO/releases
2. From the Assets, download the suitable binary zip. Extract the zip file.
3. Linux Users - Make the installation script executable and then run it.
```
chmod +x install.sh
./install.sh
```
   Windows Users - Just double click the installer and follow along, you will install it.

#### 2. Use From source (For Advanced Users only ! Works on Windows and Linux) ####

It is assumed that you already have python 3.7+ and git installed.

1. (optional but recommended) Create a virtual environment and use it.
2. Install the requirements -
```
pip install ttkbootstrap pycryptodome pyperclip
```
3. Clone this Repo -
```
git clone https://github.com/Uthayamurthy/TURPO.git
```
4. Go to the downloaded directory and run the main.py file
```
cd main.py # For Linux ! Windows users use chdir
python main.py
```

### Current Roadmap

Refer to [ROADMAP.md](ROADMAP.md) for project Roadmap.

Want to track the latest progress ? Check the development branch (https://github.com/Uthayamurthy/TURPO/tree/development) ...

#### Always Under Progress
- Bug Fixes
- Testing
- Better Documentation

### Releases Plan
Currently lots of features are planned and pending. They will be added and tested in subsequent beta releases. Expect a bunch of beta versions over next several weeks before the first major release.

### Screenshots
#### 1. Password Management
![Main Screen](/Images/main-screen.png)
Overview
![View Screen](/Images/credential-view.png)
Credential View 
![Create Screen](/Images/new-credential.png)
New Credential

#### 2. Password Generation Tools
![Password Generation 1](/Images/pass-generator1.png)
Random Character Passwords
![Password Generation 2](/Images/pass-generator2.png)
Random Word Passwords
![Password Generation 3](/Images/pass-generator3.png)
Random Numeric Pin

#### 4. Backup Tool
![Backup Screen](/Images/backup-tool.png)
Encrypted and Unencrypted Backup tool 

#### 5. Settings Page
![Settings Screen](/Images/settings.png)
