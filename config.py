#dropping files in:
#appData
#programFiles
#autorun

import os
import sys

debug_mode = False

#===============|String Values|================:
AppName = 'InstaGrow'
AppVersion = 'pre-alpha'
AutoRun_Script_Name = 'InstaGrow.bat'
icon_path = "icon.ico"

#===============|Url's|================:
loginurl = 'https://www.instagram.com/accounts/login/'
userUrl = "https://www.instagram.com/" # + username/

##===============|Proxy|================:
proxy='unknown'

##===============|WINDOWS PATHS|================:
app_data_dir = os.path.join(os.path.expanduser('~'), 'AppData', 'Local', AppName)
if not os.path.exists(app_data_dir):
    os.makedirs(app_data_dir)
    
db_file_path = os.path.join(app_data_dir, f'{AppName}.UserData.db')

def get_startup_folder():
    appdata_path = os.environ.get('APPDATA')
    startup_folder = os.path.join(appdata_path, 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    return startup_folder

def get_running_path():
   return sys.executable

##===============|XPATHS|================:

#===============|Profile/Followers [Unrestricted]|================:
#sintax: SelectorType_Page_Element_Case

fragment_follow_button = '/div/div/div/div[3]/div/button'
fragment_username = '/div/div/div/div[2]/div/div/div/a/div/div/span'

def xpath_followers_userBox_unrestricted(iterator:str)->str:
   #the last number of this variable is an iterator. It selects the user number within the list. 
   return '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div[2]/div[1]/div/div['+iterator+']'#Normal followers view


def xpath_followers_username_unrestricted(iterator:str)->str:
   #Username: 
   return xpath_followers_userBox_unrestricted(iterator)+fragment_username
    

def xpath_followers_FollowUnfolowButton_unrestricted(iterator:str)->str:
   #FollowButton: 
   return xpath_followers_userBox_unrestricted(iterator)+fragment_follow_button

#===============|Profile/Followers [Restricted]|================:
def xpath_followers_userBox_restricted(iterator:str)->str:
   return '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[2]/div/div['+iterator+']'#Cant see all followers view

def xpath_followers_username_restricted(iterator:str)->str:
   #Username: 
   return xpath_followers_userBox_restricted(iterator)+fragment_username
    

def xpath_followers_FollowUnfolowButton_restricted(iterator:str)->str:
   #FollowButton: 
   return xpath_followers_userBox_restricted(iterator)+fragment_follow_button

#===============|Profile / following|================:
def xpath_following_userBox(iterator:str)->str:
   #the last number of this variable is an iterator. It selects the user number within the list. 
   return '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div[3]/div[1]/div/div['+iterator+']'

def xpath_following_username(iterator:str)->str:
   #Username: 
   return xpath_following_userBox(iterator)+fragment_username

def xpath_following_FollowUnfolowButton(iterator:str)->str:
   #FollowButton:
   return xpath_following_userBox(iterator)+fragment_follow_button

#===============|Profile|================:
def xpath_profile_FollowUnfolowButton_loggedIn() ->str:
   return '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/div[3]/div/div/button/div/div'

