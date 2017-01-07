# set2pylist v0.0.1
# creates a Spotify playlist based on select artist's most recent setlist on setlist.fm
# Kamil Krawczyk

from bs4 import BeautifulSoup
import spotipy
import spotipy.util as util
import requests
import sys
import pprint
from collections import defaultdict

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

# this took goddamn forever to work, stupid callback URL
username = 'kamdev'
playlist_id = '35vTgBktjPHNLbNCUkyMCA'
track_id = '7eKd41R7nInfUmh3iv7JjL'
scope = 'user-library-read'
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

for values in tracklist:
    print values

# fuuuuuuck me it's a dict with a list with a dict with a list