import discord
from discord.ext import commands
import json
from llamaapi import LlamaAPI

# Replace "<your_discord_bot_token>" and "<your_llama_api_token>" with your actual tokens
DISCORD_BOT_TOKEN = ""
LLAMA_API_TOKEN = ""

# Set the desired channel ID where the bot should respond
TARGET_CHANNEL_ID = 919197436717723698  # Replace with your actual channel ID

# Initialize the SDK
llama = LlamaAPI(LLAMA_API_TOKEN)

# Create an instance of discord.Intents
intents = discord.Intents.default()
intents.message_content = True  # Allows access to message content

# Discord Bot Setup with intents
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command(name='ask')
async def ask_ai(ctx, *, question):
    # Build the API request for asking any question
    api_request_json = {
        "messages": [
            {"role": "user", "content": question}
        ],
        "stream": False,
    }

    # Execute the Request
    response = llama.run(api_request_json)

    # Extract the "content" field from the assistant's message
    content = response.json().get("choices", [{}])[0].get("message", {}).get("content", "No answer provided.")

    # Send the simplified answer to the specified Discord channel
    target_channel = bot.get_channel(TARGET_CHANNEL_ID)
    await target_channel.send(f"Question: {question}\nAnswer: {content}")

# Run the Discord bot
bot.run(DISCORD_BOT_TOKEN)
