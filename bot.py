import discord
from dotenv import load_dotenv
import os
from supabase_helper import create_row,fetch_connects,increment_connects
import asyncio
from discord.ext import commands
from datetime import datetime, timedelta, timezone

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

client = discord.Client(intents=intents)

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

    for guild in client.guilds:
        if guild is None:
            print("Guild not found.")
            return

        limited_role = discord.utils.get(guild.roles, name="LIMITED")
        if limited_role is None:
            limited_role = await guild.create_role(name="LIMITED", permissions=discord.Permissions.none(), colour=discord.Colour.red())
            print('Role "LIMITED" created.')
        else:
            print('Role "LIMITED" already exists.')
        
        for channel in guild.voice_channels:
            await channel.set_permissions(limited_role, connect=False)
            print(f"Updated permissions for {channel.name}: Users with 'LIMITED' role cannot connect.")
        
    
    client.loop.create_task(remove_limited_role())
    print('Background task created')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

@client.event
async def on_voice_state_update(member, before, after):
    MAX_NUM_OF_CONNECTS = 3 # Change later
    num_of_connects = await fetch_connects(member.id)
    if num_of_connects is None:
        await create_row(member.id)
        num_of_connects = 1

    if before.channel is None and after.channel is not None:
        print('Connect')
        incremented = await increment_connects(member.id,num_of_connects)
        
    if before.channel is not None and after.channel is None:
        print('Disconnect')
        if (num_of_connects) >= MAX_NUM_OF_CONNECTS:
            await member.send('You reached your limit, try again tomorrow')
            guild_id = member.guild.id
            guild = client.get_guild(guild_id)
            role = discord.utils.get(await guild.fetch_roles(), name="LIMITED")
            if role is not None:
                await member.add_roles(role, reason="User reached connection limit")
                print(f"Added 'LIMITED' role to {member.name}")
            return
        await member.send(f'You connected {num_of_connects} times today')




async def remove_limited_role():
    await client.wait_until_ready()  

    while not client.is_closed():
        now = datetime.now(timezone.utc)  
        midnight = datetime(now.year, now.month, now.day, 0, 0, 0, 0, tzinfo=timezone.utc)
        if now >= midnight:
            midnight += timedelta(days=1)

        time_until_midnight = (midnight - now).total_seconds()
        print(f"Waiting {time_until_midnight:.2f} seconds until midnight UTC...")
        await asyncio.sleep(time_until_midnight)  

        for guild in client.guilds:

            if guild is None:
                print("Guild not found.")
                continue

            role = discord.utils.get(guild.roles, name='LIMITED')
            if role is None:
                print(f"Role 'LIMITED' not found.")
                continue

            removed_count = 0
            for member in guild.members:
                if role in member.roles:
                    await member.remove_roles(role, reason="Daily reset at midnight UTC")
                    removed_count += 1

        print(f"Removed 'LIMITED' role from {removed_count} members.")


client.run(TOKEN)
