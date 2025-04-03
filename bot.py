import discord
import os
import asyncio
from dotenv import load_dotenv
from event_handlers import on_ready,on_voice_state
from tasks.remove_roles import remove_limited_role

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True

class MyBot(discord.Client):
    async def setup_hook(self):
        self.loop.create_task(remove_limited_role(self))  

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

client = MyBot(intents=intents)

client.event(on_ready.handle_ready)
client.event(on_voice_state.handle_voice_update)

client.run(TOKEN)
