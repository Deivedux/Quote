import discord
import json
import sqlite3
from io import StringIO
from discord.ext import commands

conn = sqlite3.connect('configs/QuoteBot.db')
c = conn.cursor()

blacklist_raw = c.execute("SELECT Id FROM Blacklist").fetchall()
blacklist_ids = [int(i[0]) for i in blacklist_raw]
del blacklist_raw

with open('configs/config.json') as json_data:
	response_json = json.load(json_data)
	owners = response_json['owner_ids']
	success_string = response_json['response_string']['success']
	error_string = response_json['response_string']['error']
	del response_json

class Owneronly:
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def donator(self, ctx, user_id: int):
		if ctx.author.id in owners:
			patrons = [int(i[0]) for i in c.execute("SELECT UserId FROM Donators").fetchall()]
			if user_id not in patrons:
				user = self.bot.get_user(user_id)
				if not user:
					try:
						user = await self.bot.get_user_info(user_id)
					except discord.NotFound:
						return await ctx.send(content = error_string + ' **That user does not exist.**')

				c.execute("INSERT INTO Donators (UserId, UserTag) VALUES (" + str(user_id) + ", '" + str(user) + "')")
				conn.commit()

				await ctx.send(content = success_string + ' **Added `' + str(user) + '` to the donators list.**')
			else:
				c.execute("DELETE FROM Donators WHERE UserId = " + str(user_id))
				conn.commit()

				user = self.bot.get_user(user_id)
				if not user:
					user = await self.bot.get_user_info(user_id)

				await ctx.send(content = success_string + ' **Removed `' + str(user) + '` from the donators list.**')

	@commands.command()
	async def blacklistadd(self, ctx, object_id: int, *, reason = None):
		if ctx.author.id in owners:
			try:
				if reason:
					c.execute("INSERT INTO Blacklist (Id, Reason) VALUES (" + str(object_id) + ", '" + reason.replace('\'', '\'\'') + "')")
					conn.commit()
				else:
					c.execute("INSERT INTO Blacklist (Id) VALUES (" + str(object_id) + ")")
					conn.commit()
			except sqlite3.IntegrityError:
				await ctx.send(content = error_string + ' **That ID is already blacklisted.**')
			else:
				blacklist_ids.append(object_id)
				await ctx.send(content = success_string + ' **Successfully blacklisted:** `' + str(object_id) + '`')
				guild = self.bot.get_guild(object_id)
				if guild:
					await guild.leave()

	@commands.command()
	async def blacklistcheck(self, ctx, object_id: int):
		if ctx.author.id in owners:
			blacklist_raw = c.execute("SELECT * FROM Blacklist WHERE Id = " + str(object_id)).fetchone()
			if not blacklist_raw:
				await ctx.send(content = error_string + ' **That ID is not blacklisted.**')
			else:
				await ctx.send(content = success_string + ' **That ID is blacklisted.**\n\n**Reason:** ' + str(blacklist_raw[1]))

	@commands.command()
	async def blacklistremove(self, ctx, object_id: int):
		if ctx.author.id in owners:
			try:
				blacklist_ids.remove(object_id)
			except ValueError:
				await ctx.send(content = error_string + ' **That ID is not blacklisted.**')
			else:
				c.execute("DELETE FROM Blacklist WHERE Id = " + str(object_id))
				conn.commit()
				await ctx.send(content = success_string + ' **Successfully unblacklisted:** `' + str(object_id) + '`')

	@commands.command()
	async def leave(self, ctx, guild_id: int):
		if ctx.author.id in owners:
			guild = self.bot.get_guild(guild_id)
			if guild:
				await guild.leave()
				await ctx.send(content = success_string + ' **Successfully left guild.**')
			else:
				await ctx.send(content = error_string + ' **No such server found.**')

	@commands.command()
	async def shutdown(self, ctx):
		if ctx.author.id in owners:
			await ctx.send(content = success_string + ' **Shutting down.**')
			await self.bot.logout()


def setup(bot):
	bot.add_cog(Owneronly(bot))
