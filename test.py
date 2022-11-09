import re, itertools, os , csv
from discord.ext import commands

#Config constants
TOKEN = ""
CONSOLE_CSV_DELIM = '>'

#Working directory
DIR_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)))

#List of active consoles
ConsoleList = []

def GetConsoles():
    #Retrieve consoles from Data folder
    dataPath = os.path.join(DIR_PATH, 'Data/')
    for entry in os.listdir(dataPath):
        print(entry)
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
                else:
                    print("Error 2")
        else:
            print("Error 1")

#Directly access single line of CSV file
def get_csv_line(path, line_number):
    with open(path,encoding='utf8') as f:
        return next(itertools.islice(csv.reader(f, delimiter=CONSOLE_CSV_DELIM ), line_number, None))

def find_csv_line(path,query):
    with open(path, 'rt',encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=CONSOLE_CSV_DELIM)
        n = 0
        for row in reader:
            n += 1
            newquery = query.rstrip()
            if ", The" in newquery:
                newquery = "The " + newquery.replace("The ","") + ", The"
            for part in row:
                if part.find(query) != -1:
                    return n
            print(newquery)
            print(row)
        print("No query found for: ", newquery, " at ", path, " after ", n)
        return -1

GetConsoles()
#print(find_csv_line(os.path.join(os.path.join(DIR_PATH, 'Data/'), "spectrum.csv"),"Zzzz"))