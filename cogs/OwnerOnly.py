import discord
import json
from DBService import DBService
from discord.ext import commands

blacklist_ids = DBService.exec("SELECT Id FROM Blacklist").fetchall()
blacklist_ids = [int(i[0]) for i in blacklist_ids]

with open('configs/config.json') as json_data:
	response_json = json.load(json_data)
	owners = response_json['owner_ids']
	success_string = response_json['response_string']['success']
	error_string = response_json['response_string']['error']
	del response_json

def is_owner(ctx):
	return ctx.author.id in owners

class Owneronly(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	@commands.check(is_owner)
	async def donator(self, ctx, user_id: int):
		patrons = [int(i[0]) for i in DBService.exec("SELECT UserId FROM Donators").fetchall()]
		if user_id not in patrons:
			user = self.bot.get_user(user_id)
			if not user:
				try:
					user = await self.bot.get_user_info(user_id)
				except discord.NotFound:
					return await ctx.send(content = error_string + ' **That user does not exist.**')

			DBService.exec("INSERT INTO Donators (UserId, UserTag) VALUES (" + str(user_id) + ", '" + str(user) + "')")
			await ctx.send(content = success_string + ' **Added `' + str(user) + '` to the donators list.**')
		else:
			DBService.exec("DELETE FROM Donators WHERE UserId = " + str(user_id))
			user = self.bot.get_user(user_id)
			if not user:
				user = await self.bot.get_user_info(user_id)

			await ctx.send(content = success_string + ' **Removed `' + str(user) + '` from the donators list.**')

	@commands.command()
	@commands.check(is_owner)
	async def blacklistadd(self, ctx, object_id: int, *, reason = None):
		try:
			if reason:
				DBService.exec("INSERT INTO Blacklist (Id, Reason) VALUES (" + str(object_id) + ", '" + reason.replace('\'', '\'\'') + "')")
			else:
				DBService.exec("INSERT INTO Blacklist (Id) VALUES (" + str(object_id) + ")")
		except sqlite3.IntegrityError:
			await ctx.send(content = error_string + ' **That ID is already blacklisted.**')
		else:
			blacklist_ids.append(object_id)
			await ctx.send(content = success_string + ' **Successfully blacklisted:** `' + str(object_id) + '`')
			guild = self.bot.get_guild(object_id)
			if guild:
				await guild.leave()

	@commands.command()
	@commands.check(is_owner)
	async def blacklistcheck(self, ctx, object_id: int):
		blacklist_raw = DBService.exec("SELECT * FROM Blacklist WHERE Id = " + str(object_id)).fetchone()
		if not blacklist_raw:
			await ctx.send(content = error_string + ' **That ID is not blacklisted.**')
		else:
			await ctx.send(content = success_string + ' **That ID is blacklisted.**\n\n**Reason:** ' + str(blacklist_raw[1]))

	@commands.command()
	@commands.check(is_owner)
	async def blacklistremove(self, ctx, object_id: int):
		try:
			blacklist_ids.remove(object_id)
		except ValueError:
			await ctx.send(content = error_string + ' **That ID is not blacklisted.**')
		else:
			DBService.exec("DELETE FROM Blacklist WHERE Id = " + str(object_id))
			await ctx.send(content = success_string + ' **Successfully unblacklisted:** `' + str(object_id) + '`')

	@commands.command()
	@commands.check(is_owner)
	async def leave(self, ctx, guild_id: int):
		guild = self.bot.get_guild(guild_id)
		if guild:
			await guild.leave()
			await ctx.send(content = success_string + ' **Successfully left guild.**')
		else:
			await ctx.send(content = error_string + ' **No such server found.**')

	@commands.command()
	@commands.check(is_owner)
	async def shutdown(self, ctx):
		await ctx.send(content = success_string + ' **Shutting down.**')
		DBService.commit()
		await self.bot.logout()


def setup(bot):
	bot.add_cog(Owneronly(bot))
