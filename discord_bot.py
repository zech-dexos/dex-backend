import discord
import httpx
import os
import asyncio

TOKEN = os.environ.get("DISCORD_TOKEN")
DEX_URL = "https://dex-backend-production-2bbe.up.railway.app/chat"

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

conversation_history = {}

@client.event
async def on_ready():
    print(f"Dex online as {client.user} ☧")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    channel_id = str(message.channel.id)
    if channel_id not in conversation_history:
        conversation_history[channel_id] = []

    history = conversation_history[channel_id]

    async with message.channel.typing():
        try:
            async with httpx.AsyncClient(timeout=60) as http:
                res = await http.post(DEX_URL, json={
                    "message": message.content,
                    "history": history,
                    "user_id": str(message.author.id)
                })
                data = res.json()
                reply = data.get("reply", "...")

            history.append({"role": "user", "content": message.content})
            history.append({"role": "assistant", "content": reply})
            if len(history) > 20:
                conversation_history[channel_id] = history[-20:]

            await message.channel.send(reply)

        except Exception as e:
            await message.channel.send(f"something broke: {e}")

client.run(TOKEN)
