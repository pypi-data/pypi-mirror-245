# songsync

Convert YouTube and YouTube Music playlists to Spotify playlists

## Installation

`pip install songsync`

## Setup

Create a Spotify app by following the instructions in the Spotify Web API documentation: https://developer.spotify.com/documentation/web-api

Set the following environment variables

```
export SPOTIPY_CLIENT_ID='your-spotify-client-id'
export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
export SPOTIPY_REDIRECT_URI='your-app-redirect-url'
```

## Usage

```python
from songsync.songsync import SongSync

ss = SongSync()
ss.convert_yt_spotify(
    yt_playlist_id="PLkZa6xWYS81W6wdF6HSpuqOuVCgu9mzjD",
    spotify_playlist_name="Your Spotify Playlist Name",
)
```

Notes:

- The YT playlist ID can be found from the URL of your Youtube/Youtube Music playlist.
- The YT playlist must be public or unlisted.
- (Experimental) The search algorithm uses language detection to search different Spotify markets and substrings of a song title.
  - Titles are more varied for normal YouTube videos in comparison to YouTube Music videos which can increase the difficulty of the search. The closer the YouTube video name is to the Spotify name the easier it is to find. See interactive mode below for manually searching tracks that cannot be found.

### Interactive Mode

```python
ss = SongSync(interactive_mode=True)
```

With interactive mode, if the script cannot find the YouTube track on Spotify you will be prompted to manually enter a title and artist. Enter it as it would appear in your country. You can enter blank in the prompt to skip.

## Local Development

Install poetry: https://python-poetry.org/docs/#installation

Setup and activate virtual environment

```
python3 -m venv .venv && source .venv/bin/activate
```

Install poetry dependencies

```
poetry install
```

Follow the above instructions for setting up your Spotify app and environment variables.
