#!/bin/python3
import src.setup as setup
import src.settings as settings
import src.client as client

import discord

setup.load()
settings.load()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# --- Wrapper initialisation ---
client0 = client.Clean(intents=intents)

