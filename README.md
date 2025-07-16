# Discord Toxxer & Toxx Message Scraper

![Discord](https://discord.com/assets/2c21aeda16de354ba5334551a883b481.png)

## Overview

My Python script is designed to work with **Discord user account tokens** (not bot tokens) and provides two main funcs:

1. **Message Scraper**  
   Scrapes messages from a specified Discord server (you input the guild ID) channels using a main user token, scans messages for blacklisted words, and saves matched message links and details to a file (created by itself).

2. **Mass Reporter**  
   Allows mass reporting of specific messages or entire guilds using multiple user tokens gotten from a file. You can send reports for multiple reasons and however much times you want (per token).

Add me on discord for any help: arman.gov
---

## Features

- Gets multiple user tokens from `tokens.txt`.
- Uses the first token as the main token for message scraping so please dont put a random token first then start aping.
- Reads blacklisted words from `blacklisted.txt` to filter messages.
- Saves matched messages to `toxxable.txt` with message links and person who sent info.
- Reports messages or servers on Discord’s API v10 `/report` endpoint.
- Supports multiple report reasons (spam, harassment, child abuse, etc.).
- Works asynchronously for the best outcome.

---

## Requirements

- Python 3.8 or higher
- `aiohttp` package (`pip install aiohttp`)

---

## Setup

1. **Prepare your token files:**

   - `tokens.txt` — Place one Discord user token per line.  
     **Note:** These are user account tokens, not bot tokens so dont be dumb lol.

   - `blacklisted.txt` — Place blacklisted words to scan for, one per line.

2. **Run the script:**

   ```bash
   python your_script_name.py
