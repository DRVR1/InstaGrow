# InstaGrow 

## ⚠️ This project is no longer being maintained so it may not work, please check the new project [instagrow2](https://github.com/DRVR1/Instagrow2) ⚠️

## Project Description
Computer softare, that automatically logs in your instagram account, and performs a defined number of actions per day, increasing your account visibility. 
You can download the windows installer in the "releases" section.

## Security Warning:
Since this is a pre-alpha, some functions are not yet avaliable, such as user data encryption. Your instagram password will be saved in a .db file in your appData folder. It won't be encrypted. Use it at your own risk.

## Features:
- Anti-ban precautions (Seleniumbase's undetected chromedriver + limited number of actions per day).
- Mass follow / unfollow instagram accounts.
- AutoStartup and automatic actions (no human intervention needed).

## Coming soon:
- Password-Protected database
- Save logs
- Use of cookies and cache
- Unfollow people who do not follow you.
- Gui (A full and user-friendly user interface to make it simpler to use).
- Can be used with a proxy & handle multiple accounts (Concurrently)
- Automatic content posting (posts, comments, likes, histories).
- Compatibility with linux.
- Optimized Xpath search (Using IA, to find the xpath for elements whose position in the DOM changes frequently).


## Requirements

- Tested in Windows 11

- Python3
- SeleniumBase
- Json
- sqlalchemy
  
## How to use (options explained)

- Change Username<br>
Change the saved username in the database (does not make any changes to your Instagram account).<br><br>
- Change Password<br>
Change the saved password in the database (does not make any changes to your Instagram account).<br><br>
- View Stats<br>
Displays usage statistics (login amount, total followed people, remaining actions, and more).<br><br>
- View Following<br>
Displays a list of Instagram usernames that are being followed by this app.<br><br>
- Configure Targets (for Mass Follow)<br>
Configure a list of targets from which you can mass follow their followers (they are selected randomly from the list at the moment of execution).<br><br>
- Change Daily Limit (Dangerous)<br>
Instagram rules prevent "abusive" or "spam" behavior by limiting the number of actions you can perform within a certain amount of time. These values can vary depending on your account's trust factor. The older your account is, the less chance you have of getting banned for performing excessive actions.<br><br>
- Change Wait Time after Clicking Buttons<br>
Changes the time the bot waits after clicking any button. This can be useful in helping to prevent Instagram from detecting "abusive" or "spam" behavior.<br><br>
- Toggle Browser Visibility<br>
Since this app uses the Chrome browser to perform actions on Instagram web, it can be hidden from view while performing them.<br><br>
- Mass Unfollow Everyone<br>
Warning: This will unfollow everyone, which may include friends or relevant accounts.<br><br>
- Mass Follow (by Target)<br>
Randomly selects an user from the target list (this list must be configured first) and then mass follows its followers.<br><br>
- Mass Unfollow (Followed by Using This App)<br>
Only unfollows those who were followed using this app.<br><br>
- Configure automatic actions<br>
When activating scheduled actions, this app will automatically start when you start Windows. Then it will perform the desired actions.
For example, if you set the total follows to 400 and total unfollows to 200, the app will prioritize the follows.<br> So, respecting the configured token limit (you can change it in settings, and by default is 200 every 24 hours), it will take 2 days to complete the follow requests (200 and 200) and one more day to complete the unfollow requests. Note that the program only starts unfollowing when all the follow requests are completed.<br>
For the following, there must be a target configured (the target is a user whose followers will be followed, so it's recommended to choose an account with a lot of followers. Also, check that the followers list is not partially limited, since this will generate errors).<br>
For the unfollowing, it just unfollows the people who have been followed by this app, excluding the rest.


![alt text](https://i.imgur.com/bWev0kN.png)
