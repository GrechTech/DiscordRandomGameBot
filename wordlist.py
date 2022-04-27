import os
import discord
from random import random

DIR_PATH = os.path.dirname(os.path.realpath(__file__)) # Working directory

####################
CUR_WORD_PATH = os.path.join(DIR_PATH,"current_word.txt")
WORD_LIST_PATH = os.path.join(DIR_PATH,"wordlist.txt")

def CurrentWord():
    with open(CUR_WORD_PATH) as f:
        lines = f.readlines()
    return lines[0].rstrip().lower()

def SetNewWord(destructive = True):
    # Get word list
    with open(WORD_LIST_PATH) as f:
        lines = f.readlines()

    Wordlist_length = len(lines)

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

    # Remove word from list
    if destructive:
        lines.remove(word)

        # Store changes to word list
        with open(WORD_LIST_PATH, "w") as f:
            f.write(lines)

async def WordlistCheck(message):
    if CurrentWord() in message.content.lower():
        # Reaction
        emoji = '\U0001F451'
        await message.add_reaction(emoji)

        # Message
        url = "https://en.wikipedia.org/wiki/" + CurrentWord()
        desc = "The word was: " + CurrentWord() + "\nClick the title to find out what it means!"
        embed=discord.Embed(title="New word found!", url=url, description=desc, color=0x828282)
        await message.channel.send(embed=embed)
        SetNewWord()
        
####################