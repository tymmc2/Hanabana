import discord
import string
import math
from random import random as rand

class CommandTemplate:
    """ This class holds the template for the commands """
    def text_command(self):
        """ This command returns a set sentence when called. """
        embed = discord.Embed(title=" ", description=self.info, color=0x4a3469)
        embed.set_footer(text=f"Hanabana | ?{self.name}")
        return embed
    
    def video_command(self):
        """ This command returns a given video when called. """
        embed = discord.Embed(title=self.info, color=0x4a3469, url=self.url)
        embed.set_footer(text=f"Hanabana | ?{self.name}")
        return embed

    def image_command(self):
        """ This command returns a given image. It also supports multiple images if the command creator add ';' between image urls. """
        embed = discord.Embed(title=f"{self.info}", color=0x4a3469)
        if ';' in self.url:
            split_version = self.url.split(';')
            random_val = math.floor(rand() * len(split_version))
            self.url = split_version[random_val]
        embed.set_image(url=self.url)
        embed.set_footer(text=f"Hanabana  | ?{self.name}")
        return embed

    def random_command(self):
        """ This command when called return a random value within a specified range. """
        chance = round(rand() * (self.rand_max - self.rand_min), 2) + self.rand_min
        if "{chance}" in self.info:
            self.info = self.info.replace("{chance}", f"{chance}")
        if "{minutes}" in self.info or "{seconds}" in self.info or "{hours}" in self.info:
            seconds = round(chance)
            minutes = seconds/60
            hours = math.floor(minutes/60)
            minutes = math.floor(minutes % 60)
            seconds = math.floor(seconds % 60)
            self.info = self.info.replace("{minutes}", f"{minutes}")
            self.info = self.info.replace("{seconds}", f"{seconds}")
            self.info = self.info.replace("{hours}", f"{hours}")
        embed = discord.Embed(title=" ", description=self.info, color=0x4a3469)
        embed.set_footer(text=f"Hanabana | ?{self.name}")
        return embed

    def __init__(self, user, arg1, name, type, info, description, url=None, min=None, max=None):
        """ Sets up the arguments and saves them """
        self.user = user
        self.arg1 = arg1
        self.name = name
        self.type = type
        self.info = info
        self.description = description
        self.url = url
        self.rand_min = min
        self.rand_max = max
        if "{user}" in self.info and self.arg1 != None:
            self.info = self.info.replace("{user}", f"{self.arg1}")
        elif "{user}" in self.info:
            self.info = self.info.replace("{user}", f"<@{user}>")
        if type == 'text':
            self.embed = self.text_command()
        elif type == 'video':
            self.embed = self.video_command()
        elif type == 'image':
            self.embed = self.image_command()
        elif type == 'random':
            self.embed = self.random_command()
        else:
            self.embed = None

