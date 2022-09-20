import interactions
from bs4 import BeautifulSoup
import requests
import pymongo
from pymongo import MongoClient
from datetime import date as Date
from datetime import datetime

bot = interactions.Client(token="MTAxODQ2ODQ5MjI4ODIxNzA5OA.GgzRkY.qj4HYWll42cooIDKKPOpO8j1M9-9F07-cas15U")
cluster = MongoClient("mongodb+srv://rebel:1234@cluster0.0lyb0.mongodb.net/?retryWrites=true&w=majority")
url = 'https://www.jftna.org/jft/'

db = cluster["users"]
collection = db["clean_time"]
@bot.event
async def on_ready():
    print('------')

@bot.command(
    name="jft",
    description="For daily readings",
    #scope=the_id_of_your_guild,
)
async def jft(ctx: interactions.CommandContext):
    r = requests.get(url)
    s = BeautifulSoup(r.text, 'html.parser')
    text = "```"
    for tag in s.find_all('tr'):
        text += tag.text
        text += '\n' 
    text += "```"
    await ctx.send(text)

@bot.command(
    name="clean_time",
    #scope=guild_id,
    options=[
        interactions.Option(
            name="store",
            description="To save your clean time",
            type=interactions.OptionType.SUB_COMMAND,
            options=[
                interactions.Option(
                    name="year",
                    description="Enter year",
                    type=interactions.OptionType.INTEGER,
                    required=True,
                ),
                interactions.Option(
                    name="month",
                    description="Enter month",
                    type=interactions.OptionType.INTEGER,
                    min_value=1,
                    max_value=12,
                    required=True,
                ),
                interactions.Option(
                    name = "date",
                    description = "Enter date",
                    type=interactions.OptionType.INTEGER,
                    min_value = 1,
                    max_value = 31,
                    required = True,
                ),
            ],
        ),
        interactions.Option(
            name="delete",
            description="To delete your date",
            type=interactions.OptionType.SUB_COMMAND,
        ),
        interactions.Option(
            name="get_clean_days",
            description="get number of clean days you have today",
            type=interactions.OptionType.SUB_COMMAND
        ),
        interactions.Option(
            name="clean_date",
            description="To know your last saved clean date",
            type=interactions.OptionType.SUB_COMMAND
        )
    ],
)
async def cmd(ctx: interactions.CommandContext, sub_command: str, year: int = None, month: int = None, date: int = None):
    if sub_command == "store":
        search = collection.find_one({"_id":str(ctx.author.id)})
        if search != None and search["_id"] == str(ctx.author.id):
            await ctx.send("Your date already exists!")
            return
        post = {"_id":str(ctx.author.id), "time": str(year)+str(month)+str(date)}
        collection.insert_one(post)
        await ctx.send("Done!")

    elif sub_command == "delete":
        status = collection.delete_one({"_id":str(ctx.author.id)})
        await ctx.send("Record deleted")

    elif sub_command == "get_clean_days":
        result = collection.find_one({"_id":str(ctx.author.id)})
        if result == None:
            await ctx.send("Your date doesnt exist. Please use store command")
            return
        clean_date = datetime.strptime(result["time"],"%Y%m%d")
        current_date = Date.today()
        current_date = datetime.combine(current_date, datetime.min.time())
        clean_days = current_date - clean_date
        await ctx.send("You are "+str(clean_days.days)+ " days clean")
    
    elif sub_command == "clean_date":
        result = collection.find_one({"_id":str(ctx.author.id)})
        if result == None:
            await ctx.send("Your date doesnt exist. Please use store command")
            return
        clean_date = datetime.strptime(result["time"],"%Y%m%d")
        await ctx.send(str(clean_date)+" in YMD")

@bot.command(
    name="info",
    description="General bot info",
    #scope=the_id_of_your_guild,
)
async def info(ctx: interactions.CommandContext):
    reply = "Current server time- "+str(datetime.utcnow())+" UTC\nConnection speed- "+str(round(bot.latency))+ " ms\nBot created by ^ReBeLLi0n^D#2343. Notify me if you find something broken I may or may not fix it lol"
    await ctx.send(reply)

bot.start()