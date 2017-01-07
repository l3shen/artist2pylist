# set2pylist v0.0.1
# creates a Spotify playlist based on select artist's most recent setlist on setlist.fm
# Kamil Krawczyk

from bs4 import BeautifulSoup
import spotipy
import spotipy.util as util
import requests
import sys
import pprint

# API environmental variables
SPOTIPY_CLIENT_ID='d3d2847c053c4f02bac26015bcff8ebd'
SPOTIPY_CLIENT_SECRET='0795f1b2f3934d599ea2d6c5ecf5d066'

#TODO add input arguments via sys.argv

# part one:
# this part of the code scrapes the relevant data and saves it in an array of song titles

# first thing is to download setlist data
url = 'http://api.setlist.fm/rest/0.1/search/setlists?artistName=phish'
r = requests.get(url)

# create BeautifulSoup object
soup = BeautifulSoup(r.text, "lxml")

# error breakpoint; terminate if error received from setlist.fm
if ('not found' in soup.get_text()):
    print('Error: No setlist found. Please double check your artist name and try again.')
    sys.exit()

# convert most recent setlist to an array w/ track names
recentSetlist = [i.get('name') for i in soup.find('setlist').find_all('song')]
playlist_name = soup.find('setlist').get('eventdate')

#TODO add break for artists that exist but have no setlist

# this took goddamn forever to work, stupid callback URL
username = 'kamdev'
scope = 'user-library-read playlist-modify-public'
name = 'Phish'

# generate user token
token = util.prompt_for_user_token(username, scope, client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri='http://localhost:8888/callback')

# search spotify for trackid and save in list
tracklist = []
spotify = spotipy.Spotify()

if token:
    for track in recentSetlist:
        print 'Adding ' + track + ' by ' + name
        query = spotify.search(q='artist:' + name + ' track:' + track, limit=1, type='track')
        # response handling
        if (query['tracks']['total'] == 0):
            print track + ' could not be added.'
        else:
            tracklist.append(query['tracks']['items'][0]['id'])
            print 'Added successfully.'
else:
    print 'Could not authenticate. Try again, ' + username

# fuuuuuuck me it's a dict with a list with a dict with a list

# part two:
# create playlist, find playlist id, and then add files to it

# works!!!!!!!
if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    playlists = sp.user_playlist_create(username, playlist_name)
    print 'Playlist created: ' + name + ' ' + playlist_name
else:
    print 'Could not authenticate. Try again, ' + username

# find playlist ID
# find users most recent playlist
authTag = 'Bearer ' + token
req2 = requests.get('https://api.spotify.com/v1/users/' + username + '/playlists?limit=1', headers={'Authorization':authTag}).json()

# parse JSON object for playlist id
playlist_id = req2['items'][0]['id']

# add to playlist
if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    results = sp.user_playlist_add_tracks(username, playlist_id, tracklist)
else:
    print("Can't get token for", username)

# IT'S SHIT BUT IT FUCKING WORKS AYYYYYY
