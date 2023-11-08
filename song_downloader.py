import json
from bs4 import BeautifulSoup
import requests
import os

DOWNLOAD_LOCATION = '''PATH/TO/MP3/LOCATION'''

song_id = input('Song Link/ID (Desktop only):  ')
song_link = song_id

if 'open.spotify.com' not in song_link:
    song_link = 'https://open.spotify.com/track/' + song_link

# access link
response = requests.get(song_link)
response.raise_for_status()
page = BeautifulSoup(response.text, 'html.parser')
info: dict[str, str | dict] = json.loads(page.find('script', {'type': 'application/ld+json'}).text)

search_url = 'https://www.google.com/search?q={search_q}+lyric+video&oq={search_q}+lyric+video&aqs=chrome.0.69i59j35i39i650l2j46i67i650j0i67i650j69i60l2j69i61.552j0j7&sourceid=chrome&ie=UTF-8'

# save song name and artist(s)
song_name: str = info['name']
artists: str = info['description'].split('on Spotify. ')[1].split(' ·')[0].strip()

# print song to console
print(f'{song_name} - {artists}')
song_name = song_name.replace('&', r'\&').replace("'", r"\'")
artists = artists.replace('&', r'\&').replace("'", r"\'")

# find youtube link
response = requests.get(search_url.replace(
    '{search_q}',
    f'{song_name.replace(" ", "+")}+{artists.replace(" ", "+")}'))
response.raise_for_status()
webpage = BeautifulSoup(response.text, 'html.parser')
links = webpage.select('a')
for link in links:
    if 'https://www.youtube.com/watch' in str(link.get('href')):
        try:
            search_url = f"https://www.youtube.com/watch?v={link.get('href')[link.get('href').index('https://www.youtube.com/watch%3Fv%3D')+len('https://www.youtube.com/watch%3Fv%3D'):link.get('href').index('&')]}"
        except ValueError:
            search_url = f"https://www.youtube.com/watch?v={link.get('href')[link.get('href').index('https://www.youtube.com/watch?v=')+len('https://www.youtube.com/watch?v='):]}"
        break

# download
os.system(f"ytmdl -o {DOWNLOAD_LOCATION} --url '{search_url}' "
            f"--spotify-id {song_id} '{song_name}'")
