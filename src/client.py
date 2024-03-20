import discord
from discord.ext import commands

import src.settings as settings
from src.logs import log
import src.logs as logs
import src.db as db
import src.shared as shared

from src.controller.reservation import ReservationController
from src.controller.planner import PlannerController
from src.controller.planning import PlanningController
from src.controller.settings import SettingsController


class Clean(commands.Bot):
    def __init__(self, *args, **kwargs):
        self.must_stop = False

        # Call discord.py Client constructor
        super().__init__(command_prefix="/", *args, **kwargs)

        self._controllers: list = []

        self.init_commands()

        shared.set_client(self)

        self.run(settings.token)

    # Events & Commands
    async def on_ready(self) -> None:
        await self.instantiate_guilds()
        await self.tree.sync()
        log("Bot started.")

    async def instantiate_guilds(self) -> None:
        for guild in self.guilds:
            built = (str(guild.id), str(guild.name),)
            settings.guilds.append(built)

    @staticmethod
    def _empty_filled(data: dict, keys: list, values: list) -> dict:
        pos = 0
        for k in keys:
            if k not in data:
                data[keys[pos]] = values[pos]
            pos += 1

        return data

    def _generate_command(self, data: dict) -> None:
        keys = ["checker", "positional", "no_extras", "cooldown", "brief", "usage", "desc", "help", "parent"]
        values = [None, False, True, None, "", "", "", "", self]

        data = self._empty_filled(data, keys, values)

        log("Adding command " + data["name"])

        self.command(
            name=data["name"],
            description=data["desc"],
            usage=data["usage"],
            require_var_positional=data["positional"],
            ignore_extra=data["no_extras"],
            cooldown=data["cooldown"],
            checker=data["checker"],
        )(data["cb"])

    def init_commands(self) -> None:
        commands = [
        {
        "name": "soutien.test",
        "cb": self.test,
        "positional": False,
        "no_extras": True,
        },
        {
        "name": "soutien",
        "cb": self.available,
        "positional": False,
        "no_extras": True,
        },
        {
        "name": "soutien.help",
        "cb": self.help,
        "positional": False,
        "no_extras": True,
        },
        {
        "name": "soutien.query",
        "cb": self.query,
        "positional": False,
        "no_extras": True,
        },
        {
        "name": "soutien.planning",
        "cb": self.planning,
        "positional": False,
        "no_extras": True,
        },
        {
        "name": "soutien.settings",
        "cb": self.settings,
        "positional": False,
        "no_extras": True,
        },
        {
        "name": "soutien.logs",
        "cb": self.logs,
        "positional": False,
        "no_extras": True,
        },
        {
        "name": "soutien.down",
        "cb": self.down,
        "positional": False,
        "no_extras": True,
        },
        {
        "name": "soutien.planner",
        "cb": self.planner,
        "positional": False,
        "no_extras": True,
        },
        ]

        for com in commands:
            self._generate_command(com)

    """
    Followings are hooks used to check rights before executing the real stuff.
    """

    async def test(*args, **kwargs) -> None:
        if str(args[1].author.id) in settings.get_bans():
            return

        """print("KWARGS:")
        for key, value in kwargs.items():
            print("%s => %s" % (key, type(value).__name__))

        print("ARGS:")
        for arg in args:
            print(type(arg).__name__)"""

        log(f"{args[1].author.id} required a test.")

    async def help(*args, **kwargs) -> None:
        if str(args[1].author.id) in settings.get_bans():
            return

        options = [
            "Les commandes suivantes doivent commencer par '/'. Tous les créneaux sont de 15 minutes.",
            "> soutien - Réserver un créneau ou annuler sa réservation.",
            "> soutien.query - Voir ce qu'on a réservé.",
            "> soutien.planner - Ajouter des créneaux à ceux disponibles ou en supprimer.",
            "> soutien.planning - Voir les créneaux réservés.",
            "> soutien.settings - Paramètres du bot.",
            "> soutien.test - Génère un message de test côté server.",
            "> soutien.logs - Affiche les logs du serveur.",
            "> soutien.down - Arrête le serveur.",
            "> soutien.help - Affiche cet aide.",
        ]

        await args[1].channel.send(content="\n\n".join(options))

    async def settings(*args, **kwargs) -> None:
        self = args[0]

        if str(args[1].author.id) in settings.get_admins():
            ctrl = SettingsController(args[1])
            ctrl.deleter = self.control_deleter
            self._controllers.append(ctrl)
            await ctrl.initialize()

    async def logs(*args, **kwargs) -> None:
        # Max message size is 2000.
        if str(args[1].author.id) not in settings.get_admins():
            return

        lst = logs.get_logs()
        if len(lst) == 0:
            await args[1].channel.send(content="Aucun log disponible.")
        else:
            for val in lst:
                await args[1].channel.send(content=val)

    async def planner(*args, **kwargs) -> None:
        self = args[0]

        if str(args[1].author.id) in settings.get_admins():
            ctrl = PlannerController(args[1])
            ctrl.deleter = self.control_deleter
            self._controllers.append(ctrl)
            await ctrl.initialize()

    async def planning(*args, **kwargs) -> None:
        self = args[0]

        if str(args[1].author.id) in settings.get_admins():
            ctrl = PlanningController(args[1])
            ctrl.deleter = self.control_deleter
            self._controllers.append(ctrl)
            await ctrl.initialize()

    async def query(*args, **kwargs) -> None:
        if str(args[1].author.id) in settings.get_bans():
            return

        lst = db.query(args[1].author.id)
        if len(lst) == 0:
            await args[1].channel.send(content="Vous n'avez rien réservé.")
        else:
            for val in lst:
                await args[1].channel.send(content=f"> {val[0]}\n\n{val[1]}")

    async def available(*args, **kwargs) -> None:
        self = args[0]

        if str(args[1].author.id) not in settings.get_bans():
            ctrl = ReservationController(args[1])
            ctrl.deleter = self.control_deleter
            self._controllers.append(ctrl)
            await ctrl.initialize()

    async def down(*args, **kwargs) -> None:
        self = args[0]

        if self.must_stop:
            return

        self.must_stop = True

        for ctrl in self._controllers:
            await ctrl.end()

        self._controllers = []

        await self.close()

    def control_deleter(self, ctrl) -> None:
        if ctrl in self._controllers:
            self._controllers.remove(ctrl)

    async def dm_reserved(self, date, time):
        lst = db.get_data(date, time)
        people = user = await self.fetch_user(lst[1])

        for admin in settings.get_admins():
            user = await self.fetch_user(admin)
            await user.send(f"> {people.mention} ({lst[3]}A) a réservé pour le {date} à {time}\n{lst[2]}")

    async def dm_cancelled(self, date, time, lst):
        people = user = await self.fetch_user(lst[1])
        for admin in settings.get_admins():
            user = await self.fetch_user(admin)
            await user.send(f"> {people.mention} ({lst[3]}A) a annulé la séance pour le {date} à {time}")

    async def dm_reservation_cancelled(self, date, time, uid, reason):
        user = await self.fetch_user(uid)
        await user.send(f">Votre réservation de scéance du {date} à {time} a été annulée.\n{reason}")

