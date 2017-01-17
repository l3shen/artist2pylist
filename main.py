# artist2pylist v0.0.3
# creates a Spotify playlist based on select artist's most recent setlist on setlist.fm
# Kamil Krawczyk

from bs4 import BeautifulSoup
import artist2pylist as a2p
import spotipy
import requests
import sys

# get user details and artist name
if len(sys.argv) >= 3:
    username = sys.argv[1]
    artist = ''
    for i in range(2,len(sys.argv)):
        artist += sys.argv[i] + ' '
else:
    print('Usage: python main.py <Spotify username> <artist in single quotes>')
    sys.exit()

# acquire playlist from setlist.fm
url = 'http://api.setlist.fm/rest/0.1/search/setlists?artistName=' + artist
try:
    r = requests.get(url)
except requests.exceptions.RequestException as error:
    print "Exit with error: " + str(error)
    sys.exit()

# create BeautifulSoup object
soup = BeautifulSoup(r.text, "lxml")

# error breakpoint; terminate if no setlist found
if ('not found' in soup.get_text()):
    print('Error: No setlist found. Please double check your artist name and try again.')
    sys.exit()

# convert most recent setlist to an array w/ track names
recentSetlist = [i.get('name') for i in soup.find('setlist').find_all('song')]
playlist_name = soup.find('setlist').get('eventdate')
playlist_name += ' ' + artist

# generate user token
userAuth = a2p.SpotifyUser(username)
token = userAuth.authorizeToken()

# search spotify for trackid and save in list
tracklist = []
spotify = spotipy.Spotify()

userAuth.createSongList(tracklist, recentSetlist, token, artist)

# quit if no songs found
if len(tracklist) == 0:
    print ('No tracks found on Spotify, please try a differnet artist.')
    sys.exit()

# create playlist
userAuth.createPlayList(playlist_name, token)

# find playlist ID
# find users most recent playlist
authTag = 'Bearer ' + token

try:
    req2 = requests.get('https://api.spotify.com/v1/users/' + username + '/playlists?limit=1', headers={'Authorization':authTag}).json()
except requests.exceptions.RequestException as error:
    print "Exit with error: " + str(error)
    sys.exit()

# parse JSON object for playlist id
# first result is most recent playlist, i.e. the one that was just made above
playlist_id = req2['items'][0]['id']

# add to playlist
userAuth.addToPlaylist(playlist_id, tracklist, token)


