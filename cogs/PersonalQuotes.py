import discord
import sqlite3
import json
from discord.ext import commands
from cogs.Main import del_commands

with open('configs/config.json') as json_data:
	response_json = json.load(json_data)
	success_string = response_json['response_string']['success']
	error_string = response_json['response_string']['error']
	del response_json

conn = sqlite3.connect('configs/QuoteBot.db')
c = conn.cursor()

def personal_embed(response, author):
	if isinstance(author, discord.Member) and author.color != discord.Colour.default():
		embed = discord.Embed(description = response, color = author.color)
	else:
		embed = discord.Embed(description = response)
	embed.set_author(name = str(author), icon_url = author.avatar_url)
	return embed

def list_embed(list_personals, author):
	if isinstance(author, discord.Member) and author.color != discord.Colour.default():
		embed = discord.Embed(description = '\n'.join(['• `' + i[1] + '`' for i in list_personals]), color = author.color)
	else:
		embed = discord.Embed(description = '\n'.join(['• `' + i[1] + '`' for i in list_personals]))
	embed.set_author(name = 'My Quotes', icon_url = author.avatar_url)
	return embed

class PersonalQuotes:
	def __init__(self, bot):
		self.bot = bot

	@commands.command(aliases = ['padd'])
	async def personaladd(self, ctx, trigger, *, response):
		user_quotes = c.execute("SELECT Trigger FROM PersonalQuotes WHERE User = " + str(ctx.author.id)).fetchall()
		if len(user_quotes) >= 10:
			return await ctx.send(content = error_string + ' **You have already exceeded your personal quotes limit.**')
		elif trigger in [i[0] for i in user_quotes]:
			return await ctx.send(content = error_string + ' **You already have a quote with that trigger.**')

		c.execute("INSERT INTO PersonalQuotes (User, Trigger, Response) VALUES (" + str(ctx.author.id) + ", '" + trigger.replace('\'', '\'\'') + "', '" + response.replace('\'', '\'\'') + "')")
		conn.commit()

		await ctx.send(content = success_string + ' **Quote added.**')

	@commands.command(aliases = ['premove'])
	async def personalremove(self, ctx, *, trigger):
		user_quotes = c.execute("SELECT * FROM PersonalQuotes WHERE User = " + str(ctx.author.id)).fetchall()
		if trigger in [i[1] for i in user_quotes]:
			c.execute("DELETE FROM PersonalQuotes WHERE User = " + str(ctx.author.id) + " AND Trigger = '" + trigger.replace('\'', '\'\'') + "'")
			conn.commit()
			await ctx.send(content = success_string + ' **Quote deleted.**')
		else:
			await ctx.send(content = error_string + ' **Quote with that trigger does not exist.**')

	@commands.command(aliases = ['p'])
	async def personal(self, ctx, *, trigger):
		user_quote = c.execute("SELECT * FROM PersonalQuotes WHERE User = " + str(ctx.author.id) + " AND Trigger = '" + trigger.replace('\'', '\'\'') + "'").fetchone()
		if not user_quote:
			await ctx.send(content = error_string + ' **No quote with that trigger exist.**')
		else:
			if ctx.guild and ctx.guild.id in del_commands:
				try:
					await ctx.message.delete()
				except discord.Forbidden:
					pass

			await ctx.send(embed = personal_embed(user_quote[2], ctx.author))

	@commands.command(aliases = ['plist'])
	async def personallist(self, ctx):
		user_quotes = c.execute("SELECT * FROM PersonalQuotes WHERE User = " + str(ctx.author.id)).fetchall()
		if len(user_quotes) == 0:
			await ctx.send(content = error_string + ' **You do not have any personal quotes.**')
		else:
			await ctx.send(embed = list_embed(user_quotes, ctx.author))


def setup(bot):
	bot.add_cog(PersonalQuotes(bot))
