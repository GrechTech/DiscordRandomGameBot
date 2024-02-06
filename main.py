import asyncio
from random import random
import aiohttp
import psutil
import os
import discord
import requests
from discord.ext import commands

import f1next
import wordlist
import autosnail
import banword
import console_bot
import motorsportevents

TOKEN = ""  # From Config / token.txt

dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)))
token_path = os.path.join(dir_path, "Config", "token.txt")
intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

if not os.path.exists(token_path):
    with open(token_path, "w+") as f:
        f.write('')
with open(token_path, "r") as f:
    TOKEN = f.readline().rstrip()


@bot.event
async def on_ready():
    print(f'{bot.user} successfully logged in!')
    for attempt in range(100):
        print('Attempt: ' + str(attempt))
        try:
            await asyncio.to_thread(await autosnail.get_history(bot, False))
        except aiohttp.client_exceptions.ServerDisconnectedError as e:
            print(e)
            await asyncio.sleep(360 * attempt)
        else:
            break
    else:
        print("## All attempts used - Reset to finish updating")


# Discord functionality
def check_reply(message):
    return message.reference is not None and message.is_system


def get_cpu_temp():
    temp_file = open("/sys/class/thermal/thermal_zone0/temp")
    cpu_temp = temp_file.read()
    temp_file.close()
    return round(float(cpu_temp) / 1000, 3)


@bot.command()
async def health(ctx):
    embed = discord.Embed(title='System')
    embed.add_field(name='Temperature', value=f'{get_cpu_temp()} °C', inline=False)
    embed.add_field(name='CPU Use', value=f'{psutil.cpu_percent()}%', inline=False)
    embed.add_field(name='Average Load (1 min)', value=f'{psutil.getloadavg()[0]}%', inline=False)
    embed.add_field(name='Average Load (15 min)', value=f'{psutil.getloadavg()[2]}%', inline=False)
    embed.add_field(name='Memory Use', value=f'{psutil.virtual_memory().percent}%', inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def leaderboards(ctx, date_type='l'):
    await ctx.channel.send(embed=await autosnail.write_leaderboard(ctx, True, date_type))


@bot.command()
async def snailcount(ctx, date_type='l'):
    await ctx.channel.send(embed=await autosnail.write_leaderboard(ctx, False, date_type))


@bot.command()
async def consoles(ctx):
    print("Console Check")
    await ctx.channel.send(embed=console_bot.get_console_list())
    
    
@bot.command()
async def count(ctx, inpt: str):
    print("Console Check")
    await ctx.channel.send(embed=console_bot.get_console_count(inpt))
    
@bot.command()
async def motorsport(ctx):
    print("motorsports calendar")
    text_body = motorsportevents.get_events_this_week()
    print(text_body)
    embed_output = discord.Embed(title="Motorsports", url="https://www.bbc.co.uk/sport/motorsport/calendar/", description=motorsportevents.get_events_this_week(), color=0xFF0000)
    await ctx.channel.send(embed=embed_output)


@bot.command()
async def calc(ctx, *, input_val: str):
    print("Calc ")
    print(ctx.message.author.name)
    print(input_val)
    # result = mathparse.parse(input_val, language='ENG')
    # print(str(result))
    # await ctx.channel.send(str(result))


@bot.command()
async def f1(ctx):
    await ctx.channel.send(
        str(discord.utils.get(bot.emojis, name="f1")) + str(discord.utils.get(bot.emojis, name="f2")) + str(
            discord.utils.get(bot.emojis, name="f3")))
    await ctx.channel.send(f1next.custom_output())


@bot.command()
async def f3(ctx):
    await ctx.channel.send(
        str(discord.utils.get(bot.emojis, name="f1")) + str(discord.utils.get(bot.emojis, name="f3")))


@bot.command()
async def ip(ctx):
    await ctx.channel.send(requests.get('https://ipinfo.io/ip').text)


@bot.command()
async def roll(ctx, inpt: int):
    print("Roll: ")
    result = round(random() * inpt)
    print(str(inpt), " ", str(result))
    await ctx.channel.send(str(result))


@bot.event
# AUTOSNAIL
async def on_message_delete(message):
    print("Message Delete Check")
    await autosnail.snail_delete_check(message, bot)


@bot.event
async def on_reaction_add(reaction, user):
    if user != bot.user and reaction.message.author.id == bot.user.id:
        print("Console Reaction Check")
        await console_bot.console_react(reaction)


@bot.event
async def on_message(message):
    if not check_reply(message):
        # AUTOSNAIL
        await autosnail.auto_snail_safe(message, bot)
        # CONSOLE
        await console_bot.check_consoles(message)

    if not message.author == bot.user:
        # WORDLIST
        await wordlist.word_list_check(message)

        # BAN WORD
    await banword.check_for_words(message, bot)

    # COMMANDS
    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        print("**Invalid command.**")
    elif isinstance(error, commands.MissingRequiredArgument):
        print('**Pass in all requirements.**')
        await ctx.send('**Pass in all requirements.**')
    elif isinstance(error, commands.MissingPermissions):
        print("**You dont have all the requirements or permissions for using this command**")
        await ctx.send("**You dont have all the requirements or permissions for using this command**")


# Start
console_bot.get_consoles()
bot.run(TOKEN)
