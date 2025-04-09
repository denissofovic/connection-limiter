import discord
from helpers.supabase_helper import increment_connects,fetch_connects,create_row
from helpers.messages import create_pretty_message

MAX_NUM_OF_CONNECTS = 6
async def handle_voice_update(client, member, before, after):
    if before.channel == after.channel:
        return  

    num_of_connects = await fetch_connects(member.id) or 0 
    if num_of_connects == 0:
        await create_row(member.id) 

    if before.channel is None and after.channel is not None:  
        print(f"{member.name} connected.")
        await increment_connects(member.id, num_of_connects)

    elif before.channel is not None and after.channel is None:  
        print(f"{member.name} disconnected.")

        if num_of_connects >= MAX_NUM_OF_CONNECTS:
            message = create_pretty_message("Notification", "You've reached your limit for today, please try connecting again tomorrow", discord.Color.red())
            await member.send(embed = message)

            limited_role = discord.utils.get(member.guild.roles, name="LIMITED")
            if limited_role:
                await member.add_roles(limited_role, reason="User reached connection limit")
                print(f"Added 'LIMITED' role to {member.name}")

        else:
            if num_of_connects == 1:
                message = create_pretty_message("Notification", "You've connected 1 time today")
            else:
                message = create_pretty_message("Notification", f"You've connected {num_of_connects} times today")
            await member.send(embed = message)
