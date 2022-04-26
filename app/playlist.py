from posixpath import join
import requests
import json
import numpy as np
from flask import jsonify

def getPlaylists(user_id, token):
    headers = {'Authorization': 'Bearer {token}'.format(token=token)}
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


def getSongInLists(playlist_id, token):
    headers = {'Authorization': 'Bearer {token}'.format(token=token)}
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


def getArtistInLists(playlist_id, token):
    headers = {'Authorization': 'Bearer {token}'.format(token=token)}
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

def getArtistGenre(artist_id, token):
    headers = {'Authorization': 'Bearer {token}'.format(token=token)}
    BASE_URL = 'https://api.spotify.com/v1/artists/'
    genres = []
    for id in artist_id:
        response = requests.get(BASE_URL + id, headers = headers) 
        raw = response.json()
        genre = raw['genres']
        genres = genres + genre
    return genres

def jointPlaylistV1(user1_songfile, user2_songfile):
    my_file = open(user1_songfile, "r")
    user1_songs = my_file.read()
    user1_songs = user1_songs.split("\n")[:-1]

    my_file.close()

    my_file = open(user2_songfile, "r")
    user2_songs = my_file.read()
    user2_songs = user2_songs.split("\n")[:-1]
    my_file.close()

    joint_playlist = list(set(user1_songs).intersection(user2_songs))
    return joint_playlist

def jointPlaylistV2(user1_songfile, user2_songfile, user1_artistfile, user2_artistfile):
    my_file = open(user1_songfile, "r")
    user1_songs = my_file.read()
    user1_songs = user1_songs.split("\n")[:-1]
    my_file.close()

    my_file = open(user1_artistfile, "r")
    user1_artists = my_file.read()
    user1_artists = user1_artists.split("\n")[:-1]
    my_file.close()

    my_file = open(user2_songfile, "r")
    user2_songs = my_file.read()
    user2_songs = user2_songs.split("\n")[:-1]
    my_file.close()

    my_file = open(user2_artistfile, "r")
    user2_artists = my_file.read()
    user2_artists = user2_artists.split("\n")[:-1]
    my_file.close()

    jointartist = list(set(user1_artists).intersection(user2_artists))
    joint_playlist = []
    for i in jointartist:
        joint_playlist.append(user1_songs[user1_artists.index(i)])
        joint_playlist.append(user2_songs[user2_artists.index(i)])
    return joint_playlist

def jointPlaylistV3(user1_genrefile, user2_genrefile):

    my_file = open(user1_genrefile, "r")
    user1_genres = my_file.read()
    user1_genres = user1_genres.split("\n")[:-1]
    my_file.close()
    
    my_file = open(user2_genrefile, "r")
    user2_genres = my_file.read()
    user2_genres = user2_genres.split("\n")[:-1]
    my_file.close()

    jointgenre = list(set(user1_genres).intersection(user2_genres))
    # display message: You both like these genres: jointgenre
    return jointgenre

def matchsummary(user1_songfile, user2_songfile, user1_artistfile, user2_artistfile, user1_genrefile, user2_genrefile):
    v1 = len(jointPlaylistV1(user1_songfile, user2_songfile))
    v2 = len(jointPlaylistV2(user1_songfile, user2_songfile, user1_artistfile, user2_artistfile))
    v3 = len(jointPlaylistV3(user1_genrefile, user2_genrefile))

    my_file = open(user1_songfile, "r")
    user1_songs = my_file.read()
    user1_songs = user1_songs.split("\n")[:-1]
    song1 = len(user1_songs)
    my_file.close()

    my_file = open(user2_songfile, "r")
    user2_songs = my_file.read()
    user2_songs = user2_songs.split("\n")[:-1]
    song2 = len(user2_songs)
    my_file.close()

    my_file = open(user1_artistfile, "r")
    user1_artists = my_file.read()
    user1_artists = user1_artists.split("\n")[:-1]
    artist1 = len(user1_artists)
    my_file.close()

    my_file = open(user2_artistfile, "r")
    user2_artists = my_file.read()
    user2_artists = user2_artists.split("\n")[:-1]
    artist2 = len(user2_artists)
    my_file.close()

    my_file = open(user1_genrefile, "r")
    user1_genres = my_file.read()
    user1_genres = user1_genres.split("\n")[:-1]
    genre1 = len(user1_genres)
    my_file.close()
    
    my_file = open(user2_genrefile, "r")
    user2_genres = my_file.read()
    user2_genres = user2_genres.split("\n")[:-1]
    genre2 = len(user2_genres)
    my_file.close()

    score1 = v1 / song1 + v2 / artist1 + v3 / genre1
    score2 = v1 / song2 + v2 / artist2 + v3 / genre2
    score = (score1 + score2) /2
    return score

def jointPlaylist(user1,user2):

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

def create_playlist(token, user_id, other_user, song_uris):
    headers = {'Authorization': 'Bearer {token}'.format(token=token),
            'Content-Type': 'application/json'}
    BASE_URL = 'https://api.spotify.com/v1/users/'

    data = '{"name": "HeartBeats Playlist with ' + other_user + '", "description": "HeartBeats Playlist with ' + other_user + '"}'

    response = requests.post(BASE_URL + user_id + '/playlists', headers=headers, data=data)
    raw = response.json()
    playlist_id = raw['id']

    data = '{ "uris": ' + str(song_uris) + '}'
    data = data.replace('\'', '"')
    BASE_URL = 'https://api.spotify.com/v1/playlists/'
    response = requests.post(BASE_URL + playlist_id + '/tracks', headers=headers, data=data)
    return playlist_id

def getSongInfo(token, uri):
    SPOTIFY_URL_TRACK = "https://api.spotify.com/v1/tracks/"
    header = {'Accept': 'application/json',
                'Content-Type': 'application/json', 
                "Authorization": "Bearer {}".format(token)}
    id = uri.split(':')[2]
    response = requests.get(SPOTIFY_URL_TRACK+id, headers=header)
    resp = response.json()
    art = resp['album']['images'][0]['url']
    duration = resp['duration_ms']
    title = resp['name']
    # return [title, duration, art]
    return title