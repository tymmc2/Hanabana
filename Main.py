# bot.py
import discord
import os
import sqlite3
from MainCog import MainCog
from discord.ext import commands
from discord.ext.commands import errors, CheckFailure
from dotenv import load_dotenv

# TODO: ADD COOLDOWN FOR COMMANDS (RUNS ON RPI, CANT HANDLE MUCH)

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

bot = commands.Bot(command_prefix='?')
bot.remove_command("help")
bot.add_cog(MainCog(bot))

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name="with the bros"))

@bot.event
async def on_command_error(ctx, error):
    if is_in_server(ctx.message.content[1:], ctx.guild.id):
        return
    if isinstance(error, errors.CommandNotFound):
        await ctx.channel.send('Command not found!')
    if isinstance(error, errors.MissingRequiredArgument):
        await ctx.channel.send('Missing argument(s)!')
    if isinstance(error, CheckFailure):
        await ctx.channel.send('You do not have permissions to this command!')

def is_in_server(name, guild):
    conn = sqlite3.connect('commands.db')
    c = conn.cursor()
    c.execute(f"SELECT * FROM commands WHERE guild = '{guild}' AND command = '{name}'")
    if len(c.fetchall()) > 0:
        return True
    return False

bot.run(TOKEN)