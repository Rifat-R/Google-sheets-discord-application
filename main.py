import disnake
from disnake.ext import commands
import os
from settings import config
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

intents = disnake.Intents.default()
intents.members = True
intents.message_content = True

bot_prefix = "."

bot = commands.Bot(command_prefix = bot_prefix, intents=intents)

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        print(f"cogs.{filename[:-3]} Loaded")
        bot.load_extension(f"cogs.{filename[:-3]}",) #Loads up all the cogs (modules) in the /cogs directory


# Reloads all the cogs (modules) in the /cogs directory
@commands.has_permissions(administrator=True)
@bot.command()
async def reload(ctx):
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            bot.reload_extension(f"cogs.{filename[:-3]}")
            print(f"Loaded up file : cogs.{filename}")

bot.run(BOT_TOKEN)
