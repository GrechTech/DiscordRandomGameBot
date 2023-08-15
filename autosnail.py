import re, time, os
import discord

DIR_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)))
URLS_PATH = os.path.join(DIR_PATH,"Config","urls.txt")
URLS_SNAILED_PATH = os.path.join(DIR_PATH,"Config","urls_snailed.txt")
URLS_SCORES_PATH = os.path.join(DIR_PATH,"Config","Scores")

if not os.path.exists(URLS_PATH):
    with open(URLS_PATH, "w+") as f: 
        f.write('')
if not os.path.exists(URLS_PATH):
    with open(URLS_SNAILED_PATH, "w+") as f: 
        f.write('')
if not os.path.exists(URLS_SCORES_PATH):
    os.mkdir(URLS_SCORES_PATH)

# Auto Snail find URL
def _findURL(string):
    # findall() has been used 
    # with valid conditions for urls in string
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex,string)      
    return [x[0] for x in url]

# Auto Snail find URL in list
async def _autosnailFind(path, clean_url, author_id):
    snail = False
    newlines = []
    # Check each line of file
    
    with open(path, "r") as file:
        for line in file:
            clean_line = line.rstrip()
            ID = int(clean_line.split('>')[0])
            date = int(clean_line.split('>')[1])
            lineurl = clean_line.split('>')[2]
            # Check if message within last 3 days
            if (int(time.time()) - date) < (86400 * 3):
                newlines.append(clean_line) # Create new list with in date messages
                if lineurl == clean_url and author_id != ID: # If message a Snail
                    snail = True        
                    await snailScores(ID,-1)
                    

    # Create new file with only in date messages   
    with open(path, "w+") as file:
        for item in newlines:
            file.write("%s\n" % item) 
    
    return snail

async def SnailDeleteCheck(message, bot):
    if not message.author.bot: 
            for react in message.reactions:
                if '\U0001F40C' == react.emoji \
                or discord.utils.get(bot.emojis, name="snailuri") == react.emoji \
                or discord.utils.get(bot.emojis, name="sparklesnail") == react.emoji:
                    embed = discord.Embed(title="Snailed Message Deleted")
                    embed.add_field(name="Member: ", value=message.author.mention, inline=False)
                    embed.add_field(name="Message: ", value=message.content, inline=True)

                    await message.channel.send(embed=embed)
                    return
                
async def snailScores(id, scoreDelta):
    score_path = os.path.join(URLS_SCORES_PATH, str(id))
    score = 0
    if os.path.exists(score_path):
        with open(score_path, "r+") as file:
            score = int(file.rstrip())
    score += scoreDelta
    with open(score_path, "w+") as file:
        file.write(str(score))


async def AutoSnail(message, bot):
    urls = _findURL(message.content)
    # Check message for url
    if len(urls) > 0:
        for url in urls:
            snail = False
            clean_url = url.rstrip().lower()
            ToCheck = ['.png', '.gif', '.jpg','.jpeg', 'discordapp','tenor']
            if not [ele for ele in ToCheck if(ele in clean_url)]:
                if "youtube.com/watch?v=" in clean_url:
                    clean_url = clean_url.replace("youtube.com/watch?v=","youtu.be/")
                
                clean_url = clean_url.split("?")[0].lower().split("#")[0].lower()
                clean_url = clean_url.replace("www.","")
                clean_url = clean_url.replace("https://","")
                clean_url = clean_url.replace("http://","")
                clean_url = clean_url.replace("m.","")
                clean_url = clean_url.replace("fxtwitter","x")
                clean_url = clean_url.replace("vxtwitter","x")
                clean_url = clean_url.replace("twitter","x")
                if await _autosnailFind(URLS_PATH,clean_url,message.author.id):
                    snail = True


                # Snail if snailable, else add to list
                if snail:
                    double_snail = False
                    # Sparkle/double snail
                    if await _autosnailFind(URLS_SNAILED_PATH,clean_url,message.author.id):
                        double_snail = True

                    # Normal snail
                    emoji = '\U0001F40C' #Snail
                    if message.author.id == 178130280400420864: #Jaysnail
                        emoji = discord.utils.get(bot.emojis, name="snailuri") #'<:snailuri:968161545035071498>'
                    if double_snail:
                        emoji = discord.utils.get(bot.emojis, name="sparklesnail") #'<:sparklesnail:>'
                        await snailScores(message.author.id,2)
                    else:
                        await snailScores(message.author.id,1)
                        with open(URLS_SNAILED_PATH, "a+") as file:
                            newline = str(message.author.id) + '>' + str(int(time.time())) + '>' + clean_url + '\n'
                            file.write(newline)

                    await message.add_reaction(emoji)
                    return True
                else:
                    with open(URLS_PATH, "a+") as file:
                        newline = str(message.author.id) + '>' + str(int(time.time())) + '>' + clean_url + '\n'
                        file.write(newline)
    return False