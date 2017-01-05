# artist2pylist v0.0.1
# creates a Spotify playlist based on information from last.fm on the desired artist
# Kamil Krawczyk

from bs4 import BeautifulSoup as parser
import spotipy as spot
import urllib2
import sys

if len(sys.argv) == 2:
    username = sys.argv[1]
    artist = sys.argv[2]
else:
    print "artist2pylist usage:\npython main.py <Spotify username> <Artist>"

# get desired artist from user via terminal; testing with generic artist
# artist = 'Radiohead';

# sanity check
print (username + artist + playlist_id)

# url to Parse
# TODO turn this into a class
url = 'http://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks&artist=' + artist + '&api_key=3a34aadae9198553ffd9123cb8c841e3'

# acquire data
# TODO add error handling
download = urllib2.urlopen(url)
content = download.read()

soup = parser(content, 'html.parser')

# sanity check
print(soup.prettify())

# more sanity checks
print(soup.track)