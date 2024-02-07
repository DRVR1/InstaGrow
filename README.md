# InstaGrow (Pre Alpha)

## Project Description
Make your Instagram account grow in a slow and safe way by performing a defined number of actions per day to increase visibility.

## Features:
- Anti-ban precautions (Seleniumbase's undetected chromedriver + limited number of actions per day).
- Mass follow / unfollow instagram accounts.

## Coming soon:
- AutoStartup and automatic actions (no human intervention needed).
- Gui (A full and user-friendly user interface to make it simpler to use).
- Can be used with a proxy & handle multiple accounts (Concurrently)
- Automatic content posting (posts, comments, likes, histories).
- Compatibility with linux.
- Optimized Xpath search (Using IA, to find the xpath for elements whose position in the DOM changes frequently).


## Requirements

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
Randomly selects a user from the target list (this list must be configured first) and then mass follows its followers.<br><br>
- Mass Unfollow (Followed by Using This App)<br>
Only unfollows those who were followed using this app.
