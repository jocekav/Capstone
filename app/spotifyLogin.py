import requests
import json
from flask import Blueprint, render_template, request, redirect, url_for

##server side
# CLIENT_ID = "64d88f30bd6e47d5a99e11985fdd0bdb"
CLIENT_ID = "374000479f0d47348edf19d25d8fe52c"
# CLIENT_SECRET = "aa57afecfba4466bb0caeae430352b4c"
CLIENT_SECRET = "83cd59ea8f2949ddb6860e216f707319"
PORT = "5000"
CLIENT_URL = "http://127.0.0.1"
REDIRECT_URI = "{}:{}/profile".format(CLIENT_URL, PORT)
# REDIRECT_URI = "http://127.0.0.1:5000/"
SCOPE = "user-modify-playback-state user-read-recently-played streaming user-read-currently-playing user-read-playback-state user-read-email user-read-private playlist-modify-public"
TOKEN_DATA = []

##spotify parameters
SPOTIFY_URL_AUTH = 'https://accounts.spotify.com/authorize/?'
SPOTIFY_URL_TOKEN = 'https://accounts.spotify.com/api/token'
RESPONSE_TYPE = 'code'   
HEADER = 'application/x-www-form-urlencoded'
REFRESH_TOKEN = ''


def getAuth():
    return "{}client_id={}&response_type={}&redirect_uri={}&scope={}".format(SPOTIFY_URL_AUTH, CLIENT_ID, RESPONSE_TYPE, REDIRECT_URI, SCOPE) 

def getUserToken(authCode):
    global TOKEN_DATA
    body = {
        "grant_type": "authorization_code",
        "code": str(authCode),
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }

    postRequest = requests.post(SPOTIFY_URL_TOKEN, data=body)
    response = json.loads(postRequest.text)
    TOKEN_DATA = handleToken(response)
    return TOKEN_DATA

def refreshToken(time):
    time.sleep(time)
    body = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN
    }
    postRefresh = requests.post(SPOTIFY_URL_TOKEN, data=body)
    response = json.dumps(postRefresh.text)
    TOKEN_DATA = handleToken(response)
    return TOKEN_DATA

def handleToken(response):
    global auth_head
    auth_head = {'Accept': 'application/json',
                'Content-Type': 'application/json', 
                "Authorization": "Bearer {}".format(response["access_token"])}
    REFRESH_TOKEN = response["refresh_token"]
    return [response["access_token"], auth_head, response["scope"], response["expires_in"]]

def getAccessToken():
    return TOKEN_DATA

def getUserID(token):
    url = "https://api.spotify.com/v1/me"
    headers = {"Authorization": 'Bearer {token}'.format(token=token),
                "Content-Type": "application/json"}
    resp = requests.get(url, headers=headers)
    print("this " + str(resp))
    resp = resp.json()
    return resp['id']
    