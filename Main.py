# bot.py
import os
import discord
import math
import praw
import array
import CommandCreator as creator
from SqlLoader import SqlLoader as sql
from random import random as rand
from discord.ext.commands import Bot
from discord.ext import commands
from dotenv import load_dotenv

# TODO: ADD COOLDOWN FOR COMMANDS (RUNS ON RPI, CANT HANDLE MUCH)

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
USER_AGENT = 'tymmc\'s discord bot'
REDDIT_SECRET = os.getenv('REDDIT_SECRET')
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')

r = praw.Reddit(user_agent=USER_AGENT,
                     client_id=REDDIT_CLIENT_ID,
                     client_secret=REDDIT_SECRET)

# The custom client
class CustomClient(discord.Client):

    async def on_ready(self):
        print(f'{client.user} has connected to Discord!')
        self.sqldb = sql()
        await client.change_presence(status=discord.Status.idle, activity=discord.Game(name="with the bros"))
        

    async def on_message(self, message):
        """ Sets up the custom embed for the Reddit command """
        def setupRedditEmbed(self, title, url, text=None):
            if text != None:
                embed = discord.Embed(title=f"{title}", color=0x4a3469, url=f"{url}", description=f"{text}")
            else:
                embed = discord.Embed(title=f"{title}", color=0x4a3469, url=f"{url}")
            embed.set_author(name="Reddit",icon_url="https://cdn4.iconfinder.com/data/icons/materia-flat-social-free/24/038_014_reddit_social_network_android_material-512.png")
            embed.set_image(url=f"{url}")
            embed.set_footer(text="Hanabana")
            return embed

        async def reddit(self):
            """ Reddit command (allows to get items from a subreddit, search through a subreddit, or search through all of reddit) """
            try:
                if arg1 == 'subreddit': # browse a subreddit
                    subList = []
                    for submission in r.subreddit(arg2).hot(limit=50):
                        subList.append(submission)
                    randnum = round(rand() * (len(subList)-1))
                    title = subList[randnum].title
                    text = subList[randnum].selftext[:1000]
                    if len(text) > 1000:
                        text += "..."
                    url = subList[randnum].url
                    embed = setupRedditEmbed(self, title, url, text=text)
                    subList.clear()
                elif arg1 == 'search': # search through all
                    subList = []
                    subs = r.subreddit('all')
                    for x in subs.search(arg2, limit=50):
                        subList.append(x)
                    randnum = round(rand() * (len(subList)-1))
                    title = subList[randnum].title
                    text = subList[randnum].selftext[:1000]
                    if len(text) > 1000:
                        text += "..."
                    url = subList[randnum].url
                    embed = setupRedditEmbed(self, title, url, text=text)
                    subList.clear()
                elif arg1 == 'subsearch': # search through a specific subreddit
                    subList = []
                    subs = r.subreddit(args[2])
                    for x in subs.search(arg3, limit=50):
                        subList.append(x)
                    randnum = math.floor(rand() * (len(subList)-1))
                    try:
                        title = subList[randnum].title
                        text = subList[randnum].selftext[:1000]
                        if len(text) > 1000:
                             text += "..."
                        url = subList[randnum].url
                        embed = setupRedditEmbed(self, title, url, text=text)
                    except IndexError:
                        await message.channel.send(f"Sorry but the specimen '{arg3}' does not exist on /r/{args[2]}!")
                        return
                    subList.clear()
                else:
                    await message.channel.send("Invalid argument(s)")
                    return
            except NameError as e:
                print(e)
                await message.channel.send("Missing argument(s)")
                return
            await message.channel.send(embed=embed)

        # TODO: add @ implementation
        async def check_rank(self):
            """ Checks a user's rank """
            user_xp = self.sqldb.get_rank(message.author.id, message.guild.id)
            user_xp_to_next = user_xp % 500
            user_level = math.floor(user_xp/500)
            embed = discord.Embed(title=f"{message.guild}", color=0x4a3469)
            embed.set_author(name=f"{message.author}", icon_url=f"https://cdn.discordapp.com/avatars/{message.author.id}/{message.author.avatar}.png?size=128")
            embed.set_thumbnail(url=f"https://cdn.discordapp.com/avatars/{message.author.id}/{message.author.avatar}.png?size=128")
            embed.add_field(name="Level", value=f"{user_level}", inline=True)
            embed.add_field(name="Total XP", value=f"{user_xp}", inline=True)
            embed.add_field(name="XP for next level", value=f"{user_xp_to_next}/500", inline=False)
            embed.set_footer(text="Hanabana")
            await message.channel.send(embed=embed)

        async def help(self):
            """ Help command displays all commands available in a server """
            embed = discord.Embed(title=" ", description="All commands start with '?'", color=0x4a3469)
            embed.set_author(name="Help Commands")
            embed.set_thumbnail(url="https://www.tubefilter.com/wp-content/uploads/2020/02/pewdiepie-return-youtube.jpg")
            try:
                if arg1 == "1":
                    self.help_fields(embed)
                    await message.channel.send(embed=embed)
                    return
                cmds = self.sqldb.get_commands(message.guild.id)
                start_index = (int(arg1)-2) * 8
                end_index = (int(arg1)-1) * 8
                splice = cmds[start_index:end_index]
                if len(splice) == 0:
                    raise IndexError
                for x in splice:
                    embed.add_field(name=f"{x[1]}", value=f"{x[4]}", inline=False)
                next_page = int(arg1) + 1
                embed.set_footer(text=f"Hanabana, '?help {next_page}' for more")
            except NameError:
                help_fields(self, embed)
            except IndexError:
                help_fields(self, embed)
            except ValueError:
                help_fields(self, embed)
            await message.channel.send(embed=embed)

        def creation_fields(self, embed):
            """ These commands are displayed for those interested in creating their own commands """
            embed.add_field(name="help [number]", value="Go through the help pages", inline=False)
            embed.add_field(name="level", value="Check your level in the server", inline=False)
            embed.add_field(name="reddit search {search}", value="Search something up on reddit", inline=False)
            embed.add_field(name="reddit subreddit {subreddit}", value="Browse on a certain subreddit", inline=False)
            embed.add_field(name="reddit subsearch {subreddit} {search}", value="Search through a specific subreddit", inline=False)
            embed.set_footer(text="Hanabana, ?creation")

        def help_fields(self, embed):
            """ These are the basic help commands  """
            embed.add_field(name="help [number]", value="Go through the help pages", inline=False)
            embed.add_field(name="level", value="Check your level in the server", inline=False)
            embed.add_field(name="reddit search {search}", value="Search something up on reddit", inline=False)
            embed.add_field(name="reddit subreddit {subreddit}", value="Browse on a certain subreddit", inline=False)
            embed.add_field(name="reddit subsearch {subreddit} {search}", value="Search through a specific subreddit", inline=False)
            embed.set_footer(text="Hanabana, '?help 2' for more")

        if message.author == client.user:
            return

        # Adds xp to the user, as they sent a message
        self.sqldb.add_xp_to_user(message.author.id, message.guild.id)

        # TODO: handle custom calls
        if message.content[0:1] == '?':
            # Handles if the message is a command
            args = message.content[1:].split()
            cmd = args[0]
            try: 
                arg1 = args[1]
            except IndexError:
                print(f'{message.author} did not provide arg1')
            try: 
                arg2 = message.content[message.content.index(args[2]):]
            except IndexError:
                print(f'{message.author} did not provide arg2')
            try:
                arg3 = message.content[message.content.index(args[3]):]
            except IndexError:
                print(f'{message.author} did not provide arg3')
            
            try:
                await message.channel.send(embed=self.sqldb.run_command(message.guild.id, message.author.id, args[1], cmd))
                return
            except IndexError:
                try:
                    await message.channel.send(embed=self.sqldb.run_command(message.guild.id, message.author.id, None, cmd))
                    return
                except TypeError:
                    print("Not found in table")
            except TypeError as e:
                print("Not in table")
            # The switch for the commands
            if cmd == 'reddit':
                await reddit(self)
            elif cmd == 'level':
                await check_rank(self)
            elif cmd == 'help':
                await help(self)
            else:
                await message.channel.send('Command does not exist.')
                

client = CustomClient()

client.run(TOKEN)