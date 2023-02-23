import logging
import discord
from discord.ext import commands
from autowl import config

log = logging.getLogger(__name__)


class Bot(commands.Bot):
    whitelist = config.Whitelist({}).whitelist

    def __init__(self, config: config.DiscordClientConfig):
        self.config = config
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(
            command_prefix=commands.when_mentioned_or("&"),
            intents=intents,
            help_command=commands.DefaultHelpCommand(dm_help=True),
        )

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
