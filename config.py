stat_value_status = ['following','unfollowing','resting']
'''0) following
   1) unfollowing
   2) resting'''
stat_key_followed = 'followed'
stat_key_unfollowed = 'unfollowed'
stat_key_logins = 'logins'
stat_key_count = 'count'


#===============|Url's|================:
loginurl = 'https://www.instagram.com/accounts/login/'
userUrl = "https://www.instagram.com/" # + username/

##===============|Proxy|================:
proxy='unknown'

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

