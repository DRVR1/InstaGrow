import config
from seleniumbase import SB
from time import sleep
import datetime
from classes import *
import json
import os

class Controller():
    def __init__(self,*args,**kwargs) -> None:
        pass
    def start(self,username,password,option=0,forced:bool=False):
        '''
        (start is the user controller)
        1. mass unfollow
        2. Always Follow (by target)
        3. Unfollow by app
        '''
        user = self.add_load_bot(username,password)
        user.startDriver()

        #login
        login_result = user.login()

        if login_result ==100:
            self.talk("Could not check login sucess, please check your credentials or disable 2FA")

        #perform actions until run out of tokens
        act_result = user.act(option,forced=forced)

        if(act_result==100):
            self.talk('Elements not found, maybe the list is empty?')
        elif(act_result==200):
            self.talk('Action limit per day reached. You can change this value in the account configuration (not recomended for new accounts).')
        elif(act_result==15):
            self.talk('Task finished. You have unfollowed everyone who were followed by this app.')
        elif(act_result==300):
            self.talk('Reached the target scheduled tasks.')
        elif(act_result==404):
            self.talk('Error locating elements, please wait for an update')

        
    def autoStart(self):
        enabled_bots = session.query(Bot_Account).filter(Bot_Account.scheduled_enabled == True).all()
        if not enabled_bots:
            return 404
        for b in enabled_bots:
            print(f'enabled bot: {b.username} sch_follows: {str(b.scheduled_follows)} sch_unfollows: {str(b.scheduled_unfollows)}')
            if b.scheduled_follows:
                self.start(b.username,b.password,2,forced=True)
            elif b.scheduled_unfollows:
                self.start(b.username,b.password,3,forced=True)
            else: 
                #notify user
                b.scheduled_enabled=False
                b.saveInstance()

    def enable_autoStart(self,username:str)->bool:
        bot = self.add_load_bot(username)
        if not bot:
            return False
        bot.scheduled_enabled = True
        bot.saveInstance()

    def add_load_bot(self,username,password=None)->'Bot_Account':
        '''Returns user object.'''
        user=session.query(Bot_Account).filter_by(username=username).first()
        if user == None:
            #create new user object
            '''Creates and saves user. Returns user object after created'''
            list=[]
            user = Bot_Account(
                #account info
                username=username,
                password=password,
                logins=0,
                last_login = None,
                #bot info
                tokens=200,
                waitUntil=datetime.datetime.now(),
                avaliable=True,
                total_followed=0,
                total_unfollowed=0,
                following_list_json=json.dumps(list),
                targeting_list_json = json.dumps(list),
                actions_per_day=200,
                actions_rest_time=3600*24,
                wait_after_click = 0.5,
                browser_visible=True,
                scheduled_enabled=False,
                scheduled_follows=0,
                scheduled_unfollows=0,
                scheduled_unfollows_everyone= False
            )
            session.add(user)
            session.commit()
        return user
    
    def remove_bot(self,username):
        user=session.query(Bot_Account).filter_by(username=username).first()
        if user:
            session.delete(user)
            session.commit()
        else:
            self.talk('User ' + username + ' doesn\'t exist')

    def getBots(self) -> list['Bot_Account']:
        '''Return object list'''
        return session.query(Bot_Account).all()

    def talk(self,words:str):
        if not (config.debug_mode):
            print('Controller: ' + words)
        else:
            print('Controller (debug mode): ' + words)

    def windows_create_autostartup(self):
        '''Creates an autostartup batch file in the windows startup folder.'''
        
        script=f"start /min \"\" \"{config.get_running_path()}\" auto"
        script_path = os.path.join(config.get_startup_folder(),config.AutoRun_Script_Name)
        self.talk(f'Creating startup file...\nPath:{script_path}')
        try:
            with open(script_path, "w") as file:
                file.write(script)
                file.close()
                self.talk('Autostartup is now enabled.')
        except:
            print(f'Error writing the script path. AutoStartup was not enabled. \nPath: {script_path}')
            input('return')
    
    def windows_remove_autostartup(self):
        script_path = os.path.join(config.get_startup_folder(),config.AutoRun_Script_Name)
        self.talk(f'Removing startup file...\nPath:{script_path}')
        try:
            os.remove(script_path)
            self.talk('Autostartup is now disabled.')
        except:
            self.talk(f'Startup file was not found')

