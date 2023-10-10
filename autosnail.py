from datetime import datetime
from datetime import timezone
from datetime import timedelta
from urlextract import URLExtract
import os
import _pickle as pickle
import time
import discord

dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)))
urls_path = os.path.join(dir_path, "Config", "urls.txt")
urls_snailed_path = os.path.join(dir_path, "Config", "urls_snailed.txt")
urls_scores_path = os.path.join(dir_path, "Config", "Scores")
activity_path = os.path.join(dir_path, "Config", "Activity")

initialised = False  # Whether the leaderboards have fully updated

if not os.path.exists(urls_path):
    with open(urls_path, "w+") as f:
        f.write('')
if not os.path.exists(urls_path):
    with open(urls_snailed_path, "w+") as f:
        f.write('')
if not os.path.exists(urls_scores_path):
    os.mkdir(urls_scores_path)
if not os.path.exists(activity_path):
    os.mkdir(activity_path)


# Auto Snail find URL
def find_url(string):
    extractor = URLExtract()
    urls = extractor.find_urls(string)
    return urls


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
            line_url = clean_line.split('>')[2]
            # Check if message within last 3 days
            if (int(time.time()) - date) < (86400 * 3):
                newlines.append(clean_line)  # Create new list with in date messages
                if line_url == clean_url and author_id != id_val:  # If message a Snail
                    snail = True
                    await snail_scores(id_val, -1)

    # Create new file with only in date messages   
    with open(path, "w+") as file:
        for item in newlines:
            file.write("%s\n" % item)

    return snail


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
    entries_sorted_value_index = sorted(range(len(entries_values)), key=entries_values.__getitem__)
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
                    if message.author.id == 178130280400420864:  # Jay snail
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


def get_date(date_type):
    today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=timezone.utc)
    this_month = today.replace(day=1)
    this_year = this_month.replace(month=1)
    yesterday = today - timedelta(days=1)
    last_week = today - timedelta(days=7)
    if date_type == 'l':  # First day of leaderboards
        return datetime(2023, 8, 15, tzinfo=timezone.utc)
    elif date_type == "birthday" or date_type == "b" or date_type == "all":
        return datetime(2022, 3, 17, tzinfo=timezone.utc)
    elif date_type == "today" or date_type == "day" or date_type == "d":
        return today
    elif date_type == "yesterday":
        return yesterday
    elif date_type == "week" or date_type == "w":
        return last_week
    elif date_type == "month" or date_type == "m":
        return this_month
    elif date_type == "year" or date_type == "y":
        return this_year


def check_valid_url(url):
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


def verify_url(content):
    urls = find_url(content)
    # Check message for url
    valid = False
    if len(urls) > 0:
        for url in urls:
            clean_url = check_valid_url(url)
            if clean_url != "":
                valid = True
                print(clean_url)
    return valid


class MessageData:
    def __init__(self, author_name, created_at, snails, content):
        self.author_name = author_name
        self.created_at = created_at
        self.snails = snails
        self.content = content


async def store_messages(channel_id, messages):
    print("Write start")
    with open(os.path.join(activity_path, str(channel_id)), "wb+") as outfile:
        pickle.dump(messages, outfile)
        print("Write successful")


async def read_messages(channel_id):
    try:
        print("Read Start " + str(channel_id))
        file_name = os.path.join(activity_path, str(channel_id))
        message_json = []
        if os.path.isfile(file_name):
            with open(file_name, 'rb') as infile:
                # Reading from json file
                print("Read Open " + str(file_name))
                message_json = pickle.load(infile)
                print("Type1: " + str(type(message_json)))
                print("Read successful")
        print("Read done")
        return message_json
    except EOFError as e:
        print(e)
        print(str(type(message_json)))
        print(str(message_json))
        return []


