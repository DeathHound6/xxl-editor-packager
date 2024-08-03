# XXL Editor Packager

A script to automatically compress all game files outputted from [XXL Editor](https://github.com/AdrienTD/XXL-Editor) to prepare them faster for being used in game

## Prerequisites
- [Python version 3](https://www.python.org/downloads/release/python-3919/) (3.9+ recommended)

## Installing
- Clone this repository
    - Copy the cloned folder into the same folder where the [XXL Editor](https://github.com/AdrienTD/XXL-Editor) executable file is located
- Open a command line into the cloned folder
    - You can use the `cd` command to move around folders
    - You can use the `ls` command to display folders and files in the current folder
- Run `python3 -m pip install -r requirements.txt`
    - This will install any depdencies this program needs
- See [Usage Section](#usage)

## Usage
- Open the [XXL Editor](https://github.com/AdrienTD/XXL-Editor), make any desired changes, then save the given changes
- Open a command line into the cloned packager folder
    - You can use the `cd` command to move around folders
    - You can use the `ls` command to display folders and files in the current folder
- Run `python3 main.py` and follow the onscreen instructions
- Copy the files from the output folder into the game folder
    - For Wii ISO files, you will need to open the file using [7zip](https://7-zip.org/download.html) and copy the compressed files into the ISO
- Launch the game to view or test your modifications

## Supported Games
- Alice in Wonderland
    - [PC (from Steam)](https://store.steampowered.com/app/316030/Disney_Alice_in_Wonderland/)
    - Wii PAL
    - Wii NTSC

## Notes
- Copying uncompressed files into the game's files, will cause the game to crash
    - That's what this project will help to prevent!
- Some changes made in XXL Editor appear well, but for some currently unknown reason, cause the game to crash