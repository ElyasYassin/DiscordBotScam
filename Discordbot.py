import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Required for message content access

bot = commands.Bot(command_prefix="!", intents=intents)

SCAM_KEYWORDS = [
    "free nitro", "airdrop", "steam giveaway", "claim reward", "giveaway",
    "discord-nitro.com", "nitro-drop", "discord-giveaway", "discordgift"
]

def is_scam_message(content):
    content_lower = content.lower()
    return any(keyword in content_lower for keyword in SCAM_KEYWORDS)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if is_scam_message(message.content):
        await message.delete()
        await message.channel.send(f"🚫 Message from {message.author.mention} was removed due to suspected scam.")
        # Optional: Ban or warn user
        # await message.author.ban(reason="Scam message")

    await bot.process_commands(message)
    
if __name__ == "__main__":
    bot.run("YOUR_BOT_TOKEN")
