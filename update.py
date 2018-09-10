import requests
import os
import sys
from dotenv import load_dotenv
load_dotenv()

LUMEN_API = 'https://' + os.getenv("INSTANCE") + '.akvolumen.org/api/'
DATASET = sys.argv[1]


tokenURI = 'https://login.akvo.org/auth/realms/akvo/protocol/openid-connect/token'
rtData = {
    'client_id':'curl',
    'username': os.getenv("KEYCLOAK_USER"),
    'password': os.getenv("KEYCLOAK_PWD"),
    'grant_type':'password',
    'scope':'openid offline_access'
}

def refreshData():
    tokens = requests.post(tokenURI, rtData).json();
    return tokens['refresh_token']

def getAccessToken():
    account = {
        'client_id':'curl',
        'refresh_token': refreshData(),
        'grant_type':'refresh_token'
    }
    try:
        account = requests.post(tokenURI, account).json();
    except:
        print('FAILED: TOKEN ACCESS UNKNOWN')
        return False
    return account['access_token']

def getResponse(url,rtype):
    header = {
        'Authorization':'Bearer ' + getAccessToken(),
        'Accept': '*/*',
        'User-Agent':'python-requests/2.14.2'
    }
    if rtype == "post":
        response = requests.post(url, headers=header).json()
    else:
        response = requests.get(url, headers=header).json()
    return response

def checkUpdate(url):
    job = getResponse(url, "get")
    if job['status'] == 'OK':
        print('DATASET IS UPDATED...')
        return job['status']
    else:
        print('WAITING...')
        checkUpdate(url)

data = getResponse(LUMEN_API + 'datasets/' + DATASET + '/update', "post")
check = LUMEN_API + "job_executions/" + data['updateId']
checkUpdate(check)
