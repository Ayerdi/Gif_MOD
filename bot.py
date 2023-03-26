import os
import datetime
import asyncio
import discord
from dotenv import load_dotenv
from flask import Flask

app = Flask(__name__)


@app.route('/')
def run_bot():
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')

    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    whitelist = []

    def remove_from_whitelist(name):
        whitelist.remove(name)
        print_whitelist()

    def print_whitelist():
        print(f"Whitelist: {', '.join(whitelist)}")

    @client.event
    async def on_ready():
        print(f'{client.user} has connected to Discord!')

    @client.event
    async def on_message(message):
        if message.author.bot:
            return
        if message.content.startswith('!whitelist'):
            await message.channel.send(f"Whitelist: {', '.join(whitelist)}")
        elif message.content.startswith('!clearwhitelist'):
            whitelist.clear()
            await message.channel.send("Whitelist cleared.")
            print_whitelist()
        elif 'https://tenor.com/view/' in message.content:
            if message.author.name not in whitelist:
                whitelist.append(message.author.name)
                await message.channel.send(f"{message.author.mention} has been whitelisted for sending a GIF.")
                loop = asyncio.get_event_loop()
                loop.call_later(28800, remove_from_whitelist,
                                message.author.name)
                print_whitelist()

    @client.event
    async def on_voice_state_update(member, before, after):
        if not member.bot and member.name not in whitelist:
            if after.channel is not None and after.channel != before.channel:
                # Mover al miembro de vuelta al canal anterior
                await member.move_to(before.channel)
                # Enviar un mensaje de advertencia
                await member.send("Hola! Soy el moderador de Home Sweet Home. Necesitas enviar un gif por el canal de texto para poder acceder a los canales de voz.")

    client.run(TOKEN)
