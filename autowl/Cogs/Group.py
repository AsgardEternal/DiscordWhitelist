import os.path

import discord
import random
import logging

import mysql.connector

from autowl import config
from autowl.bot import Bot
from discord.ext import commands
from discord import app_commands

log = logging.getLogger(__name__)


class Group(commands.Cog, name="group"):
    def __init__(self, client: Bot):
        self.client = client

    async def updateRole(self, role:discord.Role):
        self.client.squadjs.connect()
        membsup = []
        for memb in role.members:
            membsup.append(memb.id)
        if len(membsup) > 0:
            memupcur = self.client.squadjs.cursor(buffered=True)
            in_params = ','.join(['%s'] * len(membsup))
            sqlstate = "SELECT * FROM DBLog_SteamUsers WHERE discordID IN (%s)" % in_params
            log.info(sqlstate)
            memupcur.execute(sqlstate, membsup)

            udata = memupcur.fetchall()
            for data in udata:
                self.client.whitelistGrps[role.id].addMember(config.WhitelistMember(data[2], data[1], data[0]))

        self.client.squadjs.commit()
        self.client.squadjs.close()


    async def baseperm(self, interaction: discord.Interaction, role: discord.Role, perms: str):

        await interaction.response.send_message("Whitelist group successfully added/updated")
        if role.id in self.client.whitelistGrps.keys():
            if perms is not None:
                self.client.whitelistGrps[role.id].squadPerms = perms
            self.client.whitelistGrps[role.id].updateGroup()
        else:
            log.info(f"Adding {role.name} ({role.id}) as a Whitelist role")
            self.client.whitelistGrps[role.id] = config.WhitelistGroup(
                name=role.name, roleID=role.id, permissions=perms
            )

        await self.updateRole(role)

    @app_commands.command()
    async def update(
            self,
            interaction: discord.Interaction,
            role: discord.Role
    ):
        if role.id in self.client.whitelistGrps.keys():
            await interaction.response.send_message("updating role!")
            await self.updateRole(role)
        else:
            await interaction.response.send_message("role not found!")

    @app_commands.command()
    async def add(
            self,
            interaction: discord.Interaction,
            role: discord.Role,
    ):
        await self.baseperm(interaction, role, "reserve")

    @app_commands.command()
    async def addperm(
            self,
            interaction: discord.Interaction,
            role: discord.Role,
            perms: str
    ):
        await self.baseperm(interaction, role, perms)

    @app_commands.command()
    async def addremote(
            self,
            interaction: discord.Interaction,
            shortname: str,
            remoteurl: str,
            perms: str = 'whitelist'
    ):
        if os.path.exists(f"wlgrps/{shortname}.cfg"):
            await interaction.response.send_message("Already exists!")
            return
        else:
            outfile = open(f"./wlgrps/{shortname}.cfg", "w")
            outfile.write(f"remotelist={remoteurl}\n")
            outfile.write(f"permissions={perms}\n")
            outfile.close()
        await interaction.response.send_message("created!")

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
