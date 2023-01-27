import os
from sys import stderr
import discord


# run init stuff inside this function
def init():
    # make sure this prints the discord token
    # set this up as a runtime environment variable, DO NOT HARDCODE THE TOKEN
    distoken = os.environ.get("DISCORD_TOKEN")
    if not distoken:
        print("Unable to find discord token in environment!", file=stderr)
        exit(1)

    print(f"discord token:{distoken}")


init()
