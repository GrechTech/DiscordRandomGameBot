import itertools
import os 
import csv
from random import random 
import discord
from discord.ext import commands

#Config constants
TOKEN = "INSERT-TOKEN"
CONSOLE_CSV_DELIM = '>'

#Working directory
DIR_PATH = os.path.dirname(os.path.realpath(__file__))

#List of active consoles
ConsoleList = []

#Directly access single line of CSV file
def get_csv_line(path, line_number):
    with open(path) as f:
        return next(itertools.islice(csv.reader(f), line_number, None))

#Data class for a console message response
class Response:
    def __init__(self, title, developer, publisher, year, genre, score, rating):
        self.title = title
        self.developer = developer
        self.publisher = publisher
        self.year = year
        self.genre = genre
        self.score = score
        self.rating = rating

#Data class for a console database item
class Console:
    def __init__(self, name, size, title, developer, publisher, year, genre, score, rating):
        self.name = name
        self.size = size
        self.columns = Response(title, developer, publisher, year, genre, score, rating)

    def GetMessage(self):
        itemPath = os.path.join(os.path.join(DIR_PATH, 'Data/'), self.name)
        Index = round(random() * self.size)

        if Index < 1:
            Index = 1
        elif Index > self.size:
            Index = self.size

        #WIP
        n = 0
        MessageTitle = ""
        MessageDesc = "[["
        for item in get_csv_line(Index, itemPath):
            if n == self.columns.title:
                MessageTitle = item
            if n == self.columns.developer:
                MessageDesc += ('Developer: ' + item + '\n')
            if n == self.columns.publisher:
                MessageDesc += ('Publisher: ' + item + '\n')
            if n == self.columns.year:
                MessageDesc += ('Year: ' + item + '\n')
            if n == self.columns.genre:
                MessageDesc += ('Genre: ' + item + '\n')
            if n == self.columns.score:
                MessageDesc += ('Score: ' + item + '\n')
            if n == self.columns.rating:
                MessageDesc += ('Rating: ' + item + '\n')
            n+=1
        
        ##Enclosure description
        MessageDesc += ']]'
        #Create wikipedia URL
        MessageURL = "https://en.wikipedia.org/wiki/" + MessageTitle.replace(' ','_')
        #Create message body
        embed=discord.Embed(title=MessageTitle, url=MessageURL, description=MessageDesc, color=0xFF1694)
        return embed

#Function to retrieve list of valid console databases
def GetConsoles():
    #Retrieve consoles from Data folder
    dataPath = os.path.join(DIR_PATH, 'Data/')
    for entry in os.listdir(dataPath):
        itemPath = os.path.join(dataPath, entry)
        if os.path.isfile(itemPath):
            with open(itemPath, newline='') as csvfile:
                dbreader = csv.reader(csvfile, delimiter=CONSOLE_CSV_DELIM, quotechar='|',skipinitialspace=True)
                LineNo = 0

                titleN = -1
                developerN = -1
                publisherN = -1
                yearN = -1
                genreN = -1
                scoreN = -1
                ratingN = -1

                for line in dbreader:
                    for item in line: 
                        ItemNo = 0
                        if LineNo == 0:
                            #If first line, check which column contains which headers
                            if item == 'title':
                                titleN = ItemNo
                            if item == 'developer':
                                developerN = ItemNo
                            if item == 'publisher':
                                publisherN = ItemNo
                            if item == 'year':
                                yearN = ItemNo
                            if item == 'genre':
                                genreN = ItemNo
                            if item == 'score':
                                scoreN = ItemNo
                            if item == 'rating':
                                ratingN = ItemNo
                        ItemNo += 1
                    LineNo += 1

                if titleN != -1:
                    print("New Console: ")
                    print(entry.replace('.csv', ''))
                    ConsoleList.append(Console(entry, LineNo, titleN, developerN, publisherN, yearN, genreN, scoreN, ratingN ))


#Discord functionality
bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f'{bot.user} succesfully logged in!')

@bot.event
async def on_message(message):
    if message.author == bot.user: 
        return

    for console in ConsoleList:
        if console.name.replace('.csv', '').lower() in message.content.lower():
            print(f'{console.name} called')
            await message.channel.send(embed=console.GetMessage())

    await bot.process_commands(message)

#Start
GetConsoles()
#bot.run(TOKEN)