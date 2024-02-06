from time import sleep
import random
import datetime
from datetime import timedelta
from seleniumbase import Driver
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey,Table,Column, DateTime, Integer,Boolean, insert
from sqlalchemy.orm import sessionmaker, relationship,scoped_session
from sqlalchemy.sql import func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import declarative_base
import config
import json

loginurl = config.loginurl
instaUrl = config.userUrl

Base = declarative_base()

Following = Table(
                    'bot_following_account',
                    Base.metadata,
                    Column('bot_id',Integer),
                    Column('followed_id',Integer)
                )

Targeting = Table(
                    'bot_targeting_account',
                    Base.metadata,
                    Column('bot_id',Integer),
                    Column('targeted_id',Integer)
                )


class Receipt(Base):
    __tablename__ = 'receipts'
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    creation_date = Column(DateTime)
    account_id = Column(Integer, ForeignKey('accounts.id'))

class Account(Base):
    __tablename__='accounts'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    logins = Column(Integer)
    last_login = Column(DateTime)



class Instagram_Account(Account):
    credits = Column(Integer)
    nickname = Column(String)
    restore = Column(Integer)
    isbroken = Column(Boolean)  
    receipts = relationship('Receipt', backref='client') 

    
class Bot_Account(Instagram_Account):
    tokens = Column(Integer)
    status = Column(String)
    waitUntil = Column(DateTime)
    isbot = Column(Boolean)  
    avaliable = Column(Boolean)
    total_followed = Column(Integer)
    total_unfollowed = Column(Integer)
    following_list_json = Column(String)
    targeting_list_json = Column(String)
    actions_per_day=Column(Integer)
    actions_rest_time=Column(Integer)
    wait_after_click = Column(Float)
    browser_visible=Column(Boolean)

    targeting = relationship(
        'Instagram_Account',
        secondary=Targeting,
        primaryjoin=(Targeting.c.bot_id == Account.id),
        secondaryjoin=(Targeting.c.targeted_id  == Account.id),
        backref='targeted_by'
    )

    following = relationship(
        'Instagram_Account',
        secondary=Following,
        primaryjoin=(Following.c.bot_id == Account.id),
        secondaryjoin=(Following.c.followed_id  == Account.id),
        backref='followed_by'
    )
    
    def saveInstance(self):
        session.commit()

    def startDriver(self,proxy=False):
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
        print("("+self.username+"): " + words)
        
    def goto(self,url):
        self.driver.open(url)
        self.talk("Going to " + url)
        self.wait(3,'loading site')

    def scroll(self):
        '''Scroll followers window (instagram.com/user/followers)'''

        self.talk("trying to scroll...")
        self.driver.execute_script('''
        window.scrollBy(0,2000)                           
        ''')
        self.talk("scrolled...")

    def unfollow(self,target): #since the program cannot detect if the user accepted the follow request, try both cases.
        '''When on user page, click unfollow'''
        try:
            self.driver.click('button:contains("Following")')
            self.driver.click(self.convert_xpath_to_css("//span[text()='Unfollow']"))
            #if following button is not present, it may be a 'requested' button
        except:
            try:
                self.driver.click('button:contains("Requested")')
                self.driver.click('button:contains("Unfollow")')
            except:
                self.talk("Error unfollowing " + target)
                return
            
        #save stats
        try:
            self.tokens-=1
            following_list = json.loads(self.following_list_json)
            try:
                following_list.remove(target)
            except:
                self.talk("Error: user was'nt in database")
            self.following_list_json = json.dumps(following_list)
            self.saveInstance()
        except:
            self.talk('Error saving stats')
            pass

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
    

    def act(self,action: int):
        '''
        target: username of target account (if following)
        tokens: 'credit' until return
        actions:
            1. Mass unfollow everyone
            2. Follow Followers of target (select random target from list) (configure from menu first)
            3. Unfollow followed by this app
        '''
        if action==1 or action==2: 
            if action==1: # go to self following list
                self.goto(instaUrl+self.username+'/'+'following/')
            if action==2: # open followers list from target
                try:
                    targets_list=json.loads(self.targeting_list_json)
                    target = targets_list[random.randint(0, len(targets_list)-1)]
                except:
                    self.talk("No target was selected. Please configure a target to follow its followers. For example: if the target is the account @elonmusk, then his followers will be automatically followed.")
                    input("Continue")
                    return 1
                self.goto(instaUrl+target)
                self.driver.click('/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/ul/li[2]/a') #since instagram blocks direct access to the followers list, you must click the "followers" button from their profile instead of accessing the followers URL.
            divnumber=0
            while True: #loop follow/unfollow
                #Check if user can perform actions
                if not self.check_avaliable():
                    return 2
                try:
                    divnumber+=1
                    if action==1: #unfollow self following
                        #get buttons and button data
                        username = config.xpath_followlist_username(str(divnumber))
                        followbtn = config.xpath_followlist_follow_unfollow_button(str(divnumber))
                        followedname = self.driver.get_text(username)

                        #print something
                        self.talk('Unfollowing: ' +str(divnumber)+': ' +  followedname)

                        #perform action (unfollow)
                        self.driver.click(followbtn)
                        self.driver.click('button:contains("Unfollow")')

                        # Save stats to user object 
                        self.total_unfollowed+=1
                        try:
                            following_list = json.loads(self.following_list_json)
                            following_list.remove(followedname)
                            self.following_list_json = json.dumps(following_list)
                        except:
                            pass

                    if action==2: #follow target's followers
                        #get buttons and button data
                        username = config.xpath_followers_username(str(divnumber))
                        followbtn = config.xpath_followers_follow_unfollow_button(str(divnumber))
                        followedname = self.driver.get_text(username)
                        buttonvalue = self.driver.get_text(followbtn)
                        
                        #print something
                        self.talk('Following '+str(divnumber)+': ' +  followedname)

                        #perform action (follow)
                        if not (buttonvalue == 'Follow'):
                            continue
                        self.driver.click(followbtn)

                        # Save stats to user object 
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
                except:
                    self.scroll()
                    

        elif action==3:# Unfollow automated followed
            #checks if user can perform actions
            if not self.check_avaliable():
                return 2
            self.following_list_json = json.loads(self.following_list_json)
            for target in self.following_list_json:
                if not self.check_avaliable():
                    return
                self.goto(instaUrl+target)
                self.unfollow(target)
   
    def login(self):
        self.talk("Trying to login into " + self.username)
        self.goto(loginurl)
        self.driver.type('input[name="username"]', self.username)
        self.driver.type('input[type="password"]', self.password)
        self.driver.click('button:contains("Log in")')
        #self.wait(4,'After login')
        if(self.checkText("Save your login info?")):
            self.talk("login checked")
            self.logins+=1
            self.saveInstance()
        else:
            self.talk("Could not check login sucess")
            return 100
        
    def checkText(self,text: str) -> bool:
        '''Check if text is present in page. Returns bool'''
        try:
            self.driver.assert_text(text)
            return True
        except:
            return False
        
engine = create_engine('sqlite:///InstaGrow.UserData.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
