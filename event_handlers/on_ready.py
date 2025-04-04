import discord

async def handle_ready(client):
    print(f"We have logged in as {client.user}")
    print("Background task created")
