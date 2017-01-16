# set2pylist classes and functions for use in main
# Kamil Krawczyk

import spotipy.util as util
import spotipy

class UserAuthorizer (object):

    """

        Class used for generating and using authentication token.
        API information is valid. Replace with own keys if necessary.
        Abstracted for ease of reading in main code.

    """

    SPOTIPY_CLIENT_ID = 'd3d2847c053c4f02bac26015bcff8ebd'
    SPOTIPY_CLIENT_SECRET = '0795f1b2f3934d599ea2d6c5ecf5d066'
    REDIRECT_URL = 'http://localhost:8888/callback'
    scope = 'user-library-read playlist-modify-public'

    def __init__(self, username):
        self.username = username

    # return boolean token for authentication
    def authorizeToken(self):
         return util.prompt_for_user_token(self.username, self.scope, client_id=self.SPOTIPY_CLIENT_ID, client_secret=self.SPOTIPY_CLIENT_SECRET, redirect_uri=self.REDIRECT_URL)

    def createSongList (self, tracklist, setlist, token, artist):
        """

            Used to create the playlist for the user using the token provided,

        """

        if token:
            for track in setlist:
                print('Adding ' + track + ' by ' + artist)
                query = spotipy.Spotify().search(q='artist:' + artist + ' track:' + track, limit=1, type='track')
                # response handling
                if (query['tracks']['total'] == 0):
                    print(track + ' could not be added.')
                else:
                    tracklist.append(query['tracks']['items'][0]['id'])
                    print('Added successfully.')
        else:
            print('Could not authenticate. Try again, ' + self.username)

    def createPlayList(self, playlist_name, token):
        """

            Creates public playlist in the user's account.

        """
        if token:
            sp = spotipy.Spotify(auth=token)
            sp.trace = False
            playlists = sp.user_playlist_create(self.username, playlist_name)
            print('Playlist created: ' + playlist_name)
        else:
            print('Could not authenticate. Try again, ' + self.username)


def addToPlaylist (username, playlist_id, tracklist, token):

    """

        Add tracks to user's most recently made playlist.

    """

    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        results = sp.user_playlist_add_tracks(username, playlist_id, tracklist)
    else:
        print("Can't get token for", username)