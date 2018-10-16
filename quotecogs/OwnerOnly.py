import discord
import json
from io import StringIO
from discord.ext import commands

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
