import csv
import itertools
import os
import re
from random import random

import discord
import imagesearch

dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)))
consoles_delim = '>'

# List of active consoles
console_list = []


# Directly access single line of CSV file
def get_csv_line(path, line_number):
    with open(path, encoding='utf8') as f:
        return next(itertools.islice(csv.reader(f, delimiter=consoles_delim), line_number, None))


# GetCSV Row
def find_csv_line(path, query):
    with open(path, 'rt', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=consoles_delim)
        n = 0
        for row in reader:
            n += 1
            new_query = query.rstrip()
            y = 0
            for part in row:
                y += 1
                if y < 2:  # avoid description
                    if ", The" in part:
                        part = "The " + part.replace(", The", "")
                    if part.find(query) != -1:
                        return n
        print("No query found for: ", new_query, " at ", path, " after ", n)
        return -1


async def console_react(reaction):
    if str(reaction.emoji) == "❓" or str(reaction.emoji) == "❔" and not str(reaction.emoji) == "❗" and not str(
            reaction.emoji) == "❕":
        for console in console_list:
            if reaction.message.embeds[0].title.endswith('(' + console.name.replace('.csv', '').upper() + ')'):
                title = reaction.message.embeds[0].title.replace(
                    '(' + console.name.replace('.csv', '').upper() + ')', '').rstrip()
                if find_csv_line(os.path.join(os.path.join(dir_path, 'Data/'), console.name), title) != -1:
                    await reaction.message.edit(embed=console.get_message_details(title))
                    return
    elif str(reaction.emoji) == "❗" or str(reaction.emoji) == "❕":
        for console in console_list:
            if reaction.message.embeds[0].title.endswith('(' + console.name.replace('.csv', '').upper() + ')'):
                title = reaction.message.embeds[0].title.replace(
                    '(' + console.name.replace('.csv', '').upper() + ')', '').rstrip()
                if find_csv_line(os.path.join(os.path.join(dir_path, 'Data/'), console.name), title) != -1:
                    await reaction.message.edit(embed=console.get_message_details(title, True))
                    return


# Data class for a console message response
class Response:
    def __init__(self, title, developer, publisher, year, genre, score, rating, description):
        self.title = title
        self.developer = developer
        self.publisher = publisher
        self.year = year
        self.genre = genre
        self.score = score
        self.rating = rating
        self.description = description


# Data class for a console database item
class Console:
    rom_name_substitutions_pre = {"Disk", "Disc", "Side"}
    rom_name_substitutions_post = {"1", "2", "3", "4", "5", "6", "A", "B", "C", "D"}

    def __init__(self, name, size, title, developer, publisher, year, genre, score, rating, description):
        self.name = name
        self.size = size
        self.columns = Response(title, developer, publisher, year, genre, score, rating, description)

    def get_message_details(self, title, full=False):
        item_path = os.path.join(os.path.join(dir_path, 'Data/'), self.name)
        n = 0

        message_title = ""
        message_desc = ""
        index = find_csv_line(item_path, title) - 1
        line = get_csv_line(item_path, index)
        for item in line:
            print(item)
            if item != "":
                if n == self.columns.title:
                    message_title = re.sub(r"\([^()]*\)", "", item)
                    message_title = re.sub(r'\[[^]]*]', "", message_title)
                    for pre in self.rom_name_substitutions_pre:
                        for post in self.rom_name_substitutions_post:
                            message_title = message_title.replace(pre + post, "")
                            message_title = message_title.replace(pre + " " + post, "")
                    if ", The" in message_title:
                        message_title = "The " + message_title.replace(", The", "")
                    message_title = message_title.rstrip()
                if n == self.columns.developer:
                    message_desc += ('Developer: ' + item + '\n')
                if n == self.columns.publisher:
                    message_desc += ('Publisher: ' + item + '\n')
                if n == self.columns.year:
                    message_desc += ('Year: ' + item + '\n')
                if n == self.columns.genre:
                    message_desc += ('Genre: ' + item + '\n')
                if n == self.columns.score:
                    message_desc += ('Score: ' + item + '\n')
                if n == self.columns.rating:
                    message_desc += ('Rating: ' + item + '\n')
                if n == self.columns.description and full:
                    message_desc += ('Description: ' + item + '\n')
                n += 1

        # Create wikipedia URL
        message_url = "https://en.wikipedia.org/wiki/" + message_title.replace(' ', '_').replace('_-_', ':_')
        message_title_output = message_title + " (" + self.name.replace('.csv', '').upper() + ")"
        # Create message body
        embed = discord.Embed(title=message_title_output, url=message_url, description=message_desc, color=0xFF1694)
        result = imagesearch.do_search(message_title_output + " box art")
        print("Search result: ", result)
        embed.set_thumbnail(url=result)
        return embed

    def get_message(self, image=True):
        item_path = os.path.join(os.path.join(dir_path, 'Data/'), self.name)
        index = round(random() * self.size)

        if index < 1:
            index = 1
        elif index > self.size:
            index = self.size

        n = 0
        message_title = ""
        message_desc = ""
        line = get_csv_line(item_path, index)
        for item in line:
            print(item)
            if item != "":
                if n == self.columns.title:
                    message_title = re.sub(r"\([^()]*\)", "", item)
                    message_title = re.sub(r'\[[^]]*]', "", message_title)
                    for pre in self.rom_name_substitutions_pre:
                        for post in self.rom_name_substitutions_post:
                            message_title = message_title.replace(pre + post, "")
                            message_title = message_title.replace(pre + " " + post, "")
                    if ", The" in message_title:
                        message_title = "The " + message_title.replace(", The", "")
                    message_title = message_title.rstrip()
                if n == self.columns.year:
                    message_desc += ('Year: ' + item + '\n')
                if n == self.columns.developer:
                    message_desc += ('Developer: ' + item + '\n')
                n += 1

        # Create wikipedia URL
        message_url = "https://en.wikipedia.org/wiki/" + message_title.replace(' ', '_').replace('_-_', ':_')
        message_title_output = message_title + " (" + self.name.replace('.csv', '').upper() + ")"
        # Create message body
        embed = discord.Embed(title=message_title_output, url=message_url, description=message_desc, color=0xFF1694)
        result = imagesearch.do_search(message_title_output + " box art")
        print("Search result: ", result)
        if image:
            embed.set_thumbnail(url=result)
        return embed


