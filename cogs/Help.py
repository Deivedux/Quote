import discord
import json
import sqlite3
from discord.ext import commands
from cogs.Main import prefixes

conn = sqlite3.connect('configs/QuoteBot.db')
c = conn.cursor()

class Help:
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def help(self, ctx, command = None):
		


def setup(bot):
	bot.add_cog(Help(bot))
