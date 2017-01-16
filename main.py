# set2pylist v0.0.2
# creates a Spotify playlist based on select artist's most recent setlist on setlist.fm
# Kamil Krawczyk

from bs4 import BeautifulSoup
from set2pylist import UserAuthorizer, createSongList, createPlayList, addToPlaylist
import spotipy
import spotipy.util as util
import requests
import sys

# take system arguments as our artist and user name
if len(sys.argv) >= 3:
    username = sys.argv[1]
    name = ''
    for i in range(2,len(sys.argv)):
        name += sys.argv[i] + ' '
else:
    print('Usage: python main.py <Spotify username> <artist in single quotes>')
    sys.exit()

# part one:
# first thing is to download setlist data
url = 'http://api.setlist.fm/rest/0.1/search/setlists?artistName=' + name

# ensure connection successful
try:
    r = requests.get(url)
except requests.exceptions.RequestException as e:
    print("Error: " + e)
    sys.exit()

# create BeautifulSoup object
soup = BeautifulSoup(r.text, "lxml")

# error breakpoint; terminate if no setlist found
if ('not found' in soup.get_text()):
    print('Error: No setlist found. Please double check your artist name just in case and run again.')
    sys.exit()

# convert most recent setlist to an array w/ track names
recentSetlist = [i.get('name') for i in soup.find('setlist').find_all('song')]
playlist_name = soup.find('setlist').get('eventdate')
playlist_name += ' ' + name

# generate user token
token = UserAuthorizer(username).authorizeToken()

# search spotify for trackid and save in list
tracklist = []
spotify = spotipy.Spotify()
createSongList(tracklist, recentSetlist, token, name, username)

# quit if no songs found
if len(tracklist) == 0:
    print('No tracks found on Spotify, please try a differnet artist.')
    sys.exit()

# part two:
# create playlist, find playlist id, and then add files to it
createPlayList(username,playlist_name,token)

# find playlist ID
authTag = 'Bearer ' + token

try:
    req2 = requests.get('https://api.spotify.com/v1/users/' + username + '/playlists?limit=1', headers={'Authorization':authTag}).json()
except requests.exceptions.RequestException as e:
    print("Error: " + e)
    sys.exit()

# parse JSON object for playlist id
playlist_id = req2['items'][0]['id']

# add to playlist
addToPlaylist(username, playlist_id, tracklist, token)