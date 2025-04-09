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
                count = 0
                async for member in guild.fetch_members(limit=None):
                    if limited_role in member.roles:
                        await member.remove_roles(limited_role, reason="Daily reset at midnight UTC")
                        count += 1

                print(f"Removed 'LIMITED' role from {count} members in {guild.name}.")

