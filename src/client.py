import discord
import src.settings as settings
import src.infos as infos

class Clean(discord.Client):
    def __init__(self, *args, **kwargs):
        # Call discord.py Client constructor
        super().__init__(*args, **kwargs)

        self.ginfos = {}
        self.run(settings.token)

    # Events & Commands
    async def on_ready(self):
        await self.instanciate_guilds()
        print("Bot ready.")

    async def instanciate_guilds(self):
        for guild in self.guilds:
            if guild.id in settings.guilds:
                self.ginfos[guild.id] = infos.GuildInfos(guild.id, settings.guilds[guild.id])

    async def on_message(self, message):
        print("Received message: " + str(message.content))
    
        if message.author.bot or message.content == "":
            return

        options = {
            "!logs": self.logs,
            "!help": self.help,
            "!help.settings": self.settings_help,
            "!see": self.see,
            "!available": self.available,
            "!delete": self.delete,
            "!test" : self.test,
        }
        complex_options = {
            "!week ": self.week,
            "!add ": self.add,
            "!rm ": self.rm,
            "!schedule ": self.schedule, 
            "!settings.add ": self.settings_add,
            "!settings.rm ": self.settings_rm,
        }
        
        if message.content in options.keys():
            await options[message.content](message)
            return

        for elem in complex_options:
            if message.content.startswith(elem[0]):
                await complex_options[elem[0]](message)
                return

    async def delete_message(self, message):
        try:
            guild, gi = message.guild, self.ginfos[message.guild.id]
            channel = await guild.fetch_channel(gi.cid)
            msg = await channel.fetch_message(message.content.split(" ")[1])
            await msg.delete()
            await message.delete()
        except discord.NotFound or discord.Forbidden or discord.HTTPException or ValueError:
            print("Error while deleting message")

    """
    Followings are hooks used to check rights before executing the real stuff.
    """

    async def test(self, msg):
        print("Required test.")

    async def help(self, msg):
        pass

    async def settings_help(self, msg):
        if msg.author.id in settings.admins:
            await self.show_settings_help(msg)

    async def logs(self, msg):
        if msg.author.id in settings.admins:
            await self.show_logs(msg)

    async def see(self, msg):
        pass

    async def available(self, msg):
        pass

    async def delete(self, msg):
        if msg.author.id in settings.admins:
            await self.delete_message(msg)

    async def week(self, msg):
        pass

    async def add(self, msg):
        pass

    async def rm(self, msg):
        pass

    async def schedule(self, msg):
        pass

    async def settings_add(self, msg):
        pass

    async def settings_rm(self, msg):
        pass


class Client(discord.Client):
    def __init__(self, _token: str, _guilds: dict, params: dict, *args, **kwargs):
        # Call discord.py Client constructor
        super().__init__(*args, **kwargs)

        self._guilds = _guilds  # Used to instanciate guilds in instanciate_guilds()
        self.croissant_guilds = {}  # Key: guild_id, Value: Guilds instance

        self.params = params

        self.run(_token)

    # Instanciate CroissantGuild for every guild
    async def instanciate_guilds(self):
        for guild in self.guilds:
            if guild.id in self._guilds:
                # Instanciate croissant guild object
                self.croissant_guilds[guild.id] = CroissantGuild(self, guild.id, self._guilds[guild.id],
                                                                 self.params["pick_delay"])

    # Events & Commands
    async def on_ready(self):
        await self.instanciate_guilds()
        print("Bot ready")

    async def on_message(self, message):
        if message.author.bot:
            return
        if message.author.id in self.params["admin_ids"]:
            if message.content == "!delete":
                await self.delete(message)
        if message.guild.id in self.croissant_guilds:
            await self.croissant_guilds[message.guild.id].on_message(message)

    async def delete(self, message):
        try:
            guild, guild_instance = message.guild, self.croissant_guilds[message.guild.id]
            channel = await guild.fetch_channel(guild_instance.channel_id)
            msg = await channel.fetch_message(message.content.split(" ")[1])
            await msg.delete()
            await message.delete()
        except discord.NotFound or discord.Forbidden or discord.HTTPException or ValueError:
            print("Error while deleting message")


