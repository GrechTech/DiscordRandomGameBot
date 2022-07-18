import os, time
import discord
from random import random

DIR_PATH = os.path.join("usr","app","config")
CUR_WORD_PATH = os.path.join(DIR_PATH,"word_current.txt")
CUR_WORD_DATE_PATH = os.path.join(DIR_PATH,"word_current_date.txt")
WORD_LIST_PATH = os.path.join(DIR_PATH,"word_list.txt")

if not os.path.exists(CUR_WORD_PATH):
    with open(CUR_WORD_PATH, "w+") as f: 
        f.write('')
if not os.path.exists(CUR_WORD_DATE_PATH):
    with open(CUR_WORD_DATE_PATH, "w+") as f: 
        f.write('')
if not os.path.exists(WORD_LIST_PATH):
    with open(WORD_LIST_PATH, "w+") as f: 
        f.write('')

def _currentWord():
    with open(CUR_WORD_PATH) as f:
        line = f.readline()
    return line.rstrip().lower()

def _checkMonthPassed():
    date = 0
    with open(CUR_WORD_PATH) as f:
        date = int(f.readline().rstrip().lower())
    return (int(time.time()) - date > (86400 * 28) )

def _setNewWord(destructive = True):
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
    with open(CUR_WORD_PATH, "w+") as f:
        f.write(word.rstrip())
        print("Word stored")

    with open(CUR_WORD_DATE_PATH, "w+") as f:
        f.write(str(int(time.time())))
        print("Word date stored")

    # Remove word from list
    if destructive:
        lines.remove(word)

        # Store changes to word list
        with open(WORD_LIST_PATH, "w+") as f:
            f.writelines(lines)
            print("Word removed")

def _messageCheck(message, text):
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
    if _messageCheck(message, _currentWord()):
        print("Word found")
        # Reaction
        emoji = '\U0001F451'
        await message.add_reaction(emoji)

        # Message
        url = "https://en.wikipedia.org/wiki/" + _currentWord()
        desc = "New word found!"
        embed=discord.Embed(title=_currentWord(), url=url, description=desc, color=0x828282)
        await message.channel.send(embed=embed)
        _setNewWord()
    
    if _checkMonthPassed():
        print("Word timed out")

        # Message
        url = "https://en.wikipedia.org/wiki/" + _currentWord()
        desc = "New word not found after 4 weeks"
        embed=discord.Embed(title=_currentWord(), url=url, description=desc, color=0x828282)
        await message.channel.send(embed=embed)
        _setNewWord()
