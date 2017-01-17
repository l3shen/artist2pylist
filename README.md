# artist2pylist
Converts most recent setlist of desired artist in to a Spotify playlist.

# Usage
Ensure the following libraries are installed: BeautifulSoup4, lxml, spotipy

In your terminal, run:
```
python main.py <your Spotify username> <artist>
```
This will make a public playlist in your account with the format of ```DD-MM-YYYY + artist name```.

NOTE: When running for the first time, a browser tab will be opened asking you to log in to authenticate the application.
After doing so, copy-paste the URL and paste it in your terminal to continue. This will only occur once.
