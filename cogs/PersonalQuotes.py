import discord
import json
import urllib
from DBService import DBService
from discord.ext import commands
from cogs.Main import server_config

with open('configs/config.json') as json_data:
	response_json = json.load(json_data)
	success_string = response_json['response_string']['success']
	error_string = response_json['response_string']['error']
	del response_json

def personal_embed(db_response, author):
	if isinstance(author, discord.Member) and author.color != discord.Colour.default():
		embed = discord.Embed(description = db_response[2], color = author.color)
	else:
		embed = discord.Embed(description = db_response[2])
	embed.set_author(name = str(author), icon_url = author.avatar_url)
	if db_response[3] != None:
		attachments = db_response[3].split(' | ')
		if len(attachments) == 1 and (attachments[0].lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.gifv', '.webp', '.bmp')) or attachments[0].lower().startswith('https://chart.googleapis.com/chart?')):
			embed.set_image(url = attachments[0])
		else:
			attachment_count = 0
			for attachment in attachments:
				attachment_count+=1
				embed.add_field(name = 'Attachment ' + str(attachment_count), value = attachment, inline = False)
	embed.set_footer(text = 'Personal Quote')
	return embed

def list_embed(list_personals, author, page_number):
	if isinstance(author, discord.Member) and author.color != discord.Colour.default():
		embed = discord.Embed(description = '\n'.join(['• `' + i[1] + '`' for i in list_personals]), color = author.color)
	else:
		embed = discord.Embed(description = '\n'.join(['• `' + i[1] + '`' for i in list_personals]))
	embed.set_author(name = 'Personal Quotes', icon_url = author.avatar_url)
	embed.set_footer(text = 'Page: ' + str(page_number))
	return embed

class PersonalQuotes(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(aliases = ['padd'])
	async def personaladd(self, ctx, trigger, *, response = None):
		if not response and not ctx.message.attachments:
			return await ctx.send(content = error_string + ' **You must include at least a response or an attachment in your message.**')
		else:
			try:
				DBService.exec("INSERT INTO PersonalQuotes (User, Trigger" + (", Response" if response else "") + (", Attachments" if ctx.message.attachments else "") + ") VALUES (" + str(ctx.author.id) + ", '" + trigger.replace('\'', '\'\'') + "'" + (", '" + response.replace('\'', '\'\'') + "'" if response else "") + (", '" + " | ".join([attachment.url for attachment in ctx.message.attachments]).replace('\'', '\'\'') + "'" if ctx.message.attachments else "") + ")")
			except Exception:
				return await ctx.send(content = error_string + ' **You already have a quote with that trigger.**')

		await ctx.send(content = success_string + ' **Quote added.**')

	@commands.command(aliases = ['qr'])
	async def qradd(self, ctx, trigger, *, response = None):
		if not response and not ctx.message.attachments:
			return await ctx.send(content = error_string + ' **QR code must not be empty.**')

		qr_url = 'https://chart.googleapis.com/chart?' + urllib.parse.urlencode({'cht': 'qr', 'chs': '200x200', 'chld': 'L|1', 'chl': response})
		try:
			DBService.exec("INSERT INTO PersonalQuotes (User, Trigger, Attachments) VALUES (" + str(ctx.author.id) + ", '" + trigger.replace('\'', '\'\'') + "', '" + qr_url.replace('\'', '\'\'') + "')")
		except Exception:
			return await ctx.send(content = error_string + ' **You already have a quote with that trigger.**')

		await ctx.send(content = success_string + ' **Quote added.**')

	@commands.command(aliases = ['premove', 'prem'])
	async def personalremove(self, ctx, *, trigger):
		user_quote = DBService.exec("SELECT * FROM PersonalQuotes WHERE User = " + str(ctx.author.id) + " AND Trigger = '" + trigger.replace('\'', '\'\'') + "'").fetchone()
		if user_quote:
			DBService.exec("DELETE FROM PersonalQuotes WHERE User = " + str(ctx.author.id) + " AND Trigger = '" + trigger.replace('\'', '\'\'') + "'")
			await ctx.send(content = success_string + ' **Quote deleted.**')
		else:
			await ctx.send(content = error_string + ' **Quote with that trigger does not exist.**')

	@commands.command(aliases = ['p'])
	async def personal(self, ctx, *, trigger):
		user_quote = DBService.exec("SELECT * FROM PersonalQuotes WHERE User = " + str(ctx.author.id) + " AND Trigger = '" + trigger.replace('\'', '\'\'') + "'").fetchone()
		if not user_quote:
			await ctx.send(content = error_string + ' **Quote with that trigger does not exist.**')
		else:
			if ctx.guild and server_config[ctx.guild.id]['del_commands'] and ctx.guild.me.permissions_in(ctx.channel).manage_messages:
				await ctx.message.delete()

			await ctx.send(embed = personal_embed(user_quote, ctx.author))

	@commands.command(aliases = ['plist'])
	async def personallist(self, ctx, page_number: int = 1):
		user_quotes = DBService.exec("SELECT * FROM PersonalQuotes WHERE User = " + str(ctx.author.id) + " LIMIT 10 OFFSET " + str(10 * (page_number - 1))).fetchall()
		if len(user_quotes) == 0:
			await ctx.send(content = error_string + ' **No personal quotes on page `' + str(page_number) + '`**')
		else:
			await ctx.send(embed = list_embed(user_quotes, ctx.author, page_number))

	@commands.command(aliases = ['pclear'])
	async def personalclear(self, ctx):
		DBService.exec("DELETE FROM PersonalQuotes WHERE User = " + str(ctx.author.id))
		await ctx.send(content = success_string + ' **Cleared all your personal quotes.**')


def setup(bot):
	bot.add_cog(PersonalQuotes(bot))
