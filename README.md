# spotify-downloader
A project to convert a Spotify playlist or song into an mp3 file

Not included in requirements.txt - program will not actually download anything if FFmpeg is not downloaded onto your device. For correct use of program, you MUST enable FFmpeg.

Programs only tested in macOS - builtin package "os" used, so Windows/Linux devices may not function properly (but probably not).

Only works with Spotify. Only works with mp3. Process of downloading audio includes using [ytmdl]([url](https://github.com/deepjyoti30/ytmdl)) (YouTube).

Before running, change the DOWNLOAD_LOCATION constant in both files to your preference of location. To download playlists, run playlist_downloader.py. To download songs, run song_downloader.py. Run the code in Python3 and follow terminal prompts.


Please enjoy!
