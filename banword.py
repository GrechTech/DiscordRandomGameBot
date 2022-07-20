import os
import discord

DIR_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)))
BAN_LIST = os.path.join(DIR_PATH,"Config","ban_list.txt")

def _getBannedWords():
    newlines = []
    # Check each line of file
    
    with open(BAN_LIST, "r") as file:
        for line in file:
            clean_line = line.lower().rstrip()
            newlines.append(clean_line)
    
    return newlines

BannedWords = _getBannedWords()

def _words_in_string(word_list, a_string):
    return set(word_list).intersection(a_string.split())

def _words_in_string2(word_list,a_string):
    for word in word_list:
        print(word)
        print(word_list)
        if word in a_string:
            return True
    return False

async def CheckForWords(message, bot):
    msg = message.content.lower()
    if _words_in_string(BannedWords, msg) or _words_in_string2(BannedWords, msg):
        emoji = discord.utils.get(bot.emojis, name="greenwithit")
        await message.add_reaction(emoji)