import discord
import json
import sqlite3
from io import StringIO
from discord.ext import commands

conn = sqlite3.connect('configs/QuoteBot.db')
c = conn.cursor()

global blacklist_ids
blacklist_ids = []

c.execute("SELECT Id FROM Blacklist")
blacklist_ids_raw = c.fetchall()
for i in blacklist_ids_raw:
	blacklist_ids.append(int(i[0]))
del blacklist_ids_raw

with open('config.json') as json_data:
	response_json = json.load(json_data)
	owners = response_json['owner_ids']

class Owneronly:
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def blacklistadd(self, ctx, id_input):
		if ctx.author.id in owners:
			try:
				c.execute("INSERT INTO Blacklist (Id) VALUES ('" + str(id_input) + "')")
				conn.commit()
				blacklist_ids.append(int(id_input))
				await ctx.send(content = 'Successfully blacklisted ID `' + str(id_input) + '`.')
				if ctx.guild.id == int(id_input):
					await ctx.send(content = 'It appears that the ID that you blacklisted is this current server, so I\'m leaving it. :wave:')
					await ctx.guild.leave()
			except sqlite3.IntegrityError:
				await ctx.send(content = 'The following ID is already blacklisted. Did you want to unblacklist it instead?')

	@commands.command()
	async def blacklistremove(self, ctx, id_input):
		if ctx.author.id in owners:
			c.execute("DELETE FROM Blacklist WHERE Id = " + str(id_input))
			conn.commit()
			blacklist_ids.remove(int(id_input))
			await ctx.send(content = 'Unblacklisted ID `' + str(id_input) + '`.')

	@commands.command()
	async def shutdown(self, ctx):
		if ctx.author.id in owners:
			await ctx.send(content = '<:check:314349398811475968> **Shutting down.**')
			await self.bot.logout()


def setup(bot):
	bot.add_cog(Owneronly(bot))
