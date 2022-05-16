import os
import discord
from random import random

DIR_PATH = os.path.dirname(os.path.realpath(__file__)) # Working directory

####################
CUR_WORD_PATH = os.path.join(DIR_PATH,"current_word.txt")
WORD_LIST_PATH = os.path.join(DIR_PATH,"wordlist.txt")

currentWord = "_"

def CurrentWord():
    if currentWord == "_":
        with open(CUR_WORD_PATH) as f:
            line = f.readline()
        return line.rstrip().lower()
    else:
        return currentWord

def SetNewWord(destructive = True):
    global currentWord
    # Get word list
    with open(WORD_LIST_PATH) as f:
        lines = f.readlines()

    Wordlist_length = len(lines)

    print("Wordlist length: ", Wordlist_length)
    # Select random word
    Index = round(random() * Wordlist_length)
    if Index < 0:
        Index = 0
    elif Index > Wordlist_length:
        Index = Wordlist_length

    word = lines[Index]

    # Store as current word
    with open(CUR_WORD_PATH, "w") as f:
        f.write(word.rstrip())
        print("Word stored")
        currentWord = word.rstrip()

    # Remove word from list
    if destructive:
        lines.remove(word)

        # Store changes to word list
        with open(WORD_LIST_PATH, "w") as f:
            f.writelines(lines)
            print("Word removed")

def MessageCheck(message, text):
    if text in message.content:
        return True
    if message.embeds:
        if message.embeds[0].description != discord.Embed.Empty:
            if text in message.embeds[0].description:
                return True
        if message.embeds[0].title != discord.Embed.Empty:
            if text in message.embeds[0].title:
                return True
        if message.embeds[0].url != discord.Embed.Empty:
            if text in message.embeds[0].url:
                return True
    return False

async def WordlistCheck(message):
    if MessageCheck(message, CurrentWord()):
        print("Word found")
        # Reaction
        emoji = '\U0001F451'
        await message.add_reaction(emoji)

        # Message
        url = "https://en.wikipedia.org/wiki/" + CurrentWord()
        desc = "New word found!"
        embed=discord.Embed(title=CurrentWord(), url=url, description=desc, color=0x828282)
        await message.channel.send(embed=embed)
        SetNewWord()