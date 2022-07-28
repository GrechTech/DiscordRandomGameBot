import re, itertools, os , csv
from discord.ext import commands

#Config constants
TOKEN = ""
CONSOLE_CSV_DELIM = '>'

#Working directory
DIR_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)))

#List of active consoles
ConsoleList = []

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


print(find_csv_line(os.path.join(os.path.join(DIR_PATH, 'Data/'), "spectrum.csv"),"Zzzz"))