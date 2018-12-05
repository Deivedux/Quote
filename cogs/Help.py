import discord
import json
from discord.ext import commands
from cogs.Main import prefixes



class Help:
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def help(self, ctx, command = None):
		


def setup(bot):
	bot.add_cog(Help(bot))
