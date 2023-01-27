import os
import discord


# run init stuff inside this function
def init():
    # make sure this prints the discord token
    # set this up as a runtime environment variable, DO NOT HARDCODE THE TOKEN
    try:
        disToken = os.environ[
            'DISCORD_TOKEN']  # grabs the discord token from the environment variable, if not there, exit
    except:
        print("ERROR: unable to find discord token in environment variables!")
        exit(1)

    print("discord Token:"+disToken)


init()
