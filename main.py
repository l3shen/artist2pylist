# artist2pylist v0.0.1
# creates a Spotify playlist based on information from last.fm on the desired artist
# Kamil Krawczyk

from bs4 import BeautifulSoup as parser
import spotipy as spot
import spotipy.util as spotutil
from urllib2 import urlopen
import sys

if len(sys.argv) == 3:
    username = sys.argv[1]
    artist = sys.argv[2]
    playlistName = sys.argv[3]
else:
    print "artist2pylist usage:\npython main.py <Spotify username> <Artist> <Playlist Name>"
    sys.exit()

# create playlist
userToken = spotutil.prompt_for_user_token(username)

if userToken:
    sptfy = spot.Spotify(auth=userToken)
    sptfy.trace = False
    playlists = sptfy.user_playlist_create(username, playlistName)
else:
    print("Error, cannot authenticate for user " + username + ", please double check username.")

# url to Parse
artist = 'Radiohead'
# TODO make a class to pull desired artist URL
url = 'http://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks&artist=' + artist + '&api_key=3a34aadae9198553ffd9123cb8c841e3'

# acquire data
# TODO add error handling for download, does not need to be async

# download link data from XML
# create BS object
soup = parser(urlopen(url), "lxml")

topTracks = soup.find_all('track')
playlistContent = []

# iterate through all the top tracks and add to an array
for tracks in topTracks:
    item = tracks.contents[0]
    playlistContent.append(item.text.encode("utf-8"))

# sanity check
print playlistContent

# add tracks to playlist
scope = 'playlist-modify-public'
userToken = spotutil.prompt_for_user_token(username, scope)






