import requests
import json

def getPlaylists(user_id):
    AUTH_URL = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': '64d88f30bd6e47d5a99e11985fdd0bdb',
        'client_secret': 'aa57afecfba4466bb0caeae430352b4c',})
    auth_response_data = auth_response.json()
    access_token = auth_response_data['access_token']
    headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}
    BASE_URL = 'https://api.spotify.com/v1/users/'
    # header = spotifyLogin.auth_head
    response = requests.get(BASE_URL + user_id + '/playlists', headers = headers)
    playlists = response.json()
    # add parsing here
    x = json.dumps(playlists)
    y = json.loads(x)
    length = len(y['items'])
    uris = []
    for i in range(length):
        uriall = y['items'][i]['uri']
        uri = uriall.split(':')[2]
        uris.append(uri)
    return(uris)


def getSongInLists(playlist_id):
    AUTH_URL = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': '64d88f30bd6e47d5a99e11985fdd0bdb',
        'client_secret': 'aa57afecfba4466bb0caeae430352b4c',})
    auth_response_data = auth_response.json()
    access_token = auth_response_data['access_token']
    headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}
    BASE_URL = 'https://api.spotify.com/v1/playlists/'
    songs = []
    for id in playlist_id:
        response = requests.get(BASE_URL + id + '/tracks', headers = headers) 
        raw = response.json()
        # add parsing here
        x = json.dumps(raw)
        y = json.loads(x)
        length = len(y['items'])
        for i in range(length):
            songall = y['items'][i]['track']['uri']
            song = songall.split(':')[2]
            songs.append(song)
    return(songs)


def getArtistInLists(playlist_id):
    AUTH_URL = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': '64d88f30bd6e47d5a99e11985fdd0bdb',
        'client_secret': 'aa57afecfba4466bb0caeae430352b4c',})
    auth_response_data = auth_response.json()
    access_token = auth_response_data['access_token']
    headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}
    BASE_URL = 'https://api.spotify.com/v1/playlists/'
    artists = []
    for id in playlist_id:
        response = requests.get(BASE_URL + id + '/tracks', headers = headers) 
        raw = response.json()
        # add parsing here
        x = json.dumps(raw)
        y = json.loads(x)
        length = len(y['items'])
        for i in range(length):
            artistall = y['items'][i]['track']['artists'][0]['uri']
            artist = artistall.split(':')[2]
            artists.append(artist)
    return(artists)


def jointPlaylistV1(user1,user2):
    user1ids = getPlaylists(user1)
    user2ids = getPlaylists(user2)
    user1songs = getSongInLists(user1ids)
    user2songs = getSongInLists(user2ids)
    joint = list(set(user1songs).intersection(user2songs))
    return joint

def jointPlaylistV2(user1,user2):
    user1ids = getPlaylists(user1)
    user2ids = getPlaylists(user2)
    user1songs = getSongInLists(user1ids)
    user2songs = getSongInLists(user2ids)
    user1artist = getArtistInLists(user1ids)
    user2artist = getArtistInLists(user2ids)
    jointartist = list(set(user1artist).intersection(user2artist))
    joint = []
    for i in jointartist:
        joint.append(user1songs[user1artist.index(i)])
        joint.append(user2songs[user2artist.index(i)])
    return joint