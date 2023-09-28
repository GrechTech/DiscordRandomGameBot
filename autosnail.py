import datetime
import os
import re
import time
import discord

dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)))
urls_path = os.path.join(dir_path, "Config", "urls.txt")
urls_snailed_path = os.path.join(dir_path, "Config", "urls_snailed.txt")
urls_scores_path = os.path.join(dir_path, "Config", "Scores")

if not os.path.exists(urls_path):
    with open(urls_path, "w+") as f:
        f.write('')
if not os.path.exists(urls_path):
    with open(urls_snailed_path, "w+") as f:
        f.write('')
if not os.path.exists(urls_scores_path):
    os.mkdir(urls_scores_path)


# Auto Snail find URL
def find_url(string):
    # findall() has been used 
    # with valid conditions for urls in string
    regex = (r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s("
             r")<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))")
    url = re.findall(regex, string)
    return [x[0] for x in url]


# Auto Snail find URL in list
async def autosnail_find(path, clean_url, author_id):
    snail = False
    newlines = []
    # Check each line of file

    with open(path, "r") as file:
        for line in file:
            clean_line = line.rstrip()
            id_val = int(clean_line.split('>')[0])
            date = int(clean_line.split('>')[1])
            lineurl = clean_line.split('>')[2]
            # Check if message within last 3 days
            if (int(time.time()) - date) < (86400 * 3):
                newlines.append(clean_line)  # Create new list with in date messages
                if lineurl == clean_url and author_id != id_val:  # If message a Snail
                    snail = True
                    await snail_scores(id_val, -1)

    # Create new file with only in date messages   
    with open(path, "w+") as file:
        for item in newlines:
            file.write("%s\n" % item)

    return snail


def argsort(seq):
    return sorted(range(len(seq)), key=seq.__getitem__)


async def leaderboard(bot):
    print("Leaderboards")
    entries = {}
    embed_message = ""

    # Read values from scoring files and create unsorted dictionary
    for filename in os.listdir(urls_scores_path):
        url_f = os.path.join(urls_scores_path, filename)
        if os.path.isfile(url_f):
            with open(url_f, "r+") as file:
                score = int(file.read().rstrip())
                user = await bot.fetch_user(int(filename))
                entries[user] = score
    # Sort dictionary
    entries_keys = list(entries.keys())
    entries_values = list(entries.values())
    entries_sorted_value_index = argsort(entries_values)
    entries_sorted = {entries_keys[i]: entries_values[i] for i in entries_sorted_value_index}

    # Output
    for key, value in entries_sorted.items():
        embed_message += str(key).split('#')[0] + ": " + str(value) + "\n"
    embed = discord.Embed(title="Snail Score List", description=embed_message, color=0xF6B600)
    print(embed)
    return embed


async def snail_delete_check(message, bot):
    if not message.author.bot:
        for react in message.reactions:
            if '\U0001F40C' == react.emoji \
                    or discord.utils.get(bot.emojis, name="snailuri") == react.emoji \
                    or discord.utils.get(bot.emojis, name="sparklesnail") == react.emoji:
                embed = discord.Embed(title="Snailed Message Deleted")
                embed.add_field(name="Member: ", value=message.author.mention, inline=False)
                embed.add_field(name="Message: ", value=message.content, inline=True)
                print("Snail Deleted Hit")
                await message.channel.send(embed=embed)
                return


async def snail_scores(id_val, score_delta):
    score_path = os.path.join(urls_scores_path, str(id_val))
    score = 0
    if os.path.exists(score_path):
        with open(score_path, "r+") as file:
            score = int(file.read().rstrip())
    score += score_delta
    with open(score_path, "w+") as file:
        file.write(str(score))


async def check_valid_url(url):
    to_check = ['framed.wtf', 'timeguessr.com', 'oec.world/en/tradle', ' moviedle.app', 'squirdle.fireblend.com',
                'sweardle.com/herdle', '.png', '.gif', '.jpg', '.jpeg', 'discordapp', 'tenor', 'gstatic']
    name_delete = ["www.", "m.", "https://", "http://"]
    x_name = ["fxtwitter", "vxtwitter", "twitter"]
    output_url = ""
    clean_url = url.rstrip().lower()
    if not [ele for ele in to_check if (ele in clean_url)]:
        if "youtube.com/watch?v=" in clean_url:
            clean_url = clean_url.replace("youtube.com/watch?v=", "youtu.be/")
        clean_url = clean_url.split("?")[0].lower().split("#")[0].lower()
        for name in name_delete:
            clean_url = clean_url.replace(name, "")
        for name in x_name:
            clean_url = clean_url.replace(name, "x")
        output_url = clean_url
    return output_url


async def auto_snail(message, bot):
    urls = find_url(message.content)
    # Check message for url
    if len(urls) > 0:
        for url in urls:
            clean_url = check_valid_url(url)
            if clean_url != "":
                if await autosnail_find(urls_path, clean_url, message.author.id):
                    print("Snail Hit")
                    double_snail = False
                    # Sparkle/double snail
                    if await autosnail_find(urls_snailed_path, clean_url, message.author.id):
                        double_snail = True

                    # Normal snail
                    emoji = '\U0001F40C'  # Snail
                    if message.author.id == 178130280400420864:  # Jaysnail
                        emoji = discord.utils.get(bot.emojis, name="snailuri")  # '<:snailuri:968161545035071498>'
                    if double_snail:
                        emoji = discord.utils.get(bot.emojis, name="sparklesnail")  # '<:sparklesnail:>'
                        await snail_scores(message.author.id, 2)
                    else:
                        await snail_scores(message.author.id, 1)
                        with open(urls_snailed_path, "a+") as file:
                            newline = str(message.author.id) + '>' + str(int(time.time())) + '>' + clean_url + '\n'
                            file.write(newline)

                    await message.add_reaction(emoji)
                    return True
                else:
                    with open(urls_path, "a+") as file:
                        newline = str(message.author.id) + '>' + str(int(time.time())) + '>' + clean_url + '\n'
                        file.write(newline)
    return False


async def auto_snail_safe(message, bot):
    # AUTOSNAIL
    try:
        await auto_snail(message, bot)
    except discord.errors.Forbidden:
        print("Autosnail Fail")
        embed = discord.Embed(title=":sparklesnail: Blocked Snail Alert")
        embed.add_field(name="Member: ", value=message.author.mention, inline=False)
        embed.add_field(name="Message: ",
                        value="Previous message requires snailing. Automatic snail failure due to user blocking "
                              "Garry. Attempting to bypass Garry is a serious offence that can warrant snail time.",
                        inline=True)
        await message.channel.send(embed=embed)


def get_date(type):
    today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    this_month = today.replace(day=1)
    this_year = this_month.replace(month=1)
    if type == 'l':  # First day of leaderboards
        return datetime.date(2013, 8, 15)
    elif type == 'd':
        return today
    elif type == 'm':
        return this_month
    elif type == 'y':
        return this_year


def verify_url(content):
    urls = find_url(content)
    # Check message for url
    valid = False
    if len(urls) > 0:
        for url in urls:
            clean_url = check_valid_url(url)
            if clean_url != "":
                valid = True
    return valid


async def snail_search(ctx, bot, date_type):
    entries = {}
    print("## Retrieving messages")
    async for message in ctx.channel.history(after=get_date(date_type)):
        if not message.author.bot and verify_url(message.content):
            for react in message.reactions:
                if '\U0001F40C' == react.emoji \
                        or discord.utils.get(bot.emojis, name="snailuri") == react.emoji:
                    print("## Snail Found " + message.author.name)
                    if message.author.name not in entries:
                        entries[message.author.name] = 1
                    else:
                        entries[message.author.name] += 1
                if discord.utils.get(bot.emojis, name="sparklesnail") == react.emoji:
                    print("## Snail Found (x2) " + message.author.name)
                    if message.author.name not in entries:
                        entries[message.author.name] = 2
                    else:
                        entries[message.author.name] += 2
    # Sort dictionary
    entries_keys = list(entries.keys())
    entries_values = list(entries.values())
    entries_sorted_value_index = argsort(entries_values)
    entries_sorted = {entries_keys[i]: entries_values[i] for i in entries_sorted_value_index}

    # Output
    embed_message = ""
    for key, value in entries_sorted.items():
        embed_message += str(key).split('#')[0] + ": " + str(value) + "\n"
    embed = discord.Embed(title="Snail Score List", description=embed_message, color=0xF6B600)
    print(embed)
    return embed
