import discord
import json
import asyncio
import aiohttp
from discord.ext import commands

with open('configs/config.json') as json_data:
	response_json = json.load(json_data)
	webhook_url = response_json['botlog_webhook_url']
	del response_json

class BotLog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_guild_join(self, guild):
		bots = [member for member in guild.members if member.bot]
		async with aiohttp.ClientSession() as session:
			webhook = discord.Webhook.from_url(webhook_url, adapter = discord.AsyncWebhookAdapter(session))
			await webhook.send(content = ':inbox_tray: **Guild Added** `' + guild.name.strip('`') + '` (`' + str(guild.id) + '`)\n  Total: **' + str(guild.member_count) + '** | Users: **' + str(guild.member_count - len(bots)) + '** | Bots: **' + str(len(bots)) + '**')

	@commands.Cog.listener()
	async def on_guild_remove(self, guild):
		bots = [member for member in guild.members if member.bot]
		async with aiohttp.ClientSession() as session:
			webhook = discord.Webhook.from_url(webhook_url, adapter = discord.AsyncWebhookAdapter(session))
			await webhook.send(content = ':outbox_tray: **Guild Removed** `' + guild.name.strip('`') + '` (`' + str(guild.id) + '`)\n  Total: **' + str(guild.member_count) + '** | Users: **' + str(guild.member_count - len(bots)) + '** | Bots: **' + str(len(bots)) + '**')


def setup(bot):
	bot.add_cog(BotLog(bot))
