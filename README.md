# WinTradeBot
# Written by Idlan bin Hafiz
**WinTradeBot** is a Python bot designed for automating win trading on a World of Warcraft private server. The bot automates the process of queueing, detecting in-game elements, and trading wins between players.

## Features
- **Automated queueing and requeueing** for battlegrounds or arenas.
- **Image recognition** to detect in-game elements such as player frames, buttons, and map coordinates.
- Supports **multiple game clients** simultaneously.

## Installation
1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/iddysus/WinTradeBot.git
   cd WinTradeBot
2. Install the required Python libraries:
   pip install -r requirements.txt

##Usage
Prepare your World of Warcraft private server client.
Adjust the bot settings in config.json (or directly in the script) to match your screen resolution and game window.
Start the bot:
bash
Copy code
python master.py
Monitor the bot as it automates the win-trading process.

##Files Included
master.py: Main script to run the bot.
openclients.py: Handles multiple game clients.
reference_maps/: Contains the reference images used for OpenCV image detection (maps, player frames, etc.).
testing_screenshots/: Sample screenshots used during testing.
ff_fanfare.mp3: Audio file used in the bot (can be any sound or notification).
Contributing
Feel free to open an issue or submit a pull request for improvements or bug fixes.

