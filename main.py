import asyncio
import re, itertools, os , csv
from random import random
import time
from mathparse import mathparse
import discord
from discord.ext import commands
import wordlist
import autosnail
import banword
import imagesearch

#Config constants
TOKEN = ""
CONSOLE_CSV_DELIM = '>'

#Working directory
DIR_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)))
TOKEN_PATH = os.path.join(DIR_PATH,"Config","token.txt")

if not os.path.exists(TOKEN_PATH):
    with open(TOKEN_PATH, "w+") as f: 
        f.write('')
with open(TOKEN_PATH,"r") as f:
    TOKEN = f.readline().rstrip()
####################

#List of active consoles
ConsoleList = []

#Directly access single line of CSV file
def get_csv_line(path, line_number):
    with open(path,encoding='utf8') as f:
        return next(itertools.islice(csv.reader(f, delimiter=CONSOLE_CSV_DELIM ), line_number, None))

#GetCSV Row
def find_csv_line(path,query):
    with open(path, 'rt',encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=CONSOLE_CSV_DELIM)
        n = 0
        for row in reader:
            n += 1
            newquery = query.rstrip()
            y = 0
            for part in row:
                y += 1
                if y < 2: # avoid description
                    if ", The" in part:
                        part = "The " + part.replace(", The","")
                    if part.find(query) != -1:
                        return n
        print("No query found for: ", newquery, " at ", path, " after ", n)
        return -1

#Data class for a console message response
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

#Data class for a console database item
class Console:
    def __init__(self, name, size, title, developer, publisher, year, genre, score, rating, description):
        self.name = name
        self.size = size
        self.columns = Response(title, developer, publisher, year, genre, score, rating, description)

    def GetMessageDetails(self, Title, full = False):
        itemPath = os.path.join(os.path.join(DIR_PATH, 'Data/'), self.name)
        n = 0
        MessageTitle = ""
        MessageDesc = ""
        index = find_csv_line(itemPath, Title) - 1
        line = get_csv_line(itemPath, index)
        for item in line:
            print(item)
            if item != "":
                if n == self.columns.title:
                    MessageTitle = re.sub(r"\([^()]*\)", "", item)
                    MessageTitle = re.sub(r'\[[^\]]*\]', "", MessageTitle)
                    MessageTitle = MessageTitle.replace("Disk 1", "").replace("Disk 2", "").replace("Disk 3", "").replace("Disk 4", "").replace("Side A", "").replace("Side B", "")
                    MessageTitle = MessageTitle.replace("Disc 1", "").replace("Disc 2", "").replace("Disc 3", "").replace("Disc 4", "").replace("Side C", "").replace("Side D", "")
                    MessageTitle = MessageTitle.replace("- Disk 1", "").replace("- Disk 2", "").replace("- Disk 3", "").replace("- Disk 4", "").replace("- Side A", "").replace("- Side B", "")
                    MessageTitle = MessageTitle.replace("- Disc 1", "").replace("- Disc 2", "").replace("- Disc 3", "").replace("- Disc 4", "").replace("- Side C", "").replace("- Side D", "")
                    MessageTitle = MessageTitle.replace("Disk1", "").replace("Disk2", "").replace("Disk3", "").replace("Disk4", "").replace("SideA", "").replace("SideB", "")
                    MessageTitle = MessageTitle.replace("Disc1", "").replace("Disc2", "").replace("Disc3", "").replace("Disc4", "").replace("SideC", "").replace("SideD", "")
                    MessageTitle = MessageTitle.replace("- Disk1", "").replace("- Disk2", "").replace("- Disk3", "").replace("- Disk4", "").replace("- SideA", "").replace("- SideB", "")
                    MessageTitle = MessageTitle.replace("- Disc1", "").replace("- Disc2", "").replace("- Disc3", "").replace("- Disc4", "").replace("- SideC", "").replace("- SideD", "")
                    if ", The" in MessageTitle:
                        MessageTitle = "The " + MessageTitle.replace(", The","")
                    MessageTitle = MessageTitle.rstrip()
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
                if n == self.columns.description and full:
                    MessageDesc += ('Description: ' + item + '\n')
                n+=1
        
        #Create wikipedia URL
        MessageURL = "https://en.wikipedia.org/wiki/" + MessageTitle.replace(' ','_').replace('_-_',':_')
        MessageTitleOutput = MessageTitle + " (" + self.name.replace('.csv', '').upper() + ")"
        #Create message body
        embed=discord.Embed(title=MessageTitleOutput, url=MessageURL, description=MessageDesc, color=0xFF1694)
        result = imagesearch.DoSearch(MessageTitleOutput + " box art")
        print("Search result: ", result)
        embed.set_thumbnail(url=result)
        return embed


    def GetMessage(self):
        itemPath = os.path.join(os.path.join(DIR_PATH, 'Data/'), self.name)
        Index = round(random() * self.size)

        if Index < 1:
            Index = 1
        elif Index > self.size:
            Index = self.size

        n = 0
        MessageTitle = ""
        MessageScore = ""
        line = get_csv_line(itemPath, Index)
        for item in line:
            print(item)
            if item != "":
                if n == self.columns.title:
                    MessageTitle = re.sub(r"\([^()]*\)", "", item)
                    MessageTitle = MessageTitle.replace("Disk 1", "").replace("Disk 2", "").replace("Disk 3", "").replace("Disk 4", "").replace("Side A", "").replace("Side B", "")
                    MessageTitle = MessageTitle.replace("Disc 1", "").replace("Disc 2", "").replace("Disc 3", "").replace("Disc 4", "").replace("Side C", "").replace("Side D", "")
                    MessageTitle = MessageTitle.replace("- Disk 1", "").replace("- Disk 2", "").replace("- Disk 3", "").replace("- Disk 4", "").replace("- Side A", "").replace("- Side B", "")
                    MessageTitle = MessageTitle.replace("- Disc 1", "").replace("- Disc 2", "").replace("- Disc 3", "").replace("- Disc 4", "").replace("- Side C", "").replace("- Side D", "")
                    MessageTitle = MessageTitle.replace("Disk1", "").replace("Disk2", "").replace("Disk3", "").replace("Disk4", "").replace("SideA", "").replace("SideB", "")
                    MessageTitle = MessageTitle.replace("Disc1", "").replace("Disc2", "").replace("Disc3", "").replace("Disc4", "").replace("SideC", "").replace("SideD", "")
                    MessageTitle = MessageTitle.replace("- Disk1", "").replace("- Disk2", "").replace("- Disk3", "").replace("- Disk4", "").replace("- SideA", "").replace("- SideB", "")
                    MessageTitle = MessageTitle.replace("- Disc1", "").replace("- Disc2", "").replace("- Disc3", "").replace("- Disc4", "").replace("- SideC", "").replace("- SideD", "")
                    if ", The" in MessageTitle:
                        MessageTitle = "The " + MessageTitle.replace(", The","")
                    MessageTitle = MessageTitle.rstrip()
                n+=1
        
        #Create wikipedia URL
        MessageURL = "https://en.wikipedia.org/wiki/" + MessageTitle.replace(' ','_').replace('_-_',':_')
        MessageTitleOutput = MessageTitle + " (" + self.name.replace('.csv', '').upper() + ")"
        #Create message body
        embed=discord.Embed(title=MessageTitleOutput, url=MessageURL, description=MessageScore, color=0xFF1694)
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
                descriptionN = -1

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
                            if item == 'description':
                                descriptionN = ItemNo
                        ItemNo += 1
                    LineNo += 1

                if titleN != -1:
                    print("New Console: ")
                    print(entry.replace('.csv', ''))
                    ConsoleList.append(Console(entry, LineNo, titleN, developerN, publisherN, yearN, genreN, scoreN, ratingN,descriptionN ))
                else:
                    print("Error Invalid format (Check top line)")

