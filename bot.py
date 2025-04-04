import discord
import os
import asyncio
from dotenv import load_dotenv
from event_handlers.on_ready import handle_ready
from event_handlers.on_voice_state import handle_voice_update
from event_handlers.on_join import handle_join
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

@client.event
async def on_ready():
    await handle_ready(client)

@client.event
async def on_voice_state_update(member, before, after):
    await handle_voice_update(client, member, before, after)

@client.event
async def on_guild_join(guild):
    await handle_join(client,guild)

client.run(TOKEN)
