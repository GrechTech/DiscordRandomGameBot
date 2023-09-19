import os
import discord

dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)))
ban_list = os.path.join(dir_path, "Config", "ban_list.txt")


def get_banned_words():
    newlines = []
    with open(ban_list, "r") as file:
        for line in file:
            clean_line = line.lower().rstrip()
            newlines.append(clean_line)
    return newlines


banned_words = get_banned_words()


async def check_for_words(message, bot):
    # Split message into list and compare against the cringelist
    if set(banned_words).intersection(message.content.lower().split()):
        print("banned word")
        await message.add_reaction(discord.utils.get(bot.emojis, name="cringegrin"))
        # If two items of list match then react with cringe emote
