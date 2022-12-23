import os
import discord

DIR_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)))
BAN_LIST = os.path.join(DIR_PATH,"Config","ban_list.txt")

def _getBannedWords():
    newlines = []
    
    with open(BAN_LIST, "r") as file:
        for line in file:
            clean_line = line.lower().rstrip()
            newlines.append(clean_line)
    
    return newlines

BannedWords = _getBannedWords()

async def CheckForWords(message, bot):
    if set(BannedWords).intersection(message.content.lower().split()):                  #Split message into list and compare against the cringelist 
        await message.add_reaction(discord.utils.get(bot.emojis, name="cringegrin"))    #If two items of list match then react with cringe emote