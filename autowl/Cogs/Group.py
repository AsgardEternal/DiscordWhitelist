import discord
import logging
from autowl import config
from autowl.bot import Bot
from discord.ext import commands
from discord import app_commands


log = logging.getLogger(__name__)


class Group(commands.Cog, name="group"):
    def __init__(self, client: Bot):
        self.client = client

    @app_commands.command()
    async def add(
        self,
        interaction: discord.Interaction,
        role: discord.Role,
    ):
        if self.client.whitelist.get(role.name):
            await interaction.response.send_message(
                f"**{role.name}** is already added, cannot add it again!"
            )
            return

        log.info(f"Adding {role.name} ({role.id}) as a Whitelist role")
        await interaction.response.send_message(
            f"Adding **{role.name}** as a Whitelist role"
        )
        self.client.whitelist[f"{role.name}"] = config.WhitelistGroup(
            discord_role_id=role.id, members={}
        )

    @app_commands.command()
    async def remove(
        self,
        interaction: discord.Interaction,
        role: discord.Role,
    ):
        if not self.client.whitelist.get(role.name):
            await interaction.response.send_message(
                f"**{role.name}** has not been added as a whitelisted group, unable to remove!"
            )
            return

        log.info(f"Removing {role.name} ({role.id}) from Whitelisted role")
        await interaction.response.send_message(
            f"Removed **{role.name}** from Whitelisted roles"
        )
        self.client.whitelist.pop(role.name)
