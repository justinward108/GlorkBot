from interactions import Extension, extension_command, Option, OptionType
from datetime import date as Date
from datetime import datetime

class clean_date(Extension):
	def __init__(self, client):
		self.client = client

	@extension_command(
		name="clean_time",
		description = "get your clean time in days from a date",
		options=[
			Option(
					name="year",
					description="Enter year",
					type=OptionType.INTEGER,
					required=True,
				),
				Option(
					name="month",
					description="Enter month",
					type=OptionType.INTEGER,
					min_value=1,
					max_value=12,
					required=True,
				),
				Option(
					name = "date",
					description = "Enter date",
					type=OptionType.INTEGER,
					min_value = 1,
					max_value = 31,
					required = True,
				),
			],
		)

	async def cmd(self, ctx, year: int = None, month: int = None, date: int = None):
		clean_date = datetime.strptime(str(year)+str(month)+str(date),"%Y%m%d")
		current_date = Date.today()
		current_date = datetime.combine(current_date, datetime.min.time())
		clean_days = current_date - clean_date
		if clean_days.total_seconds() < 0:
			await ctx.send("Please enter valid date")
			return
		await ctx.send("You are "+str(clean_days.days)+ " days clean")

def setup(client):
	clean_date(client)