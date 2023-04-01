import os
import discord
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = 1090042458022354994 #canal privado de pruebas

intents = discord.Intents.default()
intents.message_content = True
from discord.ext import commands
client = commands.Bot(command_prefix='/', intents=intents)
#client = discord.Client(intents=intents)