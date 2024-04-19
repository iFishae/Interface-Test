import discord
from discord.ext import commands
import os
import json
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='>', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has logged in!')

@bot.event
async def on_message(message):
    if message.author.bot:  # Skip messages from bots
        return

    # Define the path for the log file
    server_folder = os.path.join('logs', str(message.guild.name))
    channel_file = os.path.join(server_folder, f'{message.channel.name}.json')

    # Check if the folder exists, if not create it
    if not os.path.exists(server_folder):
        os.makedirs(server_folder)

    # Load existing data or initialize a new list
    if os.path.exists(channel_file):
        with open(channel_file, 'r', encoding='utf-8') as file:
            messages = json.load(file)
    else:
        messages = []

    # Append the new message
    messages.append({
        'Timestamp': str(message.created_at),
        'Author Username': message.author.name,
        'Author ID': str(message.author.id),
        'Message': message.content
    })

    # Save the updated messages list back to the JSON file
    with open(channel_file, 'w', newline='', encoding='utf-8') as file:
        json.dump(messages, file, indent=4)

    await bot.process_commands(message)  # To allow command processing if using commands

bot.run(DISCORD_TOKEN)
