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

#---------------other user / followers
def xpath_followers_user_box(iterator:str)->str:
   #the last number of this variable is an iterator. It selects the user number within the list. 
   xpath_followlist_user_box_variable='/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div[2]/div[1]/div/div['+iterator+']'
   return xpath_followlist_user_box_variable

def xpath_followers_username(iterator:str)->str:
   #Username: 
   xpath_followlist_username= xpath_followers_user_box(iterator)+'/div/div/div/div[2]/div/div/div/a/div/div/span'
   return xpath_followlist_username

def xpath_followers_follow_unfollow_button(iterator:str)->str:
   #FollowButton:
   xpath_followlist_follow_button= xpath_followers_user_box(iterator)+'/div/div/div/div[3]/div/button'
   return xpath_followlist_follow_button

#---------------self user / FOLLOWING 
def xpath_followlist_user_box(iterator:str)->str:
   #the last number of this variable is an iterator. It selects the user number within the list. 
   xpath_followlist_user_box_variable='/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div[3]/div[1]/div/div['+iterator+']'
   return xpath_followlist_user_box_variable
def xpath_followlist_username(iterator:str)->str:
   #Username: 
   xpath_followlist_username= xpath_followlist_user_box(iterator)+'/div/div/div/div[2]/div/div/div/a/div/div/span'
   return xpath_followlist_username

def xpath_followlist_follow_unfollow_button(iterator:str)->str:
   #FollowButton:
   xpath_followlist_follow_button= xpath_followlist_user_box(iterator)+'/div/div/div/div[3]/div/button'
   return xpath_followlist_follow_button

##===============|CSS selectors|================: