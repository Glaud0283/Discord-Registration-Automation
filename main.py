from discord.ext import commands
import discord

class MyBot(commands.Bot):
	'''
	Bot Object
	'''
	def __init__(self):
		intents = discord.Intents.all()
		self.initial_extensions = ['registry',]
		super().__init__(command_prefix = "!", intents = intents)
	async def setup_hook(self):
		for ext in self.initial_extensions:
			await self.load_extension(ext)
					
	async def on_ready(self):
		print("Bot is Ready!")

	
client = MyBot()
client.run("token",reconnect=True)
