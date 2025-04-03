import asyncio
from datetime import datetime, timedelta, timezone
import discord


async def remove_limited_role(client):
    
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
            limited_role = discord.utils.get(guild.roles, name="LIMITED")
            if limited_role:
                members_with_role = [m for m in guild.members if limited_role in m.roles]  
                for member in members_with_role:
                    await member.remove_roles(limited_role, reason="Daily reset at midnight UTC")

                print(f"Removed 'LIMITED' role from {len(members_with_role)} members in {guild.name}.")
