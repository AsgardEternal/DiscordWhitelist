import os

import jsonpickle
from dataclasses import dataclass


@dataclass
class DiscordClientConfig:
    login_token: str


@dataclass
class WhitelistMember:
    discord_id: int
    discord_username: str
    steam64: int


@dataclass
class WhitelistGroup:
    name: str
    discord_role_id: int
    squadPerms: str
    members: dict[str, WhitelistMember]

    def __init__(self, name, roleID, permissions='reserve'):
        self.name = name
        self.discord_role_id = roleID
        self.squadPerms = permissions
        self.members = {}

    def delGroup(self):
        os.remove(f"./wlgrps/{self.name}.cfg")
        os.remove(f"./wlgrps/{self.name}.json")

    def updateFile(self):
        outFile = open(f"./wlgrps/{self.name}.json", "w")
        outFile.write(jsonpickle.encode(self))
        outFile.close()

    def updateWL(self):
        wlFile = open(f"./wlgrps/{self.name}.cfg", "w")
        wlFile.write(f"Group={self.name}:{self.squadPerms}\n")
        wlFile.write("\n")
        wlFile.write(f"//{self.name}\n")
        for wlmem in self.members:
            memb = self.members[wlmem]
            wlFile.write(f"Admin={memb.steam64}:{self.name} //{memb.discord_username} ({memb.discord_id})\n")
        wlFile.close()

    def addMember(self, member):
        self.members[f"{member.discord_id}"] = member
        self.updateFile()
        self.updateWL()
        pass

    def delMember(self, discordID):
        self.members.pop(f'{discordID}')
        self.updateFile()
        self.updateWL()
