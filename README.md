# T.U.R.P.O - Trustworthy Utility for Reliable Password Organisation

## A simple to use, feature-rich, free and Open-Source Password Management Software for Linux and Windows.

> Currently in Beta Phase, some of the features might be missing or unstable, use it for testing and fun only !

### Installation and Usage Instructions

#### 1. Install from binaries (Windows and Linux) ####

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
- [x] Build and Release V1.0-beta1 Binaries (Done! - 23/10/2023)
- [ ] Code Cleanup and Refractoring
- [ ] Complete Settings page
- [ ] Build and Release V1.0-beta2 Binaries

#### Always Under Progress
- Bug Fixes
- Testing
- Better Documentation

### Releases Plan
Currently lots of features are planned and pending. They will be added and tested in subsequent beta releases. Expect a bunch of beta versions over next several weeks before the first major release.