#Discord functionality
def check_reply(message):
    if message.reference is not None and message.is_system :
        print(message.reference)
        return True
    return False

bot = commands.Bot(command_prefix="!")

@bot.command()
async def consoles(ctx):
    list = ""
    for console in ConsoleList:
        list += console.name.replace('.csv', '').lower() + ', '
    embed=discord.Embed(title="Console List", description=list, color=0xFF1694)
    await ctx.channel.send(embed=embed)

@bot.command()
async def calc(ctx, *, input: str):
    result = mathparse.parse(input, language='ENG')
    await ctx.channel.send(str(result))

@bot.command()
async def roll(ctx, *, inpt: str):
    parsed_input = mathparse.parse(inpt, language='ENG')
    result = round(random() * parsed_input)
    await ctx.channel.send(str(result))

@bot.event
async def on_ready():
    print(f'{bot.user} succesfully logged in!')

@bot.event
# AUTOSNAIL
async def on_message_delete(message):
    await autosnail.SnailDeleteCheck(message, bot)

@bot.event
async def on_reaction_add(reaction, user):
    if user != bot.user and reaction.message.author.id == bot.user.id:
        try:
            if str(reaction.emoji) == "❓" or str(reaction.emoji) == "❔" and not str(reaction.emoji) == "❗" and not str(reaction.emoji) == "❕":
                for console in ConsoleList:
                    if reaction.message.embeds[0].title.endswith('(' + console.name.replace('.csv', '').upper() + ')'):
                        title = reaction.message.embeds[0].title.replace('(' + console.name.replace('.csv', '').upper() + ')','').rstrip()
                        if find_csv_line(os.path.join(os.path.join(DIR_PATH, 'Data/'), console.name),title) != -1:
                            await reaction.message.edit(embed=console.GetMessageDetails(title))
                            return
            elif str(reaction.emoji) == "❗" or str(reaction.emoji) == "❕":
                for console in ConsoleList:
                    if reaction.message.embeds[0].title.endswith('(' + console.name.replace('.csv', '').upper() + ')'):
                        title = reaction.message.embeds[0].title.replace('(' + console.name.replace('.csv', '').upper() + ')','').rstrip()
                        if find_csv_line(os.path.join(os.path.join(DIR_PATH, 'Data/'), console.name),title) != -1:
                            await reaction.message.edit(embed=console.GetMessageDetails(title, True))
                            return
        except:
            print("React Error (Probably a reaction on bots own message that isnt game related)")

@bot.event
async def on_message(message):
    if message.author == bot.user: 
        return

    if not check_reply(message):
        # AUTOSNAIL
        SnailCheck = await autosnail.AutoSnail(message, bot)
        if SnailCheck:
            time.sleep(0.01)
            msg = await bot.fetch_message(message.id)
            await autosnail.ConfirmSnail(msg, bot)

        # CONSOLE REPLY
        for console in ConsoleList:
            if ((' ' + console.name.replace('.csv', '').lower()+ ' ') in message.content.lower()) \
            or (message.content.lower().startswith(console.name.replace('.csv', '').lower() + " ")) \
            or (message.content.lower().endswith(" " + console.name.replace('.csv', '').lower())) \
            or (message.content.lower() == console.name.replace('.csv', '').lower()):
                print(f'{console.name} called')
                await message.channel.send(embed=console.GetMessage())
                return
        
    # BAN WORD
    await banword.CheckForWords(message, bot)
    
    # WORDLIST
    await wordlist.WordlistCheck(message)

    # COMMANDS
    await bot.process_commands(message)

    

#Start
GetConsoles()
bot.run(TOKEN)