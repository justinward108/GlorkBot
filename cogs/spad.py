from io import BytesIO
import aiohttp
import pdfplumber
import interactions
import config
import datetime
import asyncio

url = 'https://www.marscna.org/wp-content/uploads/2022/01/SPAD-ApprovalDraft_Jan22_1_WEB.pdf'

class spad(interactions.Extension):
	def __init__(self, client: interactions.Client):
		self.client: interactions.Client = client

	def pdf_process(self, r, page):
		with pdfplumber.open(BytesIO(r)) as pdf:
			if page != None:
				extracted_page = pdf.pages[page-1].extract_text()
			else:
				current_day = datetime.datetime.now().timetuple().tm_yday
				current_month = datetime.date.today().month
				page = current_day + current_month + 7
				year = datetime.date.today().year
				if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
					page -= 1
				extracted_page = pdf.pages[page-1].extract_text()
		chunklength = 1900
		
		indexes = []
		chunk = ''
		label = 0
		indexes = [i for i, letter in enumerate(extracted_page) if letter == '\n']
		for i in range(0,len(indexes)):
			if extracted_page[indexes[i]-1] == ' ':
				if extracted_page[indexes[i]-2] == '.' or extracted_page[indexes[i]-2] == '"' or extracted_page[indexes[i]-2] == '!' or extracted_page[indexes[i]-2] == ' ' or extracted_page[indexes[i]-2] == '?':
					if label == 0:
						label = indexes[i]
						chunk = extracted_page[:indexes[i]] + '\n'
					else:
						chunk += extracted_page[label:indexes[i]] + '\n'
						label = indexes[i]
		chunk += extracted_page[label:len(extracted_page)-1]
		chunks = [chunk[i:i+chunklength] for i in range (0, len(chunk), chunklength)]
		return chunks

	@interactions.extension_command(
		name='spad',
		description='spiritual principle a day',
		options=[
			interactions.Option(
			name='page',
			description='page no. of pdf (not book and leave it empty for todays reading)',
			type=interactions.OptionType.INTEGER,
			min_value = 0,
			max_value = 392,
			),
		],
	)

	async def ext_command(self, ctx:interactions.CommandContext, page: int = None):
		await ctx.defer(ephemeral=False)
		loop = asyncio.get_running_loop()
		async with aiohttp.ClientSession() as session:
			async with session.get(url) as response:
				r = await response.content.read()
				chunk = await loop.run_in_executor(None, self.pdf_process, r, page)
				for i in range(0,len(chunk)):
					await ctx.send('```'+chunk[i]+'```')
def setup(client):
	spad(client)

