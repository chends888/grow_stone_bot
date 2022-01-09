# Grow Stone Online Bot

Bot for auto-combining stones.

This bot has only been tested with Windows, might work with Linux, but some modifications on the code would be needed.

## Emulator Setup
- Download an Android emulator (I'm using LDPlayer. It will work for other, but some minor ajustments might be made)
- Set the emulator to 1600x900 (again, the bot will work for other configs, but some ajustments will be needed due to window positioning)
- Put the emulator window to the left side of your screen, align the window to the left margin of your screen. Now, from the right side of the emulator, click and drag it-s margin to resize it, so it fills the entire height of your screen. An example is shown below:
![emulator_setup](https://i.imgur.com/Yqs6FHx.png)

- As the images shows, leave your bag opened, and without any items selected (green background induces errors on image detection)
- Also, use the new UI (can be changed from in-game settings)

## Python environment setup
In order to run the bot, you'll need Python and some additional libraries.
To install Python on your machine, head over to: https://www.python.org/downloads/windows/ and download Python 3 (Check the box "Add Python 3.8 to PATH")

I would recommend you to install VSCode, which is a text editor that also has a command line, useful for installing required libraries and running the bot. To install it, go to https://code.visualstudio.com/download and download the Windows User version (you're probably using a 64-bit computer, so download the 64-bit version).

Open VSCode, on the left side, click the two files icon and "Open a Folder"


`pip install pywinauto`
