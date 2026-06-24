import discord
from discord.ext import commands
import asyncio

TOKEN = "YOUR_BOT_TOKEN"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

async def main():
    async with bot:
        await bot.load_extension("cogs.winlog")
        await bot.start(TOKEN)

asyncio.run(main())
