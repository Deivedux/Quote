import discord
import json
import aiohttp
import asyncio
from DBService import DBService
from discord.ext import commands

embed_color = 0x399ad5
categories = [
	'Funny',
	'Meme',
	'Hater',
	'Mistake',
	'Party',
	'Inspirational',
	'Heartwarming',
	'Confidence']

with open('configs/config.json') as json_data:
	response_json = json.load(json_data)
	owners = response_json['owner_ids']
	webhook_url = response_json['botlog_webhook_url']
	success_string = response_json['response_string']['success']
	error_string = response_json['response_string']['error']
	del response_json

def quote_embed(category, quote):
	return discord.Embed(title = category + ' Quote', description = quote, color = embed_color)

def is_owner(ctx):
	return ctx.author.id in owners

def channel_is_private(ctx):
	return isinstance(ctx.channel, discord.DMChannel)

class RandomQuotes(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def randcategories(self, ctx):
		await ctx.send(embed = discord.Embed(title = 'Random Quote Categories', description = '\n'.join(['• ' + i for i in categories]), color = embed_color))

	@commands.command()
	@commands.check(channel_is_private)
	@commands.cooldown(rate = 5, per = 3600, type = commands.BucketType.user)
	async def randsubmit(self, ctx, category: str, *, quote: str):
		category = category.capitalize()
		if category in categories:
			DBService.exec("INSERT INTO RandomQuotes (Author, Category, Quote, Approved) VALUES (" + str(ctx.author.id) + ", '" + category + "', '" + quote.replace('\'', '\'\'') + "', 0)")
			await ctx.send(content = success_string + ' **Quote submitted.**\n\nPlease note that there is a queue of quotes to be looked at, and they are all checked in order of which they were submitted at.', embed = quote_embed(category, quote))
			async with aiohttp.ClientSession() as session:
				webhook = discord.Webhook.from_url(webhook_url, adapter = discord.AsyncWebhookAdapter(session))
				await webhook.send(content = ':speech_balloon: **Quote Submitted** in **' + category + '** by `' + str(ctx.author).strip('`') + '` (`' + str(ctx.author.id) + '`)')
		else:
			await ctx.send(content = error_string + ' **Category with that name does not exist.**')

	@commands.command()
	async def randquote(self, ctx, category: str = None):
		db_response = DBService.exec("SELECT Category, Quote FROM RandomQuotes WHERE Approved = 1" + (" AND Category = '" + category.capitalize().replace('\'', '\'\'') + "'" if category else "") + " ORDER BY RANDOM() LIMIT 1").fetchone()
		if not db_response:
			await ctx.send(content = error_string + ' **Either you misspelled the category name, or there are currently no quotes to display.**')
		else:
			await ctx.send(embed = quote_embed(db_response[0], db_response[1]))

	@commands.command()
	@commands.check(is_owner)
	async def randqueue(self, ctx):
		db_response = DBService.exec("SELECT * FROM RandomQuotes WHERE Approved = 0 LIMIT 1").fetchone()
		if db_response:
			await ctx.send(embed = quote_embed(db_response[2], db_response[3]).set_footer(text = 'Quote ID: ' + str(db_response[0]) + ' | Author ID: ' + str(db_response[1])))
		else:
			await ctx.send(content = error_string + ' **There are currently no unapproved quotes in the queue.**')

	@commands.command()
	@commands.check(is_owner)
	async def randapprove(self, ctx, quote_id: int):
		db_response = DBService.exec("SELECT * FROM RandomQuotes WHERE QuoteID = " + str(quote_id)).fetchone()
		if not db_response:
			await ctx.send(content = error_string + ' **Quote with that ID does not exist.**')
		elif db_response[4] == 1:
			await ctx.send(content = error_string + ' **Quote with that ID is already approved.**')
		else:
			DBService.exec("UPDATE RandomQuotes SET Approved = 1 WHERE QuoteID = " + str(quote_id))
			await ctx.send(content = success_string + ' **Quote approved.**', embed = quote_embed(db_response[2], db_response[3]))

			user = self.bot.get_user(db_response[1])
			if user:
				try:
					await user.send(content = success_string + ' **Your quote has been approved.**', embed = quote_embed(db_response[2], db_response[3]))
				except discord.Forbidden:
					pass

	@commands.command()
	@commands.check(is_owner)
	async def randdecline(self, ctx, quote_id: int, *, reason: str = None):
		db_response = DBService.exec("SELECT * FROM RandomQuotes WHERE QuoteID = " + str(quote_id)).fetchone()
		if not db_response:
			await ctx.send(content = error_string + ' **Quote with that ID does not exist.**')
		elif db_response[4] == 1:
			await ctx.send(content = error_string + ' **Quote with that ID is already approved.**')
		else:
			DBService.exec("DELETE FROM RandomQuotes WHERE QuoteID = " + str(quote_id))
			await ctx.send(content = success_string + ' **Quote declined.**', embed = quote_embed(db_response[2], db_response[3]))

			user = self.bot.get_user(db_response[1])
			if user:
				try:
					await user.send(content = error_string + ' **Your quote has been declined.**' + ('\n\n**Reason:**\n' + reason if reason else ''), embed = quote_embed(db_response[2], db_response[3]))
				except discord.Forbidden:
					pass


def setup(bot):
	bot.add_cog(RandomQuotes(bot))
