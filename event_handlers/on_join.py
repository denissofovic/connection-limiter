import discord

async def handle_join(client, guild):
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

