import fitz
import interactions
import datetime
import asyncio

class spad(interactions.Extension):
	def __init__(self, client: interactions.Client):
		self.client: interactions.Client = client

	disk_pdf = fitz.open('1.pdf')
	mem = disk_pdf.tobytes()
	mem_pdf = fitz.open('pdf',mem)
	disk_pdf.close()

	def pdf_process(self, page):
		if page != None:
			req_page = spad.mem_pdf.load_page(page-1)
			extracted_page = list(req_page.get_text('text',sort=True))
		else:
			current_day = datetime.datetime.now().timetuple().tm_yday
			current_month = datetime.date.today().month
			page = current_day + current_month + 7
			year = datetime.date.today().year
			if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
				page -= 1
			req_page = spad.mem_pdf.load_page(page-1)
			extracted_page = list(req_page.get_text('text',sort=True))
		chunklength = 1900
		
		indexes = []
		chunk = []
		label = 0
		formatting_chars = ['.',' ','!','?','"']
		indexes = [i for i, letter in enumerate(extracted_page) if letter == '\n']
		_=indexes.pop(0)
		_=indexes.pop(3)
		for i in range(len(indexes)):
			if extracted_page[indexes[i]-1] == ' ':
				if extracted_page[indexes[i]-2] in formatting_chars:
					chunk.extend(extracted_page[label:indexes[i]])
					chunk += ['\n']
					label = indexes[i]
				else:
					extracted_page[indexes[i]] = '\u200b'
			else:
				extracted_page[indexes[i]] = '\u200b'
		chunk.extend(extracted_page[label:len(extracted_page)-1])
		chunk = ''.join(chunk)
		chunks = [chunk[i:i+chunklength] for i in range (0, len(chunk), chunklength)]
		chars = ['.',' ','!','?',',','\n']
		for i in range(0, len(chunks), 2):
			if len(chunks) == 1:
				break
			x=list(chunks[i])
			y=list(chunks[i+1])
			for l in range(chunklength-1,len(chunk)):
				if chunk[l+1] not in chars:
					x.append(chunk[l+1])
					_=y.pop(0)
				else:
					break
			chunks[i] = ''.join(x)
			chunks[i+1] = ''.join(y)
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
		chunk = await self.client._loop.run_in_executor(None, self.pdf_process, page)
		for i in range(0,len(chunk)):
			await ctx.send('```'+chunk[i]+'```')

def setup(client):
	spad(client)
