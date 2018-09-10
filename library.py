import requests
import json
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()

USERNAME = os.getenv("KEYCLOAK_USER")
PASSWORD = os.getenv("KEYCLOAK_PWD")
LUMEN_API = 'https://' + os.getenv("INSTANCE") + '.akvolumen.org/api/'


tokenURI = 'https://login.akvo.org/auth/realms/akvo/protocol/openid-connect/token'
rtData = {
    'client_id':'curl',
    'username': USERNAME,
    'password': PASSWORD,
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

def getResponse(url):
    header = {
        'Authorization':'Bearer ' + getAccessToken(),
        'Accept': '*/*',
        'User-Agent':'python-requests/2.14.2'
    }
    response = requests.get(url, headers=header).json()
    return response


library = getResponse(LUMEN_API + 'library/')
with open('library.json', 'w') as outfile:
    json.dump(library, outfile)
lib_dbs = pd.DataFrame(library['dashboards'])
lib_dbs = lib_dbs.drop(['author'], axis=1)
lib_dts = pd.DataFrame(library['datasets'])
lib_dts = lib_dts.drop(['author'], axis=1)
lib_vis = pd.DataFrame(library['visualisations'])
lib_vis = lib_vis.drop(['author'], axis=1)
lib_col = pd.DataFrame(library['collections'])
lib_dbs.to_csv('lib-database.csv')
lib_dts.to_csv('lib-datasets.csv')
lib_vis.to_csv('lib-visuals.csv')
lib_col.to_csv('lib-collections.csv')