def get_console_list():
    item_list = ""
    for console in console_list:
        item_list += console.name.replace('.csv', '').lower() + ', '
    return discord.Embed(title="Console List", description=item_list, color=0xFF1694)


def get_console_count(name):
    for x in console_list:
        if x.name.replace('.csv', '').lower() == name.lower():
            return discord.Embed(title="Console Count", description=x.size, color=0xFF1694)


# Function to retrieve list of valid console databases
def get_consoles():
    # Retrieve consoles from Data folder
    data_path = os.path.join(dir_path, 'Data/')
    for entry in os.listdir(data_path):
        item_path = os.path.join(data_path, entry)
        if os.path.isfile(item_path):
            with open(item_path, encoding='utf8', newline='') as csvfile:
                dbreader = csv.reader(csvfile, delimiter=consoles_delim, quotechar='|', skipinitialspace=True)
                line_count = 0

                title_count = -1
                developer_count = -1
                publisher_count = -1
                year_count = -1
                genre_count = -1
                score_count = -1
                rating_count = -1
                description_count = -1

                for line in dbreader:
                    item_count = 0
                    for item in line:
                        if line_count == 0:
                            # If first line, check which column contains which headers
                            if item == 'title':
                                title_count = item_count
                            if item == 'developer':
                                developer_count = item_count
                            if item == 'publisher':
                                publisher_count = item_count
                            if item == 'year':
                                year_count = item_count
                            if item == 'genre':
                                genre_count = item_count
                            if item == 'score':
                                score_count = item_count
                            if item == 'rating':
                                rating_count = item_count
                            if item == 'description':
                                description_count = item_count
                        item_count += 1
                    line_count += 1

                if title_count != -1:
                    print("New Console: ")
                    print(entry.replace('.csv', ''))
                    console_list.append(
                        Console(entry, line_count, title_count, developer_count, publisher_count, year_count,
                                genre_count, score_count, rating_count, description_count))
                else:
                    print("Error Invalid format (Check top line)")
                    print(item_path)


async def check_consoles(message):
    images = True
    if message.author.id == 206860027204599811:
        images = False
    for console in console_list:
        if ((' ' + console.name.replace('.csv', '').lower() + ' ') in message.content.lower()) \
                or (message.content.lower().startswith(console.name.replace('.csv', '').lower() + " ")) \
                or (message.content.lower().endswith(" " + console.name.replace('.csv', '').lower())) \
                or (message.content.lower() == console.name.replace('.csv', '').lower()):
            print(f'{console.name} called')
            await message.channel.send(embed=console.get_message(images))
            return
