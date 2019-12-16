import discord
import json
#Maybe we'll use YAML instead.
# try:
#     from yaml import CLoader as Loader, CDumper as Dumper
# except ImportError:
#     from yaml import Loader, Dumper


class Bot():
    def __init__(self):
        print('[INFO] Spinning up Bot core functionality...')
        self.updateLocalSettings()

        #these values won't change, so we can assign variables to them.
        self.token = self.settings['config']['token']
    
    def updateLocalSettings(self):
        with open('settings.json') as settings:
            self.settings = json.load(settings)
    
    def register(self, requester):
        #define a list of our current users
        users = self.settings['users']
        
        #Let's make sure the user doesn't already exist.
        #NOTE: This brute force approach is fine for now, but
        #is super awful for bigger userbases. FIXME ASAP...
        for user in users:
            if requester == users[user]['user']:
                print('[WARN] Cannot register user "{0}" as they are already registered.'.format(requester))
                return False
            #since we're already looping all of our users, lets get the last one
            #so that we can create our new user.
            newUserKey = int(user)
        
        #since we don't currently have this user, let's build their profile!
        #NOTE: The way we get our new user key is shit. FIXME.
        newUser = {
            str(newUserKey + 1): {
                "user": requester,
                "raiting": 0,
                "callMe": ""
            }
        }
        users.update(newUser)

        #Two "with" statements feels cleaner than seeking and writing
        #Load our current settings in, and update with our new information.
        #TODO: WE CAN PUT THIS INTO A FUNCTION!!!
        with open('settings.json', 'r') as settings:
            current_settings = json.load(settings)
            current_settings['users'] = users

        #Write the new users to our settings.
        with open('settings.json', 'w') as settings:
            settings.write(json.dumps(current_settings))
        
        #set our updated settings to our class level settings variable and return.
        self.updateLocalSettings()
        return True
    
    def addReputation(self, userToAdd):

        #define a list of our current users
        users = self.settings['users']
        foundUser = {}
        
        #Let's make sure the user doesn't already exist.
        #NOTE: This brute force approach is fine for now, but
        #is super awful for bigger userbases. FIXME ASAP...
        for user in users:
            if userToAdd == users[user]['user']:
                foundUser = users[user]
                foundUserkey = user

        
        if foundUser:
            updated_value = {'rating': users[foundUserkey]['rating'] + 1}
            users[foundUserkey].update(updated_value)

            #Two "with" statements feels cleaner than seeking and writing
            #Load our current settings in, and update with our new information.
            with open('settings.json', 'r') as settings:
                current_settings = json.load(settings)
                current_settings['users'] = users

            #Write the new users to our settings.
            with open('settings.json', 'w') as settings:
                settings.write(json.dumps(current_settings))
            
            #set our updated settings to our class level settings variable and return.
            self.updateLocalSettings()
            return True
        else:
            print('[WARN] Cannot modify user "{0}" as they are not yet registered.'.format(userToAdd))
            return False
    
    def fetchReputation(self, userToFetch):

        users = self.settings['users']

        #Let's make sure the user doesn't already exist.
        #NOTE: This brute force approach is fine for now, but
        #is super awful for bigger userbases. FIXME ASAP...
        for user in users:
            if userToFetch == users[user]['user']:
                foundUserkey = user

        return self.settings['users'][foundUserkey]['rating']
        
    #Utility function to test for empty variables
    def empty(self, value):
        try:
            value = float(value)
        except ValueError:
            pass
        return bool(value)



        
if __name__ in '__main__':

    client = discord.Client()
    bot = Bot()

    @client.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(client))

    @client.event
    async def on_message(message):
        print ('Message: ', message)
        if message.author == client.user:
            return

        if message.content.startswith('$ping'):
            await message.channel.send('Hello, this is CodeBot; Version 0.1!')
        elif message.content.startswith('$list'):
            await message.channel.send('''
                    Usage: $[Command]
                Command List:
                    $ping - Make sure CodeBot is around
                    $list - Show this list
                    $register - Register yourself with CodeBot
                    $addrep [user] - Give another user a reputation point
                    $showrep [user] - Show the reputation of a user
            ''')
        elif message.content.startswith('$register'):
            print(message.author.name)
            successful = bot.register(message.author.name)
            if successful:
                await message.channel.send("You've been successfully registered, @{0}".format(message.author.name))
            else:
                await message.channel.send('Something went wrong registering you, @{0}... are you already registered?'.format(message.author.name))
        elif message.content.startswith('$addrep'):
            missingUser = False

            try:
                user = message.content.split(' ')[1]
            except IndexError:
                missingUser = True

            if not missingUser:
                successful = bot.addReputation(user)
                if successful:
                    await message.channel.send("You've added a reputation point to @{0}s profile!".format(user))
                else:
                    await message.channel.send('Something went wrong giving a reputation point to @{0}. Are they registered?'.format(user))
            else:
                    await message.channel.send("Make sure you include the user you'd like to give a reputation point to, @{0}.".format(message.author.name))

        elif message.content.startswith('$showrep'):
            try:
                user = message.content.split(' ')[1]
            except IndexError:
                user = message.author.name
            
            print(user)

            await message.channel.send("@{0} currently has {1} points!".format(user, bot.fetchReputation(user)))


            


    client.run(bot.token)
