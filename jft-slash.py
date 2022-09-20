import interactions
import requests
from bs4 import BeautifulSoup
from datetime import date as Date
from datetime import datetime

url = 'https://www.jftna.org/jft/'


bot = interactions.Client(token="MTAxODQ2ODQ5MjI4ODIxNzA5OA.GgzRkY.qj4HYWll42cooIDKKPOpO8j1M9-9F07-cas15U")

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
    description="Gets your number of clean days",
    #scope=the_id_of_your_guild,
    options = [
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
        	min_value = 1,
        	max_value = 12,
        	required=True,
        ),
        interactions.Option(
        	name="date",
        	description="Enter date",
        	min_value = 1,
        	max_value = 31,
        	type=interactions.OptionType.INTEGER,
        	required=True,
        ),
    ],
)
async def clean_time(ctx: interactions.CommandContext, year: int, month: int, date: int):
	try:
		current_date = Date.today()
		current_date = datetime.combine(current_date, datetime.min.time())
		clean_date = datetime(year, month, date)
		clean_days = current_date - clean_date
		await ctx.send("You are "+str(clean_days.days)+" days clean")
	except ValueError:
		await ctx.send("Invalid date")


@bot.command(
    name="info",
    description="General bot info",
    #scope=the_id_of_your_guild,
)
async def info(ctx: interactions.CommandContext):
	reply = "Current server time- "+str(datetime.utcnow())+" UTC\nConnection speed- "+str(round(bot.latency))+ " ms\nBot created by ^ReBeLLi0n^D#2343. Notify me if you find something broken I may or may not fix it lol"
	await ctx.send(reply)
bot.start()



