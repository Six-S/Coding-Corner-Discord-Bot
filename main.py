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
        
        #Figure out if this user has already registered.
        #if they have, quit now.
        results = self.searchUsers(requester)
        if self.empty(results['key']):
            print('[WARN] Cannot register user "{0}" as they are already registered.'.format(requester))
            return {
                'message': "Something went wrong registering you, &arg1&... are you already registered?",
                'arg1': self.getMention(requester)
            }
        
        #since we don't currently have this user, let's build their profile!
        #NOTE: The way we get our new user key feels shitty. FIXME.
        new_user = {
            str(results['lastKey'] + 1): {
                "user": requester,
                "rating": 0,
                "callMe": ""
            }
        }
        users.update(new_user)

        #update our global settings
        self.updateUserSettings(users)

        #set our updated settings to our class level settings variable and return.
        self.updateLocalSettings()
        return {
            'message': "You've been successfully registered, &arg1&",
            'arg1': self.getMention(requester)
        }

    #function that returns the coding challenge of the day.
    def getChallenge(self, user):
        with open('/root/challenge.txt', 'r') as challenge:
            body = challenge.read()
            #When pulling from the email, we get all of these "=", so handle those while we pull the body out.
            #NOTE: The formatting of the body could use some work, it's sorta all over the place when it comes out.
            #Can probably handle that in v2 of the email worker, but either way.
            challenge_body = body.split('-')[0].replace('=', '')
            return { 'message': challenge_body }

    #Function that adds reputation to a specific user.
    def addReputation(self, user_to_add):

        #define a list of our current users
        users = self.settings['users']
        found_user = {}

        #look to see if we have a user to add rep to.
        found_user = self.searchUsers(user_to_add)
        
        if self.empty(found_user['key']):
            #increase rep
            updated_value = {'rating': users[found_user['key']]['rating'] + 1}
            users[found_user['key']].update(updated_value)

            #update value
            self.updateUserSettings(users)

            #set our updated settings to our class level settings variable and return.
            self.updateLocalSettings()
            return {
                'message': "You've given a reputation point to &arg1&!",
                'arg1': self.getMention(user_to_add)
            }
        else:
            print('[WARN] Cannot modify user "{0}" as they are not yet registered.'.format(user_to_add))
            return {
                'message': "Something went wrong giving a reputation point to &arg1&. Are they registered?",
                'arg1': self.getMention(user_to_add)
            }

    #function to remove reputation from a specific user.
    def removeReputation(self, user_to_remove):

        #define a list of our current users
        users = self.settings['users']
        found_user = {}

        found_user = self.searchUsers(user_to_remove)

        if self.empty(found_user['key']):
            #Grab rating.
            rating = users[found_user['key']]['rating']

            #probably don't want to mess around with negative numbers.
            if rating >= 0:
                updated_value = {'rating': rating - 1}
                users[found_user['key']].update(updated_value)
            else:
                print('[WARN] "{0}" has a reputation at or less than 0. Returning.'.format(user_to_remove))
                return {
                    'message': "&arg1&s reputation can't go any lower!",
                    'arg1': self.getMention(user_to_remove)
                }

            #uddate our settings
            self.updateUserSettings(users)
            
            #set our updated settings to our class level settings variable and return.
            self.updateLocalSettings()
            return {
                'message': "You've removed a reputation point from &arg1&!",
                'arg1': self.getMention(user_to_remove)
            }
        else:
            print('[WARN] Cannot modify user "{0}" as they are not yet registered.'.format(user_to_remove))
            return {
                'message': "Something went wrong removing a reputation point from &arg1&. Are they registered?",
                'arg1': self.getMention(user_to_remove)
            }

    #### --------------- SIMPLE REPLIES --------------- ####
    
    #Function to get the reputation of a user
    def fetchReputation(self, user_to_fetch):
        users = self.settings['users']

        found_user_key = self.searchUsers(user_to_fetch)['key']

        points = users[found_user_key]['rating']

        return {
            'message': '&arg1& currently has &arg2& points!',
            'arg1': self.getMention(user_to_fetch),
            'arg2': str(points)
        }

    #Function that confirms CodeBot is listening.
    def pong(self, user):
        return {
            'message': 'Hello &arg1&, this is CodeBot; Version 0.5!',
            'arg1': self.getMention(user)
        }

    #Function that returns our list of commands
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

    #function that returns devinfo
    def devInfo(self, user):
        return { 'message': 'I am currently in development! Want to learn more or submit a feature request? Visit https://github.com/Six-S/Coding-Corner-Discord-Bot' }

    #function that returns bug link
    def reportBug(self, user):
        return { 'message': 'Found a bug? Report it here: https://github.com/Six-S/Coding-Corner-Discord-Bot/issues' }

    #### --------------- UTILITY FUNCTIONS --------------- ####

    #Function that returns an ID that can be used to mention a user.
    def getMention(self, user_to_mention):
        for user in self.all_users:
            #FIXME TODO
            #if the userbase gets above like... 20,
            #this needs to be rewritten. 
            if user_to_mention in user.name:
                return user.mention

        #if the user doesn't exist in discord, or there was a typo,
        #just return here and let the rest of the error handling do its thing.
        return user_to_mention

    def searchUsers(self, user_to_search):
        users = self.settings['users']

        #Let's make sure the user doesn't already exist.
        #NOTE: This brute force approach is fine for now, but
        #is super awful for bigger userbases. FIXME
        for user in users:
            if user_to_search == users[user]['user']:
                return { 'key': user, 'user': users[user] }

            #There's no really "good" way to get the last index of a dict.
            #Just snag it here.
            last_user = int(user)

        return { 'key': '', 'user': {}, 'lastKey': last_user }

    #Function to write new data to our user object in our settings.
    def updateUserSettings(self, users):
        #Two "with" statements feels cleaner than seeking and writing
        #Load our current settings in, and update with our new information.
        with open('settings.json', 'r') as settings:
            current_settings = json.load(settings)
            current_settings['users'] = users

        #Write the new users to our settings.
        with open('settings.json', 'w') as settings:
            settings.write(json.dumps(current_settings))

    #Function that updates our class level settings variable with current settings.
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

        #List of all legal commands, and the matching function
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

        #list of actions you cannot perform on yourself.
        selfless_actions = ['$addrep', '$removerep']

        #top level check to make sure this command isn't messed up.
        if message.author.name in message.content:
            await message.channel.send('{0} - To run a command on yourself, run it without an argument.'.format(message.author.mention))
            return False

        #top level check to make sure the person didn't try to tag the user they're performing an action on.
        #NOTE: I'm not sure if this is right or not. Without this, there will be two mentions per command which seems annoying/excessive.
        #additionally, some small stuff will need to be modified to work with mentions. 
        if '@' in message.content:
            await message.channel.send('{0} - Please avoid tagging the user you are trying to perform this action on.'.format(message.author.mention))
            return False

        for action in legal_actions:
            if message.content.startswith(action):
                #try and get an argument out of the message if there is one.
                try:
                    user = message.content.split(' ')[1]
                except IndexError:
                    #FIXME: Find some logic to handle actions that a user can't perform on themselves (like addrep)
                    if action not in selfless_actions:
                        user = message.author.name
                    else:
                        await message.channel.send('You cant perform that action on yourself, {0}'.format(message.author.mention))
                        return False

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

    client.run(bot.token)
