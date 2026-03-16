import discord
from discord.ext import tasks
from dotenv import load_dotenv
import os
import asyncio
import random
import json

load_dotenv()
token = os.getenv("BOT_TOKEN")

CHANNEL_ID = # Paste here ID of channel

bot = commands.Bot(command_prefix="!")

COUNT_FILE = "count_day.json"


def load_count():
    if os.path.exists(COUNT_FILE):
        try:
            with open(COUNT_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {"day": 0}


def save_count(data):
    try:
        with open(COUNT_FILE, "w") as f:
            json.dump(data, f)
    except IOError as e:
        print(f"[warn] Could not save state: {e}")


count_data = load_count()


@tasks.loop(hours=24)
async def collect():
    channel = bot.get_channel(CHANNEL_ID)

    if not channel:
        print("Канал не найден. Проверь ID.")
        return

    day = count_data["day"]

    async with channel.typing():
        await asyncio.sleep(random.uniform(3, 6))

    await channel.send(f"The {day} when I`m wait your answer.")

    count_data["day"] += 1
    save_count(count_data)


@bot.event
async def on_ready():
    print(f"Start how {bot.user}")
    collect.start()


bot.run(token)
