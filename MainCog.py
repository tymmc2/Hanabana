# bot.py
import os
import discord
import math
import praw
import CommandCreator as creator
from random import random as rand
from SqlLoader import SqlLoader as sql
from discord.ext.commands import errors, has_permissions, CheckFailure
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
USER_AGENT = 'Hanabana Discord Bot'
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_SECRET = os.getenv('REDDIT_SECRET')

r = praw.Reddit(user_agent=USER_AGENT,
                     client_id=REDDIT_CLIENT_ID,
                     client_secret=REDDIT_SECRET)

class MainCog(commands.Cog):
    """ The cog that handles built-in commands """
    def __init__(self, bot):
        self.bot = bot
        self.sqldb = sql()
    
    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def custom(self, ctx):
        """ These commands are displayed for those interested in creating their own commands """
        embed = discord.Embed(title=" ", description="All commands start with '?'", color=0x4a3469)
        embed.set_author(name="Help page")
        embed.set_thumbnail(url="https://i.ya-webdesign.com/images/anime-flowers-png-5.png")
        embed.add_field(name="command create {name}", value="Create a custom command", inline=False)
        embed.add_field(name="command edit {setting} {name} {value}", value="Edit a command. For more information, please check out the repo.", inline=False)
        embed.add_field(name="command remove {name}", value="Remove a custom command from your server", inline=False)
        embed.set_footer(text="Hanabana | ?custom")
        await ctx.channel.send(embed=embed)

    def help_fields(self, embed):
        """ These are the basic help commands """
        embed.add_field(name="help [number]", value="Go through the help pages", inline=False)
        embed.add_field(name="level", value="Check your level in the server", inline=False)
        embed.add_field(name="reddit search {search}", value="Search something up on reddit", inline=False)
        embed.add_field(name="reddit subreddit {subreddit}", value="Browse on a certain subreddit", inline=False)
        embed.add_field(name="reddit subsearch {subreddit} {search}", value="Search through a specific subreddit", inline=False)
        embed.set_footer(text="Hanabana | '?help 2' for more")

    def reddit_embed(self, title, url, text=None):
        if text != None:
            embed = discord.Embed(title=f"{title}", color=0x4a3469, url=f"{url}", description=f"{text}")
        else:
            embed = discord.Embed(title=f"{title}", color=0x4a3469, url=f"{url}")
        embed.set_author(name="Reddit",icon_url="https://cdn4.iconfinder.com/data/icons/materia-flat-social-free/24/038_014_reddit_social_network_android_material-512.png")
        embed.set_image(url=f"{url}")
        embed.set_footer(text="Hanabana")
        return embed

    @commands.command(pass_context=True)
    async def reddit(self, ctx, arg1, arg2, arg3=None):
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
                embed = self.reddit_embed(title, url, text=text)
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
                embed = self.reddit_embed(title, url, text=text)
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
                    embed = self.reddit_embed(title, url, text=text)
                except IndexError:
                    await ctx.channel.send(f"Sorry but the specimen '{arg3}' does not exist on /r/{args[2]}!")
                    return
                subList.clear()
            else:
                await ctx.channel.send("Invalid argument(s)")
                return
        except NameError as e:
            print(e)
            await ctx.channel.send("Missing argument(s)!")
            return
        await ctx.channel.send(embed=embed)

    @commands.command(pass_context=True)
    async def check_rank(self, ctx):
        """ Checks a user's rank """
        user_xp = self.sqldb.get_rank(ctx.author.id, ctx.guild.id)
        user_xp_to_next = user_xp % 500
        user_level = math.floor(user_xp/500)
        embed = discord.Embed(title=f"{ctx.guild}", color=0x4a3469)
        embed.set_author(name=f"{ctx.author}", icon_url=f"https://cdn.discordapp.com/avatars/{ctx.author.id}/{ctx.author.avatar}.png?size=128")
        embed.set_thumbnail(url=f"https://cdn.discordapp.com/avatars/{ctx.author.id}/{ctx.author.avatar}.png?size=128")
        embed.add_field(name="Level", value=f"{user_level}", inline=True)
        embed.add_field(name="Total XP", value=f"{user_xp}", inline=True)
        embed.add_field(name="XP for next level", value=f"{user_xp_to_next}/500", inline=False)
        embed.set_footer(text="Hanabana")
        await ctx.channel.send(embed=embed)

    @commands.command(pass_context=True)
    async def help(self, ctx, arg="1"):
        """ Help command displays all commands available in a server """
        embed = discord.Embed(title=" ", description="All commands start with '?'", color=0x4a3469)
        embed.set_author(name="Help page")
        embed.set_thumbnail(url="https://i.ya-webdesign.com/images/anime-flowers-png-5.png")
        try:
            if arg == "1":
                self.help_fields(embed)
                await ctx.channel.send(embed=embed)
                return
            cmds = self.sqldb.get_commands(ctx.guild.id)
            start_index = (int(arg)-2) * 8
            end_index = (int(arg)-1) * 8
            splice = cmds[start_index:end_index]
            if len(splice) == 0:
                raise IndexError
            for x in splice:
                embed.add_field(name=f"{x[1]}", value=f"{x[4]}", inline=False)
            next_page = int(arg) + 1
            embed.set_footer(text=f"Hanabana | '?help {next_page}' for more")
        except NameError:
            self.help_fields(embed)
        except IndexError:
            self.help_fields(embed)
        except ValueError:
            self.help_fields(embed)
        await ctx.channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        """ Sets up the custom embed for the Reddit command """
        if message.author == self.bot.user:
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
                    print("Command not found in table")
            except TypeError as e:
                print("Command not in table")
