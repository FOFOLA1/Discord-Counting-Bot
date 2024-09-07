# Discord-Counting-Bot

Simple Discord bot for counting in decimal, hexadecimal or binary. It can handle as many channels/servers as you want.
The bot checks messages in the selected channel to see if the count is correct.

A huge credit goes to [TheFrederick (@thefrederick-git)](https://github.com/thefrederick-git), who really helped me out and explained to me how the bot is developing. I now understand how things work (I think :D).


##How to setup the bot
1. Clone this repository
2. Setup and activate the .venv
Windows:
```bash
python -m venv ./venv
.venv/Scripts/activate.bat
```
Linux:
```bash
python -m venv ./venv
source .venv/Scripts/activate
```
3. Install required packages
```bash
pip install -r requirements.txt
```
4. Enable bot
```bash
python main.py
```