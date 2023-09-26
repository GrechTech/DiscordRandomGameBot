from random import random
import os
from mathparse import mathparse
import discord
from discord.ext import commands
import wordlist
import autosnail
import banword
import console_bot
import votegary

TOKEN = ""  # From Config / token.txt

dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)))
token_path = os.path.join(dir_path, "Config", "token.txt")
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

if not os.path.exists(token_path):
    with open(token_path, "w+") as f:
        f.write('')
with open(token_path, "r") as f:
    TOKEN = f.readline().rstrip()


# Discord functionality
def check_reply(message):
    return message.reference is not None and message.is_system


@bot.command()
async def leaderboards(ctx):
    await ctx.channel.send(embed=await autosnail.leaderboard(bot))


@bot.command()
async def consoles(ctx):
    print("Console Check")
    await ctx.channel.send(embed=console_bot.get_console_list())


@bot.command()
async def calc(ctx, *, input_val: str):
    print("Calc ")
    result = mathparse.parse(input_val, language='ENG')
    print(str(result))
    await ctx.channel.send(str(result))


@bot.command()  # Create a slash command
async def votegarry(ctx, left, right):
    if left == "" or right == "":
        await ctx.channel.send("Missing data")
    else:
        await ctx.respond("Vote", view=votegary.VoteView(left, right))


@bot.command()
async def roll(ctx, *, inpt: str):
    print("Roll: ")
    parsed_input = mathparse.parse(inpt, language='ENG')
    result = round(random() * float(parsed_input))
    print(str(parsed_input), " ", str(result))
    await ctx.channel.send(str(result))


@bot.event
async def on_ready():
    print(f'{bot.user} successfully logged in!')


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
    try:
        if message.author == bot.user:
            return

        if not check_reply(message):
            # AUTOSNAIL
            await autosnail.auto_snail_safe(message, bot)

            # CONSOLE
            await console_bot.check_consoles(message)

        # BAN WORD
        await banword.check_for_words(message, bot)

        # WORDLIST
        await wordlist.word_list_check(message)

        # COMMANDS
        await bot.process_commands(message)
    except Exception as e:
        print(e)
        embed = discord.Embed(title="Error")
        embed.add_field(name="Message: ", value=str(e))
        await message.channel.send(embed=embed)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        print("**Invalid command.**")
    if isinstance(error, commands.MissingRequiredArgument):
        print('**Pass in all requirements.**')
        await ctx.send('**Pass in all requirements.**')
    if isinstance(error, commands.MissingPermissions):
        print("**You dont have all the requirements or permissions for using this command**")
        await ctx.send("**You dont have all the requirements or permissions for using this command**")


# Start
console_bot.get_consoles()
bot.run(TOKEN)
