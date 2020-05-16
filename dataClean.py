import requests
from requests.auth import HTTPBasicAuth
import json
import random

username = 'Team95'
password = 'passC7E8FDEF5'

url = 'https://razerhackathon.sandbox.mambu.com/api/'

dataCleaned = []

def getProfile(accountId):
    r = requests.get(url + 'savings/' + accountId + '/transactions',
                     auth=HTTPBasicAuth(username, password))
    # print(r.json())
    spending_habits = {}
    profile = []
    total_transaction_amount = 0
    level_1 = 300
    level_2 = 600
    level_3 = 900
    for transaction in r.json():
        if (transaction['type'] == 'DEPOSIT'):
            split_txt = transaction['comment'].split(",")
            profile.append(int(split_txt[0]))
            profile.append(split_txt[1])
        if (transaction['type'] == 'TRANSFER'):
            total_transaction_amount += int(transaction['fundsAmount'])
            if (transaction['comment'] == 'SHOPPING'):
                if (int(transaction['fundsAmount']) < level_1):
                    spending_habits['SHOPPING'] = 1
                elif (int(transaction['fundsAmount']) < level_2):
                    spending_habits['SHOPPING'] = 2
                elif (int(transaction['fundsAmount']) <= level_3):
                    spending_habits['SHOPPING'] = 3
            elif (transaction['comment'] == 'ENTERTAINMENT'):
                if (int(transaction['fundsAmount']) < level_1):
                    spending_habits['ENTERTAINMENT'] = 1
                elif (int(transaction['fundsAmount']) < level_2):
                    spending_habits['ENTERTAINMENT'] = 2
                elif (int(transaction['fundsAmount']) <= level_3):
                    spending_habits['ENTERTAINMENT'] = 3
            elif (transaction['comment'] == 'TRANSPORATION'):
                if (int(transaction['fundsAmount']) < level_1):
                    spending_habits['TRANSPORATION'] = 1
                elif (int(transaction['fundsAmount']) < level_2):
                    spending_habits['TRANSPORATION'] = 2
                elif (int(transaction['fundsAmount']) <= level_3):
                    spending_habits['TRANSPORATION'] = 3
            elif (transaction['comment'] == 'FNB'):
                if (int(transaction['fundsAmount']) < level_1):
                    spending_habits['FNB'] = 1
                elif (int(transaction['fundsAmount']) < level_2):
                    spending_habits['FNB'] = 2
                elif (int(transaction['fundsAmount']) <= level_3):
                    spending_habits['FNB'] = 3
    
    profile.append(total_transaction_amount)
    profile.append(spending_habits)
    # print(profile)
    return profile

def activity(original_list):
    selected_cust_list = random.sample(list(original_list), 10)
    # print(selected_cust_list)
    for selected_cust in selected_cust_list:
        full_profile = []
        full_profile = getProfile(original_list[selected_cust])
        full_profile.insert(0,selected_cust)
        # print(full_profile)
        dataCleaned.append(full_profile)

def get_profiles():
    # main code
    with open('dict.json') as f:
      client_list = json.load(f)

    activity(client_list)
    return dataCleaned
    # print(dataCleaned)

