import aiohttp
import asyncio
import os
import sys

PURPLE = "\033[95m"
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

BANNER = """
█████  ██████  ███    ███  █████  ███    ██ 
██   ██ ██   ██ ████  ████ ██   ██ ████   ██ 
███████ ██████  ██ ████ ██ ███████ ██ ██  ██ 
██   ██ ██   ██ ██  ██  ██ ██   ██ ██  ██ ██ 
██   ██ ██   ██ ██      ██ ██   ██ ██   ████ 
                                             
                                             
"""

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

with open('tokens.txt', 'r') as f:
    tokens = [line.strip() for line in f.readlines()]

with open('blacklisted.txt', 'r') as f:
    blacklist = [line.strip() for line in f.readlines()]

main_token = tokens[0]

reason_map = {
    "spam": 0,
    "child_abuse": 1,
    "harassment": 2,
    "hate_speech": 3,
    "self_harm": 4,
    "ip_violation": 5,
    "other": 6
}

def get_reason_code(input_str):
    return reason_map.get(input_str.lower(), 6)

async def scrape(guildid):
    headers = {"Authorization": main_token}
    async with aiohttp.ClientSession(headers=headers) as session:
        url = f"https://discord.com/api/v10/guilds/{guildid}/channels"
        async with session.get(url) as resp:
            if resp.status != 200:
                print(f"{RED}Failed to fetch channels. Status: {resp.status}{RESET}")
                return
            channels = await resp.json()
            total = 0
            matched = 0
            for channel in channels:
                cid = channel['id']
                msg_url = f"https://discord.com/api/v10/channels/{cid}/messages?limit=100"
                async with session.get(msg_url) as msg_resp:
                    if msg_resp.status != 200:
                        print(f"{RED}Failed to fetch messages for channel {cid}. Status: {msg_resp.status}{RESET}")
                        continue
                    messages = await msg_resp.json()
                    for m in messages:
                        content = m.get('content', '')
                        total += 1
                        if any(word in content for word in blacklist):
                            matched += 1
                            with open('toxxable.txt', 'a', encoding='utf-8') as f:
                                link = f"https://discord.com/channels/{guildid}/{cid}/{m['id']}"
                                f.write(f"{link} - ({m['author']['username']} - {content})\n")
            print(f"{GREEN}Scraping complete! Messages checked: {total}, matched blacklist: {matched}.{RESET}")

async def reportMessage(messageid, channelid, reason, amount):
    success_count = 0
    fail_count = 0
    for token in tokens:
        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }
        json_data = {
            "channel_id": channelid,
            "message_id": messageid,
            "reason": reason
        }
        async with aiohttp.ClientSession() as session:
            for _ in range(amount):
                try:
                    resp = await session.post("https://discord.com/api/v10/report", headers=headers, json=json_data)
                    if resp.status == 201 or resp.status == 204:
                        success_count += 1
                    else:
                        fail_count += 1
                except Exception:
                    fail_count += 1
    print(f"{GREEN}Toxx sent successfully: {success_count}{RESET}")
    if fail_count > 0:
        print(f"{RED}Failed toxx: {fail_count}{RESET}")

async def reportGuild(guildid, reason, amount):
    success_count = 0
    fail_count = 0
    for token in tokens:
        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }
        json_data = {
            "guild_id": guildid,
            "reason": reason
        }
        async with aiohttp.ClientSession() as session:
            for _ in range(amount):
                try:
                    resp = await session.post("https://discord.com/api/v10/report", headers=headers, json=json_data)
                    if resp.status == 201 or resp.status == 204:
                        success_count += 1
                    else:
                        fail_count += 1
                except Exception:
                    fail_count += 1
    print(f"{GREEN}Reports sent successfully: {success_count}{RESET}")
    if fail_count > 0:
        print(f"{RED}Failed reports: {fail_count}{RESET}")

def print_menu():
    clear()
    print(PURPLE + BANNER + RESET)
    print(f"{PURPLE}{'Made by arman.gov':^50}{RESET}")
    print(f"{PURPLE}{'-'*50}{RESET}")
    print(f"{PURPLE}{'Select an option:':^50}{RESET}")
    print(f"{PURPLE}{'-'*50}{RESET}")
    print(f"{PURPLE}[1]{RESET}  Scrape messages from a guild for blacklisted words")
    print(f"{PURPLE}[2]{RESET}  Mass report a specific message")
    print(f"{PURPLE}[3]{RESET}  Mass report a specific guild")
    print(f"{PURPLE}[4]{RESET}  Exit the program")
    print(f"{PURPLE}{'-'*50}{RESET}\n")

def main():
    while True:
        print_menu()
        choice = input("Enter your choice: ").strip().lower()
        clear()
        if choice == '1' or choice == 'scrape':
            guild_id = input("Enter the guild ID to scrape messages from: ").strip()
            print(f"{PURPLE}Starting message scrape for guild {guild_id}...{RESET}")
            asyncio.run(scrape(guild_id))
            input(f"\nPress Enter to continue...")
        elif choice == '2' or choice == 'report_message':
            message_id = input("Enter the message ID to report: ").strip()
            channel_id = input("Enter the channel ID where the message is: ").strip()
            print("Report reasons: spam, child_abuse, harassment, hate_speech, self_harm, ip_violation, other")
            reason_str = input("Enter the reason for reporting: ").strip()
            reason = get_reason_code(reason_str)
            amount = input("Enter how many reports to send per token: ").strip()
            if not amount.isdigit() or int(amount) < 1:
                print(f"{RED}Invalid amount. Must be a + integer.{RESET}")
                input(f"\nPress Enter to continue...")
                continue
            print(f"{PURPLE}Starting mass report of message {message_id}...{RESET}")
            asyncio.run(reportMessage(message_id, channel_id, reason, int(amount)))
            input(f"\nPress Enter to continue...")
        elif choice == '3' or choice == 'report_guild':
            guild_id = input("Enter the guild ID to report: ").strip()
            print("Report reasons: spam, child_abuse, harassment, hate_speech, self_harm, ip_violation, other")
            reason_str = input("Enter the reason for reporting: ").strip()
            reason = get_reason_code(reason_str)
            amount = input("Enter how many reports to send per token: ").strip()
            if not amount.isdigit() or int(amount) < 1:
                print(f"{RED}Invalid amount. Must be a + int.{RESET}")
                input(f"\nPress Enter to continue...")
                continue
            print(f"{PURPLE}Starting mass report of guild {guild_id}...{RESET}")
            asyncio.run(reportGuild(guild_id, reason, int(amount)))
            input(f"\nPress Enter to continue...")
        elif choice == '4' or choice == 'exit':
            print(f"{PURPLE}Exiting...{RESET}")
            sys.exit()
        else:
            print(f"{RED}Wrong choice, try again.{RESET}")
            input(f"\nPress Enter to continue...")

if __name__ == "__main__":
    main()
