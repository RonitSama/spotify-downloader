from bs4 import BeautifulSoup
import requests
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
import os
import sys


# Spotify Authorization
SPOTIFY_CLIENT_ID = '326b7afeb0d64682a562bd5a7200563f'
SPOTIFY_CLIENT_SECRET = '7457c81127fa4a548d3f8e1dbd2f4108'

DOWNLOAD_LOCATION = '''PATH/TO/SONGS/LOCATION'''

playlist_id = input('Playlist Link/ID (Desktop only):  ')

# extract ID from link
try:
    if 'spotify' in playlist_id:
        playlist_id = playlist_id[playlist_id.index(
            'open.spotify.com/playlist/')+len('open.spotify.com/playlist/'):]
    if '?si=' in playlist_id:
        playlist_id = playlist_id[:playlist_id.index('?si=')]
except ValueError as expt:
    print(f'\nInvalid playlist: {playlist_id}')
    sys.exit(1)

# connect to Spotify playlist
client_credentials_manager = SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
sp = Spotify(client_credentials_manager=client_credentials_manager)
results = sp.playlist_tracks(playlist_id)

# gather all songs in playlist
songs = list(results['items'])
while results['next']:
    results = sp.next(results)
    songs.extend(results['items'])

# loop every song
for song in songs:
    '''
    For each song, process is as follows:
    1) extract information from saved list of songs
    2) search YouTube for video
    3) Download from YouTube
    4) Extract metadata from Spotify and apply to .mp3 file
    '''

    # unusual glitch handling
    if not song['track']:
        continue

    search_url = 'https://www.google.com/search?q={search_q}+lyric+video&oq={search_q}+lyric+video&aqs=chrome.0.69i59j35i39i650l2j46i67i650j0i67i650j69i60l2j69i61.552j0j7&sourceid=chrome&ie=UTF-8'

    # save song name and artist
    spotify_id = str(song['track']['id']).replace('&', r'\&').replace("'", r"\'")
    song_name = str(song['track']['name'])
    artist = str(song['track']['artists'][0]['name'])

    # print song to console
    print(f'{song_name} - {artist}')
    song_name = song_name.replace('&', r'\&').replace("'", r"\'")
    artist = artist.replace('&', r'\&').replace("'", r"\'")

    # find youtube link
    response = requests.get(search_url.replace(
        '{search_q}',
        f'{song_name.replace(" ", "+")}+{artist.replace(" ", "+")}'))
    response.raise_for_status()
    webpage = BeautifulSoup(response.text, 'html.parser')
    links = webpage.select('a')
    for link in links:
        if 'https://www.youtube.com/watch' in str(link.get('href')):
            search_url = f"https://www.youtube.com/watch?v={link.get('href')[link.get('href').index('https://www.youtube.com/watch%3Fv%3D')+len('https://www.youtube.com/watch%3Fv%3D'):link.get('href').index('&')]}"
            skip = False
            break
        else:
            skip = True

    if skip:
        print('Something went wrong finding a video. Skipping song...')
        continue

    # download
    os.system(f"ytmdl -o {DOWNLOAD_LOCATION} --url '{search_url}' "
              f"--spotify-id {spotify_id} {song_name}")
