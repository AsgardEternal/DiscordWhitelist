import discord
import random
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
        if self.client.whitelistGrps.get(role.name):
            await interaction.response.send_message(
                f"**{role.name}** is already added, cannot add it again!"
            )
            return

        log.info(f"Adding {role.name} ({role.id}) as a Whitelist role")
        await interaction.response.send_message(
            f"Adding **{role.name}** as a Whitelist role"
        )
        self.client.whitelistGrps[role.id] = config.WhitelistGroup(
            name=role.name, roleID=role.id, permissions='reserve'
        )

    @app_commands.command()
    async def addperm(
            self,
            interaction: discord.Interaction,
            role: discord.Role,
            perms: str
    ):
        if self.client.whitelistGrps.get(role.name):
            await interaction.response.send_message(
                f"**{role.name}** is already added, cannot add it again!"
            )
            return

        log.info(f"Adding {role.name} ({role.id}) as a Whitelist role")
        await interaction.response.send_message(
            f"Adding **{role.name}** as a Whitelist role"
        )
        self.client.whitelistGrps[role.id] = config.WhitelistGroup(
            name=role.name, roleID=role.id, permissions=perms
        )

    @app_commands.command()
    async def remove(
        self,
        interaction: discord.Interaction,
        role: discord.Role,
    ):
        if not self.client.whitelistGrps.get(role.id):
            await interaction.response.send_message(
                f"**{role.name}** has not been added as a whitelisted group, unable to remove!"
            )
            return

        log.info(f"Removing {role.name} ({role.id}) from Whitelisted role")
        await interaction.response.send_message(
            f"Removed **{role.name}** from Whitelisted roles"
        )
        self.client.whitelistGrps[role.id].delGroup()
        self.client.whitelistGrps.pop(role.id)

    @app_commands.command()
    async def list_whitelisted_roles(self, interaction: discord.Interaction):
        whitelisted_roles = []
        if not interaction.guild:
            await interaction.response.send_message(
                "This command must be ran within a discord server"
            )
            return

        for group in self.client.whitelistGrps:
            role_id = self.client.whitelistGrps[group].discord_role_id
            if not interaction.guild.get_role(role_id):
                continue
            whitelisted_roles.append(f"<@&{role_id}>")

        embed_description = (
            "\n".join(whitelisted_roles)
            if whitelisted_roles
            else "No whitelisted roles found, you can some using `/add`"
        )

        embed = discord.Embed(
            title="Whitelisted Roles",
            description=embed_description,
            color=random.randint(0, 0xFFFFFF),
        ).set_footer(text="Users with these roles will be whitelisted on Squad")

        await interaction.response.send_message(embed=embed)
