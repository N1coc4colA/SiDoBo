import os
from dotenv import load_dotenv


def build_guild(varn: str, default: str) -> dict:
    val: str = os.environ.get(varn, "")
    l: list = val.split(";")
    out: dict = {}

    for elem in l:
        sl: list = elem.split("|")
        if len(sl) != 2:
            continue

        out[sl[0]] = sl[1]

    return out


token = ""
test_token = ""
guilds = {}
test_guilds = {}
admins = []


def load():
    global token, test_token, guilds, test_guilds, admins

    load_dotenv()

    token = os.environ.get("DISCORD_AKEY", "")
    test_token = os.environ.get("DISCORD_TAKEY", "")

    guilds = build_guild("DISCORD_GUILDS", "")
    test_guilds = build_guild("DISCORD_TGUILDS", "")

    admins = os.environ.get("DISCORD_IDS", "").split(";")

    print(f"Token: {token}")
    print(f"Test token: {test_token}")
    print(f"Guilds: {guilds}")
    print(f"TGuilds: {test_guilds}")
    print(f"Admins: {admins}")

