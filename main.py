from classes import *
from controller import Controller
import os

controller = Controller()

def menu_delete_account(accname):
    controller.remove_bot(accname)
    

def menu_add_account():         
    username = str(input("\nUsername: @"))
    password = str(input("\nPassword: "))
    controller.add_load_bot(username,password)
    print("\nAdded.\n")
    menu_manage_accounts()

def menu_manage_accounts(back_username:str=False):
    tupleList = [''] 
    print('\nSelect an account: \n')
    stuser=''
    i=0
    if not back_username:
        try:
            for bot in controller.getBots():
                    username=bot.username
                    i+=1
                    print(str(i) +'. @'+ username)
                    tup = (i,username) 
                    tupleList.append(tup)
        except:
            print("Error reading users, try adding users first.")
            input("Continue")
            menu()
        try:
            op = int(input("\nOption: "))
        except:
            print('Option must be a number')
            menu()
        if op==0:
            menu()
        stuser = tupleList[op][1] #gather selected username from tuple list
    else:
        stuser=back_username
    os.system("cls")
    print('Selected user: ' + stuser)   
    user = controller.add_load_bot(stuser) 
    if not user:
        print('error')
        menu()
    bv='unknown'
    if user.browser_visible:
        bv='visible'
    else:
        bv='invisible'

    text=f'''          
    |-------|Account Data|-------|
    1. Change username
    2. Change password\n
    |-------|Statistics|-------|
    3. View stats
    4. View following\n
    |-------|Configuration|-------|
    5. Configure targets (for mass follow)
    6. Change daily limit (dangerous)
    7. Change wait time after clicking buttons
    8. Toggle browser visibility: [{bv}]\n
    |-------|Actions|-------|
    9. Mass unfollow everyone, including your friends (if you have)  
    10. Mass follow (by target)
    11. Mass unfollow (followed by using this app)\n
    |-------|Configuration (Warning)|-------|
    99. Delete'''
    text9='    0. Back'


    print(text)
    print(text9)
    try:
        op = int(input("\nOption: "))
    except:
        print('Option must be a number')
        menu()
    


    if op == 1:
        print("Note that this changes are NOT applied to your instagram account.")
        print("Current username: " + user.username)
        op = str(input("\nNew username: @"))
        user.username = op
        user.saveInstance()
        menu_manage_accounts(user.username)
    if op==2:
        print("Note that this changes are NOT applied to your instagram account.")
        op = str(input("\nNew password: "))
        user.password = op
        user.saveInstance()
        menu_manage_accounts(back_username=user.username)
    if op==3:
        print('Username: ' + user.username)
        print('Logins: ' + str(user.logins))
        print('Status: ' + str(user.status))
        print('Avaliable actions: ' + str(user.tokens))
        print('Total followed: ' + str(user.total_followed))
        print('Total unfollowed: ' + str(user.total_unfollowed))
        input("\nContinue?\n")
        menu_manage_accounts(user.username)
    if op == 4:
        following = json.loads(user.following_list_json)
        if not following:
            print("\nYou don't follow anyone with this app")
            input("\nContinue?\n")
            menu_manage_accounts(user.username)
        print('Accounts you follow using this app:\n')
        for acc in following:
            print('@'  + acc)
        input("\nContinue?\n")
        menu_manage_accounts(user.username)
    if op == 5:        
        text = '''\n
        1. Add target
        2. Remove target
        3. Display targets
        0. Back
        '''
        print(text)
        op = int(input("Option: "))
        
        if(op == 1):
            tar = input("Enter target to add: @")
            targets_list=json.loads(user.targeting_list_json)
            targets_list.append(tar)
            user.targeting_list_json=json.dumps(targets_list)
            user.saveInstance()
            print("Added " + tar + " to targets.")
            input("Continue")
        if(op == 2):
            print('Select wich target to remove:')
            user_targets = json.loads(user.targeting_list_json)
            iterator=0
            asociacion=[]
            for target in user_targets:
                print(str(iterator) + '. @' + target)
                asociacion.append((iterator,target))
            selected = int(input('Selection: '))
            target = asociacion[selected][1]
            user_targets.remove(target)
            user.targeting_list_json = json.dumps(user_targets)
            user.saveInstance()
            print("Removed " + target + " from targets.")
            input("Continue")
        if(op == 3):
            print("Target list: ")
            targets_list=json.loads(user.targeting_list_json)
            print('\n')
            i=0
            for target in targets_list:
                i+=1
                print(str(i)+'. @'+target)
                print('\n')
            input("All targets listed. Continue?")
        if(op ==0):
            menu_manage_accounts(user.username)
        user.saveInstance()

        menu_manage_accounts(user.username)

    if op==6:
        print('Your daily limit is ' + str(user.actions_per_day) + ' and your currently avaliable actions are ' + str(user.tokens))
        lim = int(input('Enter new limit (0 for cancel): '))
        if lim<=0:
            menu_manage_accounts(user.username)
        user.actions_per_day = lim
        user.tokens = lim
        user.saveInstance()
        print('\nDaily limit changed.\n')
        input("Continue")
        menu_manage_accounts(user.username)

    if op==7:
        print('\nCurrent waiting time is: ' + str(user.wait_after_click) + ' seconds.')
        lim = float(input('Enter new time (0 for cancel): '))
        if lim<=0:
            menu_manage_accounts(user.username)
        user.wait_after_click=lim
        user.saveInstance()
        input('waiting changed to ' + str(lim) + ' seconds. Continue?')
        menu_manage_accounts(user.username)

    if op==8:
        user.browser_visible = not user.browser_visible
        user.saveInstance()
        menu_manage_accounts(user.username)

    if op == 9:# just mass unfollow
        controller.start(user.username, user.password, 1)

    if op == 10: #Follow by target
        controller.start(user.username, user.password, 2)

    if op == 11: #unfollow by followed in app
        controller.start(user.username, user.password, 3)



    if op == 99:
        op = int(input('\nThis will get the data of your account deleted from this program. \n\n1. Delete\n2. Cancel\nInput: '))
        if op==1:
            controller.remove_bot(user.username)
            menu()
        else:
            menu_manage_accounts(user.username)

    if op == 0:
        menu_manage_accounts()

def menu():
    os.system('cls')
    print("\nWelcome.")
    print('Remember to disable 2FA (two factor autentication)')
    
    text='''          
    1. Add account
    2. Manage accounts
    3. Autostartup (TODO) 
    0. Exit'''
    print(text)

    try:
        op = int(input("\nOption: "))
    except:
        print('Option must be a number')
        menu()

    if (op == 1):
        menu_add_account()
    if (op == 2):
        menu_manage_accounts()
    if (op ==0):
        return

menu()