from random import random
import os
from mathparse import mathparse
import discord
from discord.ext import commands
import wordlist
import autosnail
import banword
import console_bot

TOKEN = "" # From Config / token.txt

dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)))
token_path = os.path.join(dir_path,"Config","token.txt")

bot = commands.Bot(command_prefix="!")

if not os.path.exists(token_path):
    with open(token_path, "w+") as f: 
        f.write('')
with open(token_path,"r") as f:
    TOKEN = f.readline().rstrip()

# Discord functionality
def check_reply(message):
    if message.reference is not None and message.is_system :
        print(message.reference)
        return True
    return False

@bot.command()
async def leaderboards(ctx):
    embed_message = ""
    URLS_SCORES_PATH = os.path.join(dir_path,"Config","Scores")
    for filename in os.listdir(URLS_SCORES_PATH):
        f = os.path.join(URLS_SCORES_PATH, filename)
        if os.path.isfile(f):
           with open(f, "r+") as file:
                score = int(file.read().rstrip())
                user = await bot.fetch_user(int(filename))
                embed_message += str(user).split('#')[0] + ": " + str(score) + "\n"
    embed=discord.Embed(title="Snail Score List", description=embed_message, color=0xF6B600)     
    await ctx.channel.send(embed=embed)   

@bot.command()
async def consoles(ctx):
    await ctx.channel.send(embed=console_bot.console_list())

@bot.command()
async def calc(ctx, *, input: str):
    result = mathparse.parse(input, language='ENG')
    await ctx.channel.send(str(result))

@bot.command()
async def roll(ctx, *, inpt: str):
    parsed_input = mathparse.parse(inpt, language='ENG')
    result = round(random() * float(parsed_input))
    await ctx.channel.send(str(result))

@bot.event
async def on_ready():
    print(f'{bot.user} succesfully logged in!')

@bot.event
# AUTOSNAIL
async def on_message_delete(message):
    await autosnail.snail_delete_check(message, bot)

@bot.event
async def on_reaction_add(reaction, user):
    if user != bot.user and reaction.message.author.id == bot.user.id: 
        console_bot.console_react(reaction)

@bot.event
async def on_message(message):
    if message.author == bot.user: 
        return

    if not check_reply(message):
        # AUTOSNAIL
        await autosnail.auto_snail_safe(message, bot)

        # CONSOLE REPLY
        await console_bot.check_consoles(message)     
        
    # BAN WORD
    await banword.check_for_words(message, bot)
    
    # WORDLIST
    await wordlist.word_list_check(message)

    # COMMANDS
    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.Forbidden):
        print("No permission")

#Start
console_bot.get_consoles()
bot.run(TOKEN)