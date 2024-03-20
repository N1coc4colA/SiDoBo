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
admins = []
bans = []
guilds = []


def remove_empty(lst) -> list:
    return list(filter(lambda a: a != "", lst))


def load() -> None:
    global token, bans, admins

    load_dotenv()

    token = os.environ.get("DISCORD_AKEY", "")
    admins = remove_empty(os.environ.get("ADMIN_IDS", "").split(";"))
    bans = remove_empty(os.environ.get("BANNED_IDS", "").split(";"))

    print(f"Token: {token}")
    print(f"Admins: {admins}")


def get_admins() -> list:
    global admins
    return admins


def get_guilds() -> list:
    global guilds
    return guilds


def get_bans() -> list:
    global bans
    return bans

