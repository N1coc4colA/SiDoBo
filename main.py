#!/bin/python3

import discord
import asyncio
import schedule
from time import sleep

import src.setup as setup
import src.settings as settings
import src.client as client
import src.logs as logs
import src.db as db
import src.shared as shared


setup.load()
settings.load()
logs.load()


# --- Setup cleanup job ---

schedule.every().day.at("01:00").do(db.cleanup)


# --- Wrapper initialisation ---

intents = discord.Intents.default()
#intents.members = True
intents.message_content = True


# --- Run it ---

while not shared.get_client() or not shared.get_client().must_stop:
    try:
        client.Clean(intents=intents)
        while not shared.get_client().must_stop:
            sleep(0.1)

    except KeyboardInterrupt:
        print("Received stop request.")
        asyncio.run(shared.get_client().down())

    except Exception as e:
        logs.log(str(e))

    sleep(0.1)

