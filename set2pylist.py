# set2pylist classes
# Kamil Krawczyk

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

    def authorizeToken(self):
         return util.prompt_for_user_token(self.username, self.scope, client_id=self.SPOTIPY_CLIENT_ID, client_secret=self.SPOTIPY_CLIENT_SECRET, redirect_uri=self.REDIRECT_URL)

