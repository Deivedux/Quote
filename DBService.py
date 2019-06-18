# Database Service

import sqlite3
import asyncio

conn = sqlite3.connect('configs/QuoteBot.db')
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS ServerConfig (Guild INTEGER unique, Prefix TEXT, DelCommands TEXT, OnReaction TEXT, PinChannel INTEGER)")
c.execute("CREATE TABLE IF NOT EXISTS Blacklist (Id INTEGER unique, Reason TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS PersonalQuotes (User INTEGER, Trigger TEXT, Response TEXT, Attachments TEXT, PRIMARY KEY (User, Trigger))")
c.execute("CREATE TABLE IF NOT EXISTS Donators (UserId INTEGER unique, UserTag TEXT)")
c.execute("DROP TABLE IF EXISTS RandomQuotes")

try:
	c.execute("ALTER TABLE ServerConfig ADD COLUMN WebhookURL TEXT")
except sqlite3.OperationalError:
	pass

class DBService:

	def exec(sql):
		try:
			return c.execute(sql)
		except sqlite3.IntegrityError:
			raise Exception

	def commit():
		return conn.commit()

	async def while_commit():
		while True:
			await asyncio.sleep(60)
			conn.commit()

async def main():
	asyncio.ensure_future(DBService.while_commit())

if __name__ == 'DBService':
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main())
