import os
import discord


# main runtime function
def main():
    try:
        disToken = os.environ['DISCORD_TOKEN']  # grabs the discord token from the environment variable, if not there, exit
    except:
        print("ERROR: unable to find discord token in environment variables!")
        exit(1)

    print("hello world")


main()
