import config
from seleniumbase import SB
from time import sleep
import datetime
from datetime import timedelta
import pytest
from classes import *
import json

class Controller():
    def __init__(self,*args,**kwargs) -> None:
        pass
    def start(self,username,password,option=0):
        '''
        (start is the user controller)
        1. mass unfollow
        2. Always Follow (by target)
        3. Unfollow by app
        '''
        user = self.add_load_bot(username,password)
        user.startDriver()
        login_result = user.login()
        if login_result ==100:
            return
        act_result = user.act(option)
        if(act_result==200):
            self.talk('Action limit per day reached. You can change this value in the account configuration (not recomended for new accounts).')
            input('Continue?')


    def add_load_instagram_account(self,username,password=None)->Instagram_Account:
        '''Returns instagram account object.'''
        instagram_acc=session.query(Instagram_Account).filter_by(username=username).first()
        if instagram_acc == None:
            instagram_acc = Instagram_Account(
                #account info
                username=username,
                password=password,
                logins=0,
                last_login = None,
                credits=0,
                nickname='',
                restore=0,
                isbroken=False
            )
            session.add(instagram_acc)
            session.commit()
        return instagram_acc
    

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
                credits=0,
                nickname='',
                restore=0,
                isbroken=False,
                #bot info
                tokens=200,
                status='Resting',
                waitUntil=datetime.datetime.now(),
                isbot=True,
                avaliable=True,
                total_followed=0,
                total_unfollowed=0,
                following_list_json=json.dumps(list),
                targeting_list_json=json.dumps(list),
                actions_per_day=200,
                actions_rest_time=3600*24,
                wait_after_click = 0.5,
                browser_visible=True
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

    def getBots(self) -> list:
        '''Return object list'''
        return session.query(Bot_Account).all()

    def talk(self,words:str):
        print('Controller: ' + words)

    def windows_create_autostartup(self):
        '''Creates an autostartup batch file in the windows startup folder.'''
        
        script=f"start /min \"\" \"{config.get_running_path()}\""
        script_path = os.path.join(config.get_startup_folder(),config.AutoRun_Script_Name)
        self.talk(f'Creating startup file...\nPath:{script_path}')
        try:
            with open(script_path, "w") as file:
                file.write(script)
                file.close()
                self.talk('Created.')
        except:
            print(f'Error writing the script path. AutoStartup was not enabled. \nPath: {script_path}')
            input('return')

        pass

    '''Website functions (if you are coming from github, ignore the following code)'''
    def website_bot_follow(self):
        '''
        Due to pytest nature, the controller cannot manage user() behavior completely. Thats why the bot user() 
        will be doing some controller actions like checking lists, time, etc.
        '''
        #pytest --uc -s --proxy=brd-customer-hl_########-zone-residential:############@brd.superproxy.io:##### --locale=us --var1=target bot.py
        pytest_args = [ #pytest -k testname (without "test_") code.py
            "-n=2", #hilos
            "--uc",#undetected
            "-s", #permite print-talk
            "--locale=us",
            "--var1=None",
            "--k=website_bot_follow",
            "bot.py" #archivo
        ]
        pytest.main(pytest_args)

    def website_restore_targeting(self):
        users = session.query(Instagram_Account).filter(Instagram_Account.restore>0).filter_by(isbroken=False).all()
        if not users:
            return
        for user in users:
            av_bots = self.website_get_avaliable_bots(user.username)
            self.website_set_bots_target(user,av_bots,user.restore,restoring=True)
    
    def website_set_bots_target(self,instagram_acc:Instagram_Account,botlist:list,amount:int,restoring:bool=False)->None:
        '''
        instagram_acc: objeto cuenta de instagram
        botlist: una lista de objetos bot (obtener de website_get_avaliable_bots() para que sean activos)
        amount: cantidad de bots a asignar 
        '''
        b = botlist
        bot_size_tuples = [(bot, len(bot.targeting)) for bot in b]
        sorted_bots = sorted(bot_size_tuples, key=lambda x: x[1]) #buscar bots con menor carga
        for bot,val in sorted_bots[:amount]: #cortar la lista segun los bots requeridos
            if(instagram_acc.username==bot.username):
                continue
            bot.targeting.append(instagram_acc)
            if restoring:
                instagram_acc.restore-=1
            #guardar datos del bot
            session.commit()

    def website_get_avaliable_bots(self,target:str=None)->list:
        '''
        -Returns avaliable bots for following target (excluding broken, targeting and following)
        -Returns all online bots if no target is specified.
        -Removes targets from broken bots
        '''
        result_bots = []
        bots = self.getBots()
        for bot in bots:
            uname = bot.username
            b = session.query(Bot_Account).filter_by(username=uname).first()
            if b.isbot and not b.isbroken:
                if target:
                    following = [client.username for client in b.following]
                    targeting = [client.username for client in b.targeting]
                    if not target in following and not target in targeting:
                        if b.username != target:
                            result_bots.append(b)
                else:
                    result_bots.append(b)
            else:
                continue
        return result_bots

    def website_buy_followers(self,instagram_acc:Instagram_Account,amount:int)->str:
        '''
        -Chequea si la cuenta cumple los requisitos (tener bots disponibles para el)
        -Asigna target al bot
        -Agrega los creditos
        -Guarda los nuevos datos
        '''

        #chequear cantidad solicitada
        if amount <= 0:
            error = 'Requested credit is less than 1'
            self.talk(error)
            return error          
        
        #chequear existencia de cliente
        if not instagram_acc:
            error = 'Client doesn\'t exist.'
            self.talk(error)
            return error
        
        #longitud de lista de objetos bots obtenida de avaliable bots
        avaliable_bots_obj = self.website_get_avaliable_bots(instagram_acc.username)
        avaliable_bots = len(avaliable_bots_obj)

        #chequear si alcanzan los bots para la compra
        if (avaliable_bots < amount):
            error = 'Not enough bots to do the job for your account.'
            self.talk(error)
            return error

        #asignar target a los bots
        self.website_set_bots_target(instagram_acc,avaliable_bots_obj,amount)

        #darle los creditos al cliente
        instagram_acc.credits +=amount

        #guardar datos del usuario
        session.commit()
        
    
    def debug_load_bots_from_file(self,path:str)->None:
        with open(path,'r') as file:
            diccionario = dict()
            for line in file:
                key, value = line.strip().split(':', 1)  # Split into key and value using the first occurrence of ": "
                diccionario[key] = value
            file.close()
        
        for username,password in diccionario.items():
            self.add_load_bot(username,password)
            self.add_load_instagram_account(username,password)
