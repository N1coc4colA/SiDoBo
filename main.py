#!/bin/python3
import src.setup as setup
import src.settings as settings
import src.client as client

import discord

setup.load()
settings.load()

# --- Wrapper initialisation ---
client0 = client.Clean(intents=discord.Intents.default())
 
