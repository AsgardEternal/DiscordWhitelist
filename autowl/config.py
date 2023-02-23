from dataclasses import dataclass


@dataclass
class DiscordClientConfig:
    login_token: str


@dataclass
class WhitelistMember:
    discord_username: str
    steam64: int


@dataclass
class WhitelistGroup:
    discord_role_id: int
    members: dict[int, WhitelistMember]


@dataclass
class Whitelist:
    whitelist: dict[str, WhitelistGroup]

    def __iter__(self):
        for key in self.whitelist:
            yield self.whitelist[key]
