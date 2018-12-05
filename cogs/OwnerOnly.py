import discord
import json
import sqlite3
from io import StringIO
from discord.ext import commands

conn = sqlite3.connect('configs/QuoteBot.db')
c = conn.cursor()

with open('config.json') as json_data:
	response_json = json.load(json_data)
	owners = response_json['owner_ids']

class Owneronly:
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def shutdown(self, ctx):
		if ctx.author.id in owners:
			await ctx.send(content = '<:check:314349398811475968> **Shutting down.**')
			await self.bot.logout()


def setup(bot):
	bot.add_cog(Owneronly(bot))
