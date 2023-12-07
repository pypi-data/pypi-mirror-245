# songsync

Convert YouTube and YouTube Music playlists to Spotify playlists

## Setup

Install poetry: https://python-poetry.org/docs/#installation

Setup and activate virtual environment

```
python3 -m venv .venv && source .venv/bin/activate
```

Install poetry dependencies

```
poetry install
```

Create a Spotify app by following the instructions in the Spotify Web API documentation: https://developer.spotify.com/documentation/web-api

Set the following environment variables

```
export SPOTIPY_CLIENT_ID='your-spotify-client-id'
export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
export SPOTIPY_REDIRECT_URI='your-app-redirect-url'
```

## Usage

Run the command line script and set `yt_playlist_id` and `spotify_playlist_name` to your YouTube playlist ID and what you'd like to name the Spotify playlist.

Notes:

- The YT playlist ID can be found from the URL of your Youtube/Youtube Music playlist.
- The YT playlist must be public or unlisted.
- The search algorithm uses language detection to search different Spotify markets and substrings of a song title.
  - Titles are more varied for normal YouTube videos in comparison to YouTube Music videos which can increase the difficulty of the search. The closer the YouTube video name is to the Spotify name the easier it is to find. See interactive mode below for manually searching tracks that cannot be found.

Example:

```
./songsync_cmd.sh --yt_playlist_id PLwjEXrvFo-2Bs1-hvfjQ_G61COZ0aBTK5 --spotify_playlist_name "My Playlist"
```

For interactive mode, include the `--interactive` flag.

Example:

```
./songsync_cmd.sh --yt_playlist_id PLwjEXrvFo-2Bs1-hvfjQ_G61COZ0aBTK5 --spotify_playlist_name "My Playlist" --interactive
```

In interactive mode, if the script cannot find the YouTube track on Spotify you will be prompted to manually enter a title and artist. Enter it as it would appear in your country. You can enter blank in the prompt to skip.
