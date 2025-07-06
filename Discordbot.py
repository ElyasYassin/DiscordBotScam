import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
INTENTS = discord.Intents.default()
INTENTS.message_content = True
INTENTS.guilds = True
INTENTS.members = True

bot = commands.Bot(command_prefix='!', intents=INTENTS)

# Add scam message patterns (lowercase for case-insensitive check)
SCAM_KEYWORDS = [
    "macbook", "first come first serve", "dm if you are interested",
    "give out", "i want to give", "can't afford", "perfect health",
    "i just got a new", "for free", "alongside a charger"
]

# Helper to check if a message is a likely scam
def is_scam_message(msg: str):
    msg = msg.lower()
    return all(keyword in msg for keyword in SCAM_KEYWORDS[:3])  # Relaxable logic

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

@bot.event
async def on_message(message):
    print(f"Received message: {message.content} from {message.author}")  # Debug print

    if message.author == bot.user:
        return

    if is_scam_message(message.content):
        print("Scam detected!")  # Debug print
        try:
            await message.author.ban(reason="Scam message detected.")
            await message.channel.send(f'🚨 {message.author} has been banned for scamming.')
        except Exception as e:
            print(f"Error banning user: {e}")

    await bot.process_commands(message)

if __name__ == '__main__':
    bot.run(TOKEN)