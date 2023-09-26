import os
import time
from random import random

import discord

dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)))
cur_word_path = os.path.join(dir_path, "Config", "word_current.txt")
cur_word_date_path = os.path.join(dir_path, "Config", "word_current_date.txt")
word_list_path = os.path.join(dir_path, "Config", "word_list.txt")

if not os.path.exists(cur_word_path):
    with open(cur_word_path, "w+") as f:
        f.write('')
if not os.path.exists(cur_word_date_path):
    with open(cur_word_date_path, "w+") as f:
        f.write('')
if not os.path.exists(word_list_path):
    with open(word_list_path, "w+") as f:
        f.write('')


def current_word():
    with open(cur_word_path) as file:
        line = file.readline()
    return line.rstrip().lower()


def check_month_passed():
    date = 0
    with open(cur_word_date_path) as file:
        date = int(file.readline().rstrip().lower())
    return int(time.time()) - date > (86400 * 28)


def set_new_word(destructive=True):
    # Get word list
    with open(word_list_path) as file:
        lines = file.readlines()

    wordlist_length = len(lines)

    print("Wordlist length: ", wordlist_length)
    # Select random word
    index = round(random() * wordlist_length)
    if index < 0:
        index = 0
    elif index > wordlist_length:
        index = wordlist_length

    word = lines[index]

    # Store as current word
    with open(cur_word_path, "w+") as file:
        file.write(word.rstrip())
        print("Word stored")

    with open(cur_word_date_path, "w+") as file:
        file.write(str(int(time.time())))
        print("Word date stored")

    # Remove word from list
    if destructive:
        lines.remove(word)

        # Store changes to word list
        with open(word_list_path, "w+") as file:
            file.writelines(lines)
            print("Word removed")


def message_check(message, text):
    if text in message.content:
        return True
    if message.embeds is not None and len(message.embeds) > 0:
        print(message.embeds)
        if text in message.embeds[0].description:
            return True
        if text in message.embeds[0].title:
            return True
        if text in message.embeds[0].url:
            return True
    return False


async def word_list_check(message):
    if message_check(message, current_word()):
        print("Word found")
        # Reaction
        emoji = '\U0001F451'
        await message.add_reaction(emoji)

        # Message
        url = "https://en.wikipedia.org/wiki/" + current_word()
        desc = "New word found!"
        embed = discord.Embed(title=current_word(), url=url, description=desc, color=0x828282)
        await message.channel.send(embed=embed)
        set_new_word()

    if check_month_passed():
        print("Word timed out")
        # Message
        url = "https://en.wikipedia.org/wiki/" + current_word()
        desc = "New word not found after 4 weeks"
        embed = discord.Embed(title=current_word(), url=url, description=desc, color=0x828282)
        await message.channel.send(embed=embed)
        set_new_word()
