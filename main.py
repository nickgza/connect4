import os
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

async def run():
    bot = Bot()
    try:
        await bot.start(TOKEN)
    except KeyboardInterrupt:
        await bot.close()

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!')
        self.load_extension('cogs.connect4')
    
    async def on_ready(self):
        print('READY')

try:
    loop = asyncio.new_event_loop()
    loop.run_until_complete(run())
    loop.close()
except KeyboardInterrupt:
    pass
