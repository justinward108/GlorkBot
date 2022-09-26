from io import BytesIO
import requests
import pdfplumber
import interactions
import config

url = 'https://www.marscna.org/wp-content/uploads/2022/01/SPAD-ApprovalDraft_Jan22_1_WEB.pdf'

class spad(interactions.Extension):
	def __init__(self, client: interactions.Client):
		self.client: interactions.Client = client

	@interactions.extension_command(
		name='spad',
		description='spiritual principle a day',
		options=[
			interactions.Option(
			name='page',
			description='enter page no. of document',
			type=interactions.OptionType.INTEGER,
			required=True,
			),
		],
	)

	async def ext_command(self, ctx:interactions.CommandContext, page: int):
		await ctx.defer(ephemeral=False)
		r = requests.get(url)
		with pdfplumber.open(BytesIO(r.content)) as pdf:
			extracted_page = pdf.pages[page-1].extract_text()
		chunklength = 1900
		chunks = [extracted_page[i:i+chunklength] for i in range (0, len(extracted_page), chunklength)]
		for chunk in chunks:
			for i in range(0, len(chunk)):
				if chunk[i] == '\n':
					if chunk[i-1] == ' ':
						if chunk[i-2] == '.' or chunk[i-2] == '"' or chunk[i-2] == '!' or chunk[i-2] == ' ':
							chunk = chunk[:i] + '\n' + chunk[i:]
				
			await ctx.send('```'+chunk+'```')
def setup(client):
	spad(client)

