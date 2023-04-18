import os.path

import jsonpickle
import logging
import discord
import mysql.connector
from discord.ext import commands
from autowl import config

log = logging.getLogger(__name__)


class Bot(commands.Bot):
    squadjs_updateDiscordID = ("UPDATE DBLog_SteamUsers SET discordID = %s "
                               "WHERE steamID = %s")

    squadjs_findByDiscordID = ("SELECT * FROM DBLog_SteamUsers "
                               "WHERE discordID = %s")

    whitelistGrps = {}

    if not os.path.exists('./wlgrps'):
        os.makedirs('./wlgrps')
    else:
        for wlfile in os.listdir('./wlgrps'):
            filename = os.fsdecode(wlfile)
            if filename.endswith('.json'):
                file = open(f'./wlgrps/{filename}', 'r')
                wlgrp: config.WhitelistGroup = jsonpickle.decode(file.read())
                whitelistGrps[wlgrp.discord_role_id] = wlgrp

    def __init__(self, config: config.DiscordClientConfig, mysqlpass):
        self.config = config
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(
            command_prefix=commands.when_mentioned_or("&"),
            intents=intents,
            help_command=commands.DefaultHelpCommand(dm_help=True),
        )
        self.squadjs = mysql.connector.connect(user='squadjs', password=mysqlpass, host='asgard.orion-technologies.io', database='squadjs', use_pure=False)

    async def on_command(self, ctx: commands.Context):
        log.info(f"{ctx.author} ({ctx.author.id}) invoked command: {ctx.command.name}, {ctx.message}")

    async def on_ready(self):
        log.info(f"Logged in as '{self.user}' ({self.user.id})")
        log.info(
            f"Have access to the following guilds: "
            f"{', '.join([str(guild.name) + ' (' + str(guild.id) + ')' for guild in self.guilds])}"
        )

        for guild in self.guilds:
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
            log.info(f"Synced guild: {guild.name}")

        await self.tree.sync()

    async def on_member_update(self, before: discord.Member, after: discord.Member):
        disusername = after.nick if after.nick is not None else after.name
        findcur = self.squadjs.cursor(buffered=True)
        findcur.execute(self.squadjs_findByDiscordID, [f"{after.id}"])
        if findcur.arraysize <= 0:
            return
        userdata = findcur.fetchone()
        log.info(f"Updating {disusername} ({after.id})")
        rmroles = []
        for befrole in before.roles:
            rmroles.append(befrole.id)
        for aftrole in after.roles:
            for befrole in before.roles:
                if befrole.id == aftrole.id:
                    rmroles.remove(aftrole.id)
        log.info(f"roles found to remove from {disusername}: {rmroles}")
        for rmroleid in rmroles:
            if not(rmroleid in self.whitelistGrps.keys()):
                continue
            self.whitelistGrps[rmroleid].delMember(before.id)

        addroles = []
        for aftrole in after.roles:
            addroles.append(aftrole.id)
        for befrole in before.roles:
            for aftrole in after.roles:
                if aftrole.id == befrole.id:
                    addroles.remove(befrole.id)
        log.info(f"roles found to add to {disusername}: {addroles}")
        for addroleid in addroles:
            if not(addroleid in self.whitelistGrps.keys()):
                continue
            self.whitelistGrps[addroleid].addMember(config.WhitelistMember(after.id, disusername, userdata[0]))
        self.squadjs.commit()

    async def setup_hook(self):
        log.info("Setting up bot")
        from autowl import Cogs

        await self.add_cog(Cogs.Whitelist(self))
        await self.add_cog(Cogs.Group(self))

    def start_bot(self):
        log.info("Starting discord bot")

        try:
            self.run(self.config.login_token, log_handler=None)
        except discord.errors.LoginFailure as e:
            log.debug(f"Received login failure: {e}")
            log.error("Failed to login to discord, check your discord token!")
            raise e
