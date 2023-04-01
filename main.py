from imports import *
from config import *
from utils import *
import datetime
from datetime import datetime


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    change_status.start()
    loop = asyncio.get_event_loop()
    loop.call_later(57600, check_time_whitelist)


def check_time_whitelist():
    whitelist = load_whitelist()
    current_time = time.time()
    for user_id, name, added_time in whitelist:
        time_left = current_time - added_time
        horas = 16
        time_limit = horas * 3600 
        if time_left > time_limit:
            remove_from_whitelist(user_id, added_time)


@client.command()
async def piing(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')



@client.command()
async def add(ctx):
    # check if user has Admin role
    # user_roles = [role.name for role in ctx.author.roles]
    # if "Admin" in user_roles:
    if ctx.message.author.id == 270284648053997579:  # TODO maybe cambiar esto por un rol directamente
        if ctx.message.mentions != 0:
            whitelist = load_whitelist()
            id_list = []
            for user in whitelist:
              print(user)
              id_list.append(int(user[0]))
            print(id_list)
            for user in ctx.message.mentions:
              print(type(user.id))
              if user.id in id_list:
                await ctx.message.channel.send(f"{user.name}, ya está en la lista blanca.")
              else:
                whitelist.append((user.id, user.name, time.time()))
            save_whitelist(whitelist)
            # convert list into string
            whitelist_string = ', '.join(name for _, name, _ in whitelist)
            await ctx.send(f"Whitelist updated: {whitelist_string}")
            print_whitelist(whitelist)
        else:
            await ctx.send("No se ha mencionado ningún usuario.")


@client.command()
async def clear_whitelist(ctx):
    save_whitelist([])
    await ctx.send("Whitelist cleared.")


@client.command()
async def show_whitelist(ctx):
    whitelist = load_whitelist()
    await ctx.send(f"Whitelist: {', '.join(name for _, name, _ in whitelist)}")


@client.command()
async def time_left(ctx):
    whitelist = load_whitelist()
    await tiempo_restante_whitelist(whitelist)  # TODO: revisar

@client.command()
async def kick(ctx, member: discord.Member):
    if member.voice is not None:
        await member.move_to(None)

@client.event
async def on_message(message):
    whitelist = load_whitelist()
    if message.author.bot:
        return
    if 'https://tenor.com/view/' in message.content:
        if message.author.id not in [id for id, _, _ in whitelist]:
            if message.channel.id != 792734128193011712:  #canal general = 613130176808878109
                deleted_message_content = message.content
                await message.delete()
                destination_channel = message.guild.get_channel(613130176808878109)
                user_mention = message.author.mention
                channel_mention = message.channel.mention
                await destination_channel.send(f"{user_mention} ha enviado el siguiente gif por el canal {channel_mention}:\n{deleted_message_content}\nTen más cuidado la próxima vez.", reference=message)
            else:
                whitelist.append((message.author.id, message.author.name, time.time()))
                save_whitelist(whitelist)
                print_whitelist(whitelist)
    await client.process_commands(message)


@client.event
async def on_voice_state_update(member, before, after):
    whitelist = load_whitelist()
    if not member.bot and member.name not in [name for _, name, _ in whitelist]:
        if after.channel is not None and after.channel != before.channel:
            # Mover al miembro de vuelta al canal
            await member.move_to(before.channel)
            # Enviar un mensaje de advertencia
            await member.send("Hola! Soy el moderador de Home Sweet Home. Necesitas enviar un gif por el canal de texto para poder acceder a los canales de voz.")

status = cycle(['Inspeccionando Gifs', 'Verificando Gifs', 'Revisando Gifs'])


@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


def get_time_left(user_id):
    for i, (id, name, time_added) in enumerate(whitelist):
        if id == user_id:
            remove_time = time_added + timedelta(hours=16)
            time_left = remove_time - datetime.now()
            return time_left
    return None



client.run(TOKEN)