async def get_history(bot, update):
    global initialised
    print("## Get history, Update: " + str(update))
    for guild in bot.guilds:
        for channel in guild.text_channels:
            counter = 0
            message_store = []
            after_date = datetime(2022, 3, 17)
            before_date = datetime.now()
            if os.path.isfile(os.path.join(activity_path, str(channel.id))):
                message_store = await read_messages(channel.id)
                message_store_size = len(message_store)
                print("## Existing messages stored: " + str(message_store_size))
                print("From: " + str(message_store[0].created_at) + " to " + str(message_store[-1].created_at))
                if message_store_size > 0:
                    if update:
                        after_date = message_store[0].created_at
                    else:
                        before_date = message_store[-1].created_at
            print("## Start datetime " + str(after_date))
            print("## End datetime " + str(before_date))
            async for message in channel.history(after=after_date, before=before_date, limit=None,
                                                 oldest_first=False):
                if (not message.author.bot) and verify_url(message.content):
                    snails = 0
                    for react in message.reactions:
                        users = [user async for user in react.users()]
                        if bot.user in users:
                            if '\U0001F40C' == react.emoji \
                                    or discord.utils.get(bot.emojis, name="snailuri") == react.emoji:
                                snails = 1
                                print("## Snail Found " + message.author.name)
                            if discord.utils.get(bot.emojis, name="sparklesnail") == react.emoji:
                                snails = 2
                                print("## Double Snail Found " + message.author.name)
                    message_item = MessageData(message.author.name, message.created_at, snails, message.content)
                    if update:
                        message_store.insert(0, message_item)
                    else:
                        message_store.append(message_item)
                    counter += 1
                    if counter % 100 == 0:
                        print(str(channel.id) + " " + str(counter))
                        await store_messages(channel.id, message_store)
            print("## Completed Get history " + str(channel.id) + " size: " + str(counter))
            print("## Newest datetime " + str(message_store[0].created_at))
            print("## Oldest datetime " + str(message_store[-1].created_at))
            await store_messages(channel.id, message_store)
    initialised = True
    print("## History initialised")


async def write_leaderboard(ctx, date_type):
    entries = {}
    entries_activity = {}
    search_date = get_date(date_type)
    counter = 0
    snailer_data = []
    for channel in ctx.guild.text_channels:
        if initialised:
            print("## Updating new messages")
            await get_history(channel, True)
        print("## Checking messages")
        print("## Search date: " + str(search_date))
        message_store = await read_messages(channel.id)
        print("## Messages ready")
        oldest_message_date = message_store[-1].created_at
        print("Oldest date: " + str(oldest_message_date))
        still_updating = search_date < oldest_message_date
        print("Waiting: " + str(still_updating))
        
        print("## Store ID: " + str(channel.id))
        print("## Store size: " + str(len(message_store)))
        for message in message_store:
            if message.created_at < search_date:
                break
            if message.snails == 0:
                negatives = snailer_data.count(check_valid_url(message.content))
                if negatives > 0:
                    if message.author_name not in entries:
                        entries[message.author_name] = negatives * -1
                    else:
                        entries[message.author_name] -= negatives
                    # remove the item for all its occurrences 
                    for i in range(negatives):
                        snailer_data.remove(check_valid_url(message.content))
            else:
                if message.author_name not in entries:
                    entries[message.author_name] = message.snails
                else:
                    entries[message.author_name] += message.snails

                if message.author_name not in entries_activity:
                    entries_activity[message.author_name] = message.snails
                else:
                    entries_activity[message.author_name] += message.snails

                snailer_data.append(check_valid_url(message.content))
            counter += 1

    print("## Messages counted: " + str(counter))
    # Sort dictionary
    entries_keys = list(entries.keys())
    entries_values = list(entries.values())
    entries_sorted_value_index = sorted(range(len(entries_values)), key=entries_values.__getitem__)
    entries_sorted = {entries_keys[i]: entries_values[i] for i in entries_sorted_value_index}
    print("## Snails sorted")
    # Output
    embed_message = ""
    for key, value in entries_sorted.items():
        embed_message += str(key).split('#')[0] + ": " + str(value) + " (" + str(entries_activity[key]) + ") \n"
    if still_updating:
        embed = discord.Embed(title="Snail Score List (Updating)", description=embed_message, color=0xF6B600)
    else:
        embed = discord.Embed(title="Snail Score List", description=embed_message, color=0xF6B600)
    print(embed)
    return embed
