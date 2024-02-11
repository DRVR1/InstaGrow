from time import sleep
import random
import datetime
from datetime import timedelta
from seleniumbase import Driver
from seleniumbase.fixtures import xpath_to_css
from sqlalchemy import create_engine, Column, Integer, String, Float,Column, DateTime, Integer,Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
import config
import json

loginurl = config.loginurl
instaUrl = config.userUrl

Base = declarative_base()

class Account(Base):
    __tablename__='accounts'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    logins = Column(Integer)
    last_login = Column(DateTime)

class Bot_Account(Account):
    tokens = Column(Integer)#remaining actions in the defined time interval. 
    waitUntil = Column(DateTime)#The date when the tokens will be restored to actions_per_day value and 'avaliable' will be set to true
    avaliable = Column(Boolean)#defines if the bot is waiting that time interval.
    total_followed = Column(Integer)#stats
    total_unfollowed = Column(Integer)#stats
    following_list_json = Column(String)#a list of the people the user is following with this app
    targeting_list_json = Column(String)#a list of the people whose followers will be followed
    actions_per_day=Column(Integer) #how much actions per time interval are allowed
    actions_rest_time=Column(Integer)#wait time interval since you run out of tokens
    wait_after_click = Column(Float)#how much time the bot waits after clicking a button
    browser_visible=Column(Boolean)#sets browser visibility (headed/headless)
    scheduled_enabled = Column(Boolean)#sets automatic actions flag (act when the program starts)
    scheduled_follows = Column(Integer)#sets the total number of account that must be followed
    scheduled_unfollows = Column(Integer)#sets the total number of account that must be unfollowed
    scheduled_unfollows_everyone = Column(Boolean)#a bool that defines wether the scheduled unfollow should look at the following_list_json, or just unfollow everyone

    def saveInstance(self):
        session.commit()

    def startDriver(self,proxy=False):
        
        self.talk('Starting ChromeDriver...')

        if not config.debug_mode:
            from seleniumbase.config import settings
            settings.HIDE_DRIVER_DOWNLOADS = True #hide download warning for pyinstaller users

        if not self.browser_visible:
            self.driver = Driver(uc=True,locale_code='en',proxy=proxy,is_mobile=True,headed=False,headless=True)
        else:
            self.driver = Driver(uc=True,locale_code='en',proxy=proxy,is_mobile=True,headed=True,headless=False)

    def wait(self,time,reason:str=False) -> None:
        if reason:
            self.talk("Waiting "+ str(time) + " seconds. Reason: " + reason)
        sleep(time)
        pass

    def talk(self,words):
        if(config.debug_mode):
            print("("+self.username+")(debug mode): " + words)
        else:
            print("("+self.username+"): " + words)
        
        
    def goto(self,url):
        self.driver.open(url)
        self.talk("Going to " + url)

    def scroll(self):
        '''Scroll followers window (instagram.com/user/followers)'''
        scrollby = '230'
        self.driver.execute_script(f'''window.scrollBy(0,{scrollby})''')
        self.talk("Scrolled " + scrollby + 'px.')

    def unfollow(self,target,following_list): #since the program cannot detect if the user accepted the follow request, try both cases.
        self.goto(config.userUrl+target)

        '''When on user page, click unfollow'''
        unfollow=True
        unfollowed = False

        follow_unfollow_button = xpath_to_css.convert_xpath_to_css(config.xpath_profile_FollowUnfolowButton_loggedIn())
        #TODO optimize wait time
        self.wait(4,'Elements load')
        try:
            button = self.driver.find_elements(follow_unfollow_button)[0]
            if(button.text == 'Follow'):
                self.talk('Not following user, erasing and returning')
                unfollow=False
        except:
            pass
        if unfollow:
            try:
                self.driver.click('button:contains("Following")')
                self.driver.click('span:contains("Unfollow")')
                unfollowed=True
                #if following button is not present, it may be a 'requested' button
            except:
                try:
                    self.driver.click('button:contains("Requested")')
                    self.driver.click('button:contains("Unfollow")')
                    unfollowed=True
                except:
                    self.talk("Error unfollowing " + target)
        #save stats
        if unfollowed:
            self.tokens-=1
            self.wait(1,'Unfollowing')
            self.talk('Unfollowed ' + target)
        try:
            following_list.remove(target)
        except:
            self.talk("Error: user was'nt in database")
        self.following_list_json = json.dumps(following_list)
        self.saveInstance()


    def check_avaliable(self)->bool:
        if self.tokens<=0 and self.avaliable:
            self.avaliable=False
            new_time =  datetime.datetime.now() + timedelta(seconds=self.actions_rest_time)
            self.waitUntil = new_time.strftime("%H:%M:%S - %d %B %Y")
            self.time_save_timestamp()
            return False
        if self.time_hasPassed(seconds=self.actions_rest_time) and not self.avaliable:
            self.tokens=self.actions_per_day
            self.avaliable = True
            self.saveInstance()
            return True
        if not self.avaliable:
            return False
        return True
    
    def time_hasPassed(self,hours=0,seconds=0)->bool:
        '''Specify a Bot object (self), and the time that should have passed from (waitUntil) to return true'''
        previous_timestamp = self.waitUntil
        
        # Get the current timestamp
        current_timestamp = datetime.datetime.now()

        # Calculate the time difference
        time_difference = current_timestamp - previous_timestamp

        if hours and not seconds:
            if time_difference.total_seconds() >= hours * 3600: 
                return True
            else:
                return False
        elif seconds and not hours:
            if time_difference.total_seconds() >= seconds:  
                return True
            else:
                return False
        else:
            print("newtime: Time error. Used multiple time formats")
            return

    def time_save_timestamp(self):
        current_timestamp = datetime.datetime.now()
        self.waitUntil = current_timestamp
        self.saveInstance()
    

    def act(self,action: int,forced:bool=False)->int:
        '''
        actions:
            1. Mass unfollow everyone
            2. Follow Followers of target (select random target from list) (configure from menu first)
            3. Unfollow followed by this app

            if forced, it means the bot was started with no human intervention.
        '''
        if action==1 or action==2: 
            if action==1: # go to self following list
                self.goto(instaUrl+self.username+'/'+'following/')
            if action==2: # open followers list from target
                try:
                    targets_list=json.loads(self.targeting_list_json)
                    target = targets_list[random.randint(0, len(targets_list)-1)]
                except:
                    self.driver.close()
                    self.talk("No target was selected. Please configure a target to follow its followers. For example: if the target is the account @elonmusk, then his followers will be automatically followed.")
                    input("Continue")
                    return
                self.goto(instaUrl+target)

                button_following_xpath = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/ul/li[2]/a'
                if config.debug_mode:
                    self.talk(f'trying to click {button_following_xpath}')
                self.driver.click(button_following_xpath) #since instagram blocks direct access to the followers list, you must click the "followers" button from their profile instead of accessing the followers URL.
                if config.debug_mode:
                    self.talk(f'clicked?')
            divnumber=0
            except_streak = 0
            restricted = False
            while True: #loop follow/unfollow
                #Check if user can perform actions
                if not self.check_avaliable():
                    self.driver.close()
                    return 200
                try:
                    divnumber+=1
                    if action==1: #unfollow self following
                        if forced:
                            if self.scheduled_unfollows<=0:
                                self.driver.close()
                                return 300
                        #get buttons and button data
                        username = config.xpath_following_username(str(divnumber))
                        followbtn = config.xpath_following_FollowUnfolowButton(str(divnumber))
                        followedname = self.driver.get_text(username)

                        #print something
                        self.talk('Unfollowing: ' +str(divnumber)+': ' +  followedname)

                        #perform action (unfollow)
                        self.driver.click(followbtn)
                        self.driver.click('button:contains("Unfollow")')
                        except_streak=0#reset excepction streak

                        # Save stats to user object 
                        self.total_unfollowed+=1
                        if forced:
                            self.scheduled_unfollows-=1
                        try:
                            following_list = json.loads(self.following_list_json)
                            following_list.remove(followedname)
                            self.following_list_json = json.dumps(following_list)
                        except:
                            pass

                    if action==2:#follow target's followers
                        if forced:
                            if self.scheduled_follows<=0:
                                self.driver.close()
                                return 300
                        #get buttons and button data
                        username = config.xpath_followers_username_unrestricted(str(divnumber))
                        followbtn = config.xpath_followers_FollowUnfolowButton_unrestricted(str(divnumber))
                        if config.debug_mode:
                            self.talk('finding elements as unrestricted follower list:')
                            self.talk(f'username: {username}\nfollowbtn: {followbtn}')

                        followedname=''
                        buttonvalue=''
                        try:
                            if restricted:
                                username = config.xpath_followers_username_restricted(str(divnumber))
                                followbtn = config.xpath_followers_FollowUnfolowButton_restricted(str(divnumber))
                            followedname = self.driver.get_text(username)
                            buttonvalue = self.driver.get_text(followbtn)
                        except:
                            if restricted == True:
                                self.driver.close()
                                return 100
                            if(config.debug_mode):
                                self.talk('Unrestricted elements not found, trying restricted mode')
                            restricted = True

                        #print something
                        self.talk('Following '+str(divnumber)+': ' +  followedname)

                        #perform action (follow)
                        if not (buttonvalue == 'Follow'):
                            continue
                        self.driver.click(followbtn)
                        except_streak=0 #reset excepction streak

                        # Save stats to user object 
                        if forced:
                            self.scheduled_follows-=1
                        self.total_followed+=1
                        following_list = json.loads(self.following_list_json)
                        if followedname not in following_list:
                            following_list.append(followedname)
                        self.following_list_json = json.dumps(following_list)   

                    # Save stats to user object (both cases)
                    self.tokens-=1
                    self.talk('Remaining actions: ' + str(self.tokens))
                    self.wait(self.wait_after_click) #wait to perform another action
                    self.saveInstance()
                except Exception as e:
                    if config.debug_mode:
                        self.talk(f'\nan exception was found:\n{e}\n')
                    self.scroll()
                    divnumber-=1
                    except_streak+=1
                    if except_streak>=3:
                        self.driver.close()
                        return 100
                    

        elif action==3:# Unfollow automated followed
            #checks if user can perform actions
            following_list = json.loads(self.following_list_json)
            for target in following_list:
                if not self.check_avaliable():
                    self.driver.close()
                    return 200
                if forced:
                    if self.scheduled_unfollows<=0:
                        self.driver.close()
                        return 300
                self.unfollow(target,following_list)
                if forced:
                    self.scheduled_unfollows-=1
                    self.saveInstance()
            self.driver.close()
            return 15
   
    def login(self):
        self.talk("Trying to login into " + self.username)
        self.goto(loginurl)
        self.driver.type('input[name="username"]', self.username)
        self.driver.type('input[type="password"]', self.password)
        self.driver.click('button:contains("Log in")')
        if(self.checkText("Save your login info?")):
            self.talk("login checked")
            self.logins+=1
            self.saveInstance()
        else:
            self.driver.close()
            return 100
        
    def checkText(self,text: str) -> bool:
        '''Check if text is present in page. Returns bool'''
        try:
            self.driver.assert_text(text)
            return True
        except:
            return False
        


# Create the SQLAlchemy engine
engine = create_engine(f'sqlite:///{config.db_file_path}')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
