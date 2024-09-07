# 🔢 Discord counting bot

Simple Discord bot for counting in decimal, hexadecimal or binary. It can handle as many channels/servers as you want.
The bot checks messages in the selected channel to see if the count is correct.

A huge credit goes to [TheFrederick (@thefrederick-git)](https://github.com/thefrederick-git), who really helped me out and explained to me how the bot is developing. I now understand how things work (I think :D).
- **Author:** [FOFOLA1 (@FOFOLA1)](https://github.com/fofola1)
- **Credit:** [TheFrederick (@thefrederick-git)](https://github.com/thefrederick-git)

## 🔧 How to run the bot
**1. Clone this repository**

**2. Setup and activate the .venv**

- **Windows:**
```bash
python -m venv .venv
".venv/Scripts/activate.bat"
```
- **Linux:**
```bash
python3 -m venv .venv
source ".venv/bin/activate"
```
**3. Install required packages**
```bash
pip install -r requirements.txt
```
**4. Enable bot**
```bash
python bot.py
```


## ⭐ Setup channel for counting and commands
I recommend using an empty channel or create a new one. These commands can use only server owner.

To setup counting channel use ``/setup`` command:
- channel: choose a channel for counting
- style: bin (binary), dec (decimal) od hex (hexadecimal)

If you want to reset counting, use ``/reset_count`` command:
- channel: choose a channel for resetting counting

If you don't want to counting channel, use ``/remove`` command:
- channel: choose a channel to remove counting

Commands ``/shutdown`` and ``/remove_all_channels`` are just for bot owners (you need to replace my ID with your own in ``is_bot_owner`` method to work):
