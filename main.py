#CodeBot v0.5
#written by: Six-S 
#https://github.com/Six-S/Coding-Corner-Discord-Bot

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
        self.all_users = []

        #these values won't change, so we can assign variables to them.
        self.token = self.settings['config']['token']
    
    def register(self, requester):
        #define a list of our current users
        users = self.settings['users']
        
        results = self.searchUsers(requester)
        if self.empty(results['key']):
            print('[WARN] Cannot register user "{0}" as they are already registered.'.format(requester))
            return {
                'message': "Something went wrong registering you, &arg1&... are you already registered?",
                'arg1': self.getMention(requester)
            }
        
        #since we don't currently have this user, let's build their profile!
        #NOTE: The way we get our new user key is shit. FIXME.
        newUser = {
            str(results['lastKey'] + 1): {
                "user": requester,
                "rating": 0,
                "callMe": ""
            }
        }
        users.update(newUser)

        self.updateUserSettings(users)

        #set our updated settings to our class level settings variable and return.
        self.updateLocalSettings()
        return {
            'message': "You've been successfully registered, &arg1&",
            'arg1': self.getMention(requester)
        }
    
    def getChallenge(self, user):
        with open('challenge.txt', 'r') as challenge:
            body = challenge.read()
            challenge_body = body.split('-')[0].replace('=', '')
            return {
                'message': challenge_body
            }

    def addReputation(self, userToAdd):

        #define a list of our current users
        users = self.settings['users']
        foundUser = {}

        foundUser = self.searchUsers(userToAdd)
        
        if self.empty(foundUser['key']):
            updated_value = {'rating': users[foundUser['key']]['rating'] + 1}
            users[foundUser['key']].update(updated_value)

            self.updateUserSettings(users)

            #set our updated settings to our class level settings variable and return.
            self.updateLocalSettings()
            return {
                'message': "You've given a reputation point to &arg1&!",
                'arg1': self.getMention(userToAdd)
            }
        else:
            print('[WARN] Cannot modify user "{0}" as they are not yet registered.'.format(userToAdd))
            return {
                'message': "Something went wrong giving a reputation point to &arg1&. Are they registered?",
                'arg1': self.getMention(userToAdd)
            }

    def removeReputation(self, userToRemove):

        #define a list of our current users
        users = self.settings['users']
        foundUser = {}

        foundUser = self.searchUsers(userToRemove)

        if self.empty(foundUser['key']):
            rating = users[foundUser['key']]['rating']
            if rating >= 0:
                updated_value = {'rating': rating - 1}
                users[foundUser['key']].update(updated_value)
            else:
                return {
                    'message': "&arg1&s reputation can't go any lower!",
                    'arg1': self.getMention(userToRemove)
                }

            self.updateUserSettings(users)
            
            #set our updated settings to our class level settings variable and return.
            self.updateLocalSettings()
            return {
                'message': "You've removed a reputation point from &arg1&!",
                'arg1': self.getMention(userToRemove)
            }
        else:
            print('[WARN] Cannot modify user "{0}" as they are not yet registered.'.format(userToRemove))
            return {
                'message': "Something went wrong removing a reputation point from &arg1&. Are they registered?",
                'arg1': self.getMention(userToRemove)
            }

    #### --------------- REPLIES WITH NO LOGIC --------------- ####
    
    def fetchReputation(self, userToFetch):
        users = self.settings['users']

        foundUserkey = self.searchUsers(userToFetch)['key']

        points = users[foundUserkey]['rating']

        return {
            'message': '&arg1& currently has &arg2& points!',
            'arg1': self.getMention(userToFetch),
            'arg2': str(points)
        }

    def pong(self, user):
        return {
            'message': 'Hello &arg1&, this is CodeBot; Version 0.5!',
            'arg1': self.getMention(user)
        }

    def fetchList(self, user):
        return {
            'message': '''
Usage: $[Command]
Command List:
    $ping - Make sure CodeBot is around
    $list - Show this list
    $challenge - Get the coding challenge of the day
    $register - Register yourself with CodeBot
    $addrep [user] - Give another user a reputation point
    $removerep [user] - Remove a reputation point from another user
    $showrep [user] - Show the reputation of a user
    $codebotdev - Learn more about CodeBots development
    $bug - Report a bug you found in CodeBot
        '''}

    def devInfo(self, user):
        return {
            'message': 'I am currently in development! To report a bug or learn more visit: https://github.com/Six-S/Coding-Corner-Discord-Bot'
        }

    def reportBug(self, user):
        return {
            'message': 'Found a bug? Report it here: https://github.com/Six-S/Coding-Corner-Discord-Bot/issues'
        }

    #### --------------- UTILITY FUNCTIONS --------------- ####

    def getMention(self, userToSearch):
        for user in self.all_users:
            if userToSearch in user.name:
                return user.mention

    def searchUsers(self, userToSearch):
        users = self.settings['users']

        #Let's make sure the user doesn't already exist.
        #NOTE: This brute force approach is fine for now, but
        #is super awful for bigger userbases. FIXME ASAP...
        for user in users:
            if userToSearch == users[user]['user']:
                return { 'key': user, 'user': users[user] }

            #There's no really "good" way to get the last index of a dict.
            #Just snag it here.
            lastUser = int(user)

        return { 'key': '', 'user': {}, 'lastKey': lastUser }

    def updateUserSettings(self, users):
        #Two "with" statements feels cleaner than seeking and writing
        #Load our current settings in, and update with our new information.
        with open('settings.json', 'r') as settings:
            current_settings = json.load(settings)
            current_settings['users'] = users

        #Write the new users to our settings.
        with open('settings.json', 'w') as settings:
            settings.write(json.dumps(current_settings))

    #Could probably do this better.
    def updateLocalSettings(self):
        with open('settings.json') as settings:
            self.settings = json.load(settings)

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
        bot.all_users = client.users

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        legal_actions = {
            '$ping': bot.pong,
            '$list': bot.fetchList,
            '$challenge': bot.getChallenge,
            '$register': bot.register,
            '$addrep': bot.addReputation,
            '$removerep': bot.removeReputation,
            '$showrep': bot.fetchReputation,
            '$codebotdev': bot.devInfo,
            '$bug': bot.reportBug
        }

        for action in legal_actions:
            if message.content.startswith(action):
                #try and get an argument out of the message if there is one.
                try:
                    user = message.content.split(' ')[1]
                except IndexError:
                    #FIXME: Find some logic to handle actions that a user can't perform on themselves (like addrep)
                    user = message.author.name

                response = legal_actions[action](user)
                # if message.author.name != user:
                user = message.author.name
                if len(response) == 1:
                    await message.channel.send(response['message'])
                elif len(response) > 1:
                    #since we don't have access to our discord scope in the bot class
                    #do a makeshift "format" here, find and replace with correct values.
                    full_response = response['message'].replace('&arg1&', response['arg1'])

                    #arg2 only exists when there is a second argument.
                    #NOTE: I'll probably find another solution here if I really need more than
                    #two arguments. but for now I only need a max of two.
                    try:
                        full_response = full_response.replace('&arg2&', response['arg2'])
                    except KeyError:
                        pass

                    await message.channel.send(full_response)

                    return
                # else:
                #     await message.channel.send('You cant perform that action on yourself, @{0}'.format(message.author.name))

    client.run(bot.token)
