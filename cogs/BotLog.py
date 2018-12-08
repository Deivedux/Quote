import discord
import json
import asyncio
import aiohttp
from discord.ext import commands

with open('configs/config.json') as json_data:
	response_json = json.load(json_data)

webhook_url = response_json['botlog_webhook_url']
del response_json

outages = {}

class BotLog:
	def __init__(self, bot):
		self.bot = bot

	async def on_shard_ready(self, shard_id):
		async with aiohttp.ClientSession() as session:
			webhook = discord.Webhook.from_url(webhook_url, adapter = discord.AsyncWebhookAdapter(session))
			await webhook.send(content = ':ballot_box_with_check: **Shard #' + str(shard_id) + ' ready.**')

	async def on_ready(self):
		while True:
			high_latency = []
			for i in [(i[0], round(i[1] * 1000)) for i in self.bot.latencies]:
				if i[1] > 1000:
					outages[i[0]] = []
					high_latency.append(':name_badge: **Shard #' + str(i[0]) + ' | ' + str(i[1]) + 'ms**')
				elif i[1] > 400:
					outages[i[0]] = []
					high_latency.append(':warning: **Shard #' + str(i[0]) + ' | ' + str(i[1]) + 'ms**')
				elif i[1] in outages.keys():
					outages[i[0]].append(i[1])
					if len(outages[i[0]]) == 3:
						del outages[i[0]]
						high_latency.append('Shard #' + str(i[0]) + ' | Check: ' + str(len(outages[i[0]])) + '/3 (successfully recovered)')
					else:
						high_latency.append('Shard #' + str(i[0]) + ' | Check: ' + str(len(outages[i[0]])) + '/3')

			async with aiohttp.ClientSession() as session:
				webhook = discord.Webhook.from_url(webhook_url, adapter = discord.AsyncWebhookAdapter(session))
				await webhook.send(content = '\n'.join(high_latency))

			await asyncio.sleep(60)

	async def on_guild_join(self, guild):
		bots = [member for member in guild.members if member.bot]
		async with aiohttp.ClientSession() as session:
			webhook = discord.Webhook.from_url(webhook_url, adapter = discord.AsyncWebhookAdapter(session))
			await webhook.send(content = ':inbox_tray: **Guild Added** `' + guild.name + '` (`' + str(guild.id) + '`)\n  Total: **' + str(guild.member_count) + '** | Users: **' + str(guild.member_count - len(bots)) + '** | Bots: **' + str(len(bots)) + '**')

	async def on_guild_remove(self, guild):
		bots = [member for member in guild.members if member.bot]
		async with aiohttp.ClientSession() as session:
			webhook = discord.Webhook.from_url(webhook_url, adapter = discord.AsyncWebhookAdapter(session))
			await webhook.send(content = ':outbox_tray: **Guild Removed** `' + guild.name + '` (`' + str(guild.id) + '`)\n  Total: **' + str(guild.member_count) + '** | Users: **' + str(guild.member_count - len(bots)) + '** | Bots: **' + str(len(bots)) + '**')


def setup(bot):
	bot.add_cog(BotLog(bot))
