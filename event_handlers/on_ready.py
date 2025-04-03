import discord

async def handle_ready():
    print(f"We have logged in as {client.user}")

    for guild in client.guilds:
        limited_role = discord.utils.get(guild.roles, name="LIMITED")
        if limited_role is None:
            limited_role = await guild.create_role(
                name="LIMITED", permissions=discord.Permissions.none(), colour=discord.Colour.red()
            )
            print(f'Role "LIMITED" created in {guild.name}')
        else:
            print(f'Role "LIMITED" already exists in {guild.name}')

        for channel in guild.voice_channels:
            await channel.set_permissions(limited_role, connect=False)
            print(f"Updated permissions for {channel.name}: 'LIMITED' role cannot connect.")

    client.loop.create_task(remove_limited_role())
    print("Background task created")
