
from discord.ext import commands
TOKEN = "INSERT-TOKEN"

CONFIG_CSV_DELIM = ','
CONSOLE_CSV_DELIM = '>'

ConsoleList = []

class Console:
    def __init__(self, name, fileName, size):
        self.name = name
        self.fileName = fileName
        self.size = size
    
    def GetMessage():
        pass


def GetConsoles():
    pass

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f'{bot.user} succesfully logged in!')

@bot.event
async def on_message(message):
    if message.author == bot.user: 
        return

    for console in ConsoleList:
        if console.name in message.content:
            print(f'{console.name} called')
            await message.channel.send(console.GetMessage())

    if message.content == 'hello':
        await message.channel.send(f'Hi {message.author}')

    await bot.process_commands(message)

bot.run(TOKEN)