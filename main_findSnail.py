import re, itertools, os , csv
from random import random
import discord
from discord.ext import commands

#Config constants
TOKEN = ""
CONSOLE_CSV_DELIM = '>'

#Working directory
DIR_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)))
TOKEN_PATH = os.path.join(DIR_PATH,"Config","token.txt")

if not os.path.exists(TOKEN_PATH):
    with open(TOKEN_PATH, "w+") as f: 
        f.write('')
with open(TOKEN_PATH,"r") as f:
    TOKEN = f.readline().rstrip()
####################

bot = commands.Bot(command_prefix="!")

mostSnailedMessageID = 0
mostSnailedUserPostsID = 0
mostSnailedUserSnailsID = 0
mostSnailedMessageNo = 0
mostSnailedUserPostsNo = 0
mostSnailedUserSnailsNo = 0

@bot.command()
async def snailreport(ctx):
    list = ""
    messages = [message async for message in channel.history(limit=123)]

    channel = bot.get_channel(795647732063666196)
    messages = await ctx.channel.history(oldest_first=True).flatten()

    for msg in messages:
        if word in msg.content:
            print(msg.jump_url)

    embed=discord.Embed(title="Console List", description=list, color=0xFF1694)
    await ctx.channel.send(embed=embed)

@bot.event
async def on_ready():
    print(f'{bot.user} succesfully logged in!')


#Start
bot.run(TOKEN)