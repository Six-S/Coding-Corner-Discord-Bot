# Coding-Corner-Discord-Bot
A quick little Discord bot written in Python.

This is a small project that makes use of [Rapptz's Discord API Wrapper](https://github.com/Rapptz/discord.py) to add some cool functionality to my Discord Server.

The current iteration of this bot (v0.5) features a community driven reputation system. Users can allocate points to one another for good deeds, helpful advice, etc.
Additionally, users can use this bot to gain access to a daily coding challenge to complete.

### Notes:

Usage: $[Command]

Command List:
- $ping - Make sure CodeBot is around
- $list - Show this list
- $challenge - Show the coding challenge of the day
- $register - Register yourself with CodeBot
- $addrep [user] - Give another user a reputation point
- $removerep [user] - Remove a reputation point from a user
- $showrep [user] - Show the reputation of a user
- $codebotdev - Learn more about CodeBots development
- $bug - Report a bug found in CodeBot.

More to come!
There are plenty of things I want to implement in this project.
Feel free to take this and use it if you want.

Feel like this bot is missing a feature? [Submit a feature request!](https://github.com/Six-S/Coding-Corner-Discord-Bot/issues) Just make sure you label is properly!

### Setup:
CodeBot was written to run in a Linux environment, but with some small changes could be altered to run elsewhere.

#### Without Docker
If you don't want to use Docker, then setup is as simple as:
`python3 -m pip install -U discord.py`
then
`python3 main.py`

Having trouble? Your answer is probably [here](https://discordpy.readthedocs.io/en/latest/intro.html#installing), courtesy of Rapptz.

What you do with the emailWorker.py script it up to you - though, it would be easiest to just add it as a cron job.

#### With Docker
From inside the Coding-Corner-Discord-Bot directory, run:
`sudo docker build -t code-bot  .`

`sudo docker run --rm --name code-bot code-bot`

When running the container, you do not have to name it, and it does not need the --rm flag.
The name is for ease of use, and the --rm is much more useful for debugging it. Once it works how you'd like, it may be of more benifit to remove the `--rm` flag.
