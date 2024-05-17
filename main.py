import discord
from discord.ext import commands
import re
import json

bot = commands.Bot(intents=discord.Intents.all())

config = json.load(open("config.json","r"))

@bot.event
async def on_ready():
    print(f'Bot {bot.user} está listo y conectado.')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    invite_links = re.findall(r'(https?://)?(www\.)?(discord\.(gg|com)/invite/[^\s]+)', message.content)
    for link in invite_links:
        invite_code = link[2].split("/")[-1]

        try:
            invite = await bot.fetch_invite(invite_code)

            if any(keyword in (invite.guild.name + invite.guild.description).lower() for keyword in config["keywords"]):
                await message.author.ban(reason="Enlace a servidor pornografico detectado")
                await message.delete()
                await message.channel.send(f"El usuario {message.author.mention} ha sido baneado por enviar un enlace a un servidor inapropiado.")
        except discord.NotFound:
            pass
    await bot.process_commands(message)

bot.run(config["TOKEN"])