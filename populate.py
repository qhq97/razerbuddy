import requests
from requests.auth import HTTPBasicAuth

import json # Just to print nice nice json response
import uuid # Generate unique id

import random
import json

username = 'Team95'
password = 'passC7E8FDEF5'

url = 'https://razerhackathon.sandbox.mambu.com/api/'

#NESTED dictionary of name(key) and accoundID(value)
accountID_dict = {}




def populateBank(branchKey):
    names = [chr(x) for x in range(ord('A'), ord('Z') + 1)]
    for name in names:
        createClient(name,branchKey)
        print(name)

def createClient(name,branchKey):
    payload = {
    "client": {
        "firstName": name,
        "lastName": " ",
        "preferredLanguage": "ENGLISH",
        "notes": "Enjoys playing RPG",
        "assignedBranchKey": branchKey # From 1.2
        },
    "idDocuments": [{
        "identificationDocumentTemplateKey": "8a8e867271bd280c0171bf7e4ec71b01",
        "issuingAuthority": "Immigration Authority of Singapore",
        "documentType": "NRIC/Passport Number",
        "validUntil": "2021-09-12",
        "documentId": "S9812345A"
        }],
    "addresses": [],
    "customInformation": [
        {
            "value":"Singapore",
            "customFieldID":"countryOfBirth"
        },
        {
            "value": str(uuid.uuid4()), #Generate unique id
            "customFieldID":"razerID"
            }
        ]
    }
    r = requests.post(url + 'clients', auth=HTTPBasicAuth(username, password), json=payload)
    print(json.dumps(r.json(), indent=2))
    clientID = r.json()['client']['encodedKey']

    #creation of saving account under client with deposit
    accountID = createSavingAccount(name,clientID)

    #creation of expense account PLUS transactions with saving account
    createExpenseAccount(clientID, accountID)
    

def createSavingAccount(name,clientID):
    payload = {
    "savingsAccount": {
        "name": "Saving",
        "accountHolderType": "CLIENT",
        "accountHolderKey": clientID,
        "accountState": "APPROVED",
        "productTypeKey": "8a8e878471bf59cf0171bf6979700440",
        "accountType": "CURRENT_ACCOUNT",
        "currencyCode": "SGD",
        "allowOverdraft": "true",
        "overdraftLimit": "100",
        "overdraftInterestSettings": {
            "interestRate": 5
            },
        "interestSettings": {
            "interestRate": "1.25"
            }
        }
    }
    r = requests.post(url + 'savings', auth=HTTPBasicAuth(username, password), json=payload)
    print(json.dumps(r.json(), indent=2))
    accountID = r.json()['savingsAccount']['id']

    #save to dictionary the savingaccountID
    accountID_dict.update({name:accountID})

    #create random age group and preferred language
    age = randomAge()
    lang = randomLang()
    deposit_comment = str(age) + ',' + lang
    
    #make initial deposit
    payload ={
        "amount": 4000,
        "notes": deposit_comment,
        "type": "DEPOSIT",
        "method": "bank",
        "customInformation": [
            {
                "value": "unique identifier for receipt",
                "customFieldID": "IDENTIFIER_TRANSACTION_CHANNEL_I"
            }
        ]
    }
    
    r = requests.post(url + 'savings/'+ accountID + '/transactions', auth=HTTPBasicAuth(username, password), json=payload)
    print(json.dumps(r.json(), indent=2))
    return accountID


def createExpenseAccount(clientID, accountID):
    payload = {
    "savingsAccount": {
        "name": "Expense",
        "accountHolderType": "CLIENT",
        "accountHolderKey": clientID,
        "accountState": "APPROVED",
        "productTypeKey": "8a8e878471bf59cf0171bf6979700440",
        "accountType": "CURRENT_ACCOUNT",
        "currencyCode": "SGD",
        "allowOverdraft": "true",
        "overdraftLimit": "100",
        "overdraftInterestSettings": {
            "interestRate": 5
            },
        "interestSettings": {
            "interestRate": "1.25"
            }
        }
    }
    r = requests.post(url + 'savings', auth=HTTPBasicAuth(username, password), json=payload)
    print(json.dumps(r.json(), indent=2))
    addtionalAccountID = r.json()['savingsAccount']['id']

    categories = ["FNB","ENTERTAINMENT","SHOPPING","TRANSPORATION"]

    for expense_type in categories:
        expense_amt = randomExpense()    
        payload={
        "type": "TRANSFER",
        "amount": expense_amt,
        "notes": expense_type,
        "toSavingsAccount": addtionalAccountID,
        "method":"bank"
        }
        r = requests.post(url + 'savings/'+ accountID + '/transactions', auth=HTTPBasicAuth(username, password), json=payload)
        print(json.dumps(r.json(), indent=2))
        
    """expAccounts = ["FNB","ENTERTAINMENT","SHOPPING","TRANSPORATION"]
    for acc_name in expAccounts:
        createExpAccount(acc_name,clientID)""" 

    

def randomAge():
    return random.randint(15,35)

def randomLang():
    num = random.randint(1,100)
    if num<=60:
        return 'E'
    elif num<=90:
        return 'C'
    else:
        return 'M'

def randomExpense():
    return str(random.randint(0,900))





#main code

r = requests.get(url + 'branches/' + username, auth=HTTPBasicAuth(username, password))
print(json.dumps(r.json(), indent=2))
branchKey = r.json()['encodedKey']

populateBank(branchKey)

print(accountID_dict)

json = json.dumps(accountID_dict)
f = open("dict.json","w")
f.write(json)
f.close()   






    


