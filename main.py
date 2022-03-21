from distutils.command.clean import clean
import re
import itertools
import os 
import csv
from random import random
import discord
from discord.ext import commands
import time

#Config constants
TOKEN = ""
CONSOLE_CSV_DELIM = '>'

#Working directory
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
URLS_PATH = os.path.join(DIR_PATH,"urls.txt")

# Auto Snail find URL
def FindURL(string):
    # findall() has been used 
    # with valid conditions for urls in string
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex,string)      
    return [x[0] for x in url]

#List of active consoles
ConsoleList = []
lastConsole = ""

#Directly access single line of CSV file
def get_csv_line(path, line_number):
    with open(path,encoding='utf8') as f:
        return next(itertools.islice(csv.reader(f, delimiter=CONSOLE_CSV_DELIM ), line_number, None))

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
    lastEmbed = discord.Embed()

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

        n = 0
        MessageTitle = ""
        MessageDesc = ""
        MessageScore = ""
        line = get_csv_line(itemPath, Index)
        for item in line:
            print(item)
            if item != "":
                if n == self.columns.title:
                    MessageTitle = re.sub(r"\([^()]*\)", "", item)
                    MessageTitle = MessageTitle.replace("Disk 1", "").replace("Disk 2", "").replace("Disk 3", "").replace("Disk 4", "").replace("Side A", "").replace("Side B", "")
                    MessageTitle = MessageTitle.replace("Disc 1", "").replace("Disc 2", "").replace("Disc 3", "").replace("Disc 4", "").replace("Side C", "").replace("Side D", "")
                    if ", The" in MessageTitle:
                        MessageTitle = "The " + MessageTitle.replace(", The","")
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
                    MessageScore = ('Score: ' + item + '\n')
                if n == self.columns.rating:
                    MessageDesc += ('Rating: ' + item + '\n')
                n+=1
        
        #Create wikipedia URL
        MessageURL = "https://en.wikipedia.org/wiki/" + MessageTitle.replace(' ','_').replace('_-_',':_')
        #Create message body
        self.lastEmbed = discord.Embed(title=MessageTitle, url=MessageURL, description=MessageDesc, color=0xFF1694)
        embed=discord.Embed(title=MessageTitle, url=MessageURL, description=MessageScore, color=0xFF1694)
        print(Index)
        return embed

#Function to retrieve list of valid console databases
def GetConsoles():
    #Retrieve consoles from Data folder
    dataPath = os.path.join(DIR_PATH, 'Data/')
    for entry in os.listdir(dataPath):
        itemPath = os.path.join(dataPath, entry)
        if os.path.isfile(itemPath):
            with open(itemPath,encoding='utf8', newline='') as csvfile:
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
                    ItemNo = 0
                    for item in line: 
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
def check_reply(message):
    if message.reference is not None and message.is_system :
        print(message.reference)
        return True
    return False

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f'{bot.user} succesfully logged in!')

@bot.event
async def on_message(message):
    global lastConsole
    if message.author == bot.user: 
        return

    if check_reply(message):
        if 'detail' in message.content.lower():
            for console in ConsoleList:
                if console.name.replace('.csv', '').lower() in lastConsole.replace('.csv', '').lower():
                    await message.channel.send(embed=console.lastEmbed,mention_author=False)
    else:
        for console in ConsoleList:
            if ((' ' + console.name.replace('.csv', '').lower()+ ' ') in message.content.lower()) \
            or (message.content.lower().startswith(console.name.replace('.csv', '').lower() + " ")) \
            or (message.content.lower().endswith(" " + console.name.replace('.csv', '').lower())) \
            or (message.content.lower() == console.name.replace('.csv', '').lower()):
                print(f'{console.name} called')
                lastConsole = console.name
                await message.channel.send(embed=console.GetMessage())
                return
        
        # Autosnail
        if not message.embeds:
            urls = FindURL(message.content)
            # Check message for url
            if len(urls) > 0:
                for url in urls:
                    snail = False
                    clean_url = url.rstrip().lower()
                    if clean_url.contains("youtube.com/watch?v="):
                        clean_url = clean_url.replace("youtube.com/watch?v=","youtu.be/")
                    
                    clean_url = clean_url.split("?")[0].lower()  
                    newlines = []
                    # Check each line of file
                    
                    with open(URLS_PATH, 'r') as file:
                        for line in file:
                            clean_line = line.rstrip()
                            date = int(clean_line.split('>')[0])
                            lineurl = clean_line.split('>')[1]
                            # Check if message within last 3 days
                            if (int(time.time()) - date) < (86400 * 3):
                                newlines.append(clean_line) # Create new list with in date messages
                                if lineurl == clean_url: # If message a Snail
                                    snail = True        

                    # Create new file with only in date messages   
                    with open(URLS_PATH, 'w') as file:
                        for item in newlines:
                            file.write("%s\n" % item) 

                    # Snail if snailable, else add to list
                    if snail:
                        emoji = '\U0001F40C' #Snail
                        if message.author.id == 178130280400420864: #Jaysnail
                            emoji = ":snailuri:"
                        await message.add_reaction(emoji)
                    else:
                        with open(URLS_PATH, 'a') as file:
                            newline = str(int(time.time())) + '>' + clean_url + '\n'
                            file.write(newline)


    await bot.process_commands(message)

#Start
GetConsoles()
bot.run(TOKEN)