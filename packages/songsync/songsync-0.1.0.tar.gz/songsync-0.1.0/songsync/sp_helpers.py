"""Spotify helper functions"""
import json
from spotipy import Spotify, SpotifyException
from spotipy.oauth2 import SpotifyOAuth
from songsync.lang_helpers import get_country_codes_from_text, split_text_by_language
from songsync.yt_helpers import YTSong


def auth_to_spotify() -> Spotify:
    """authenticate to Spotify

    Returns:
        Spotify: Spotify object
    """
    scope = ",".join(
        [
            "user-read-private",
            "user-read-email",
            "playlist-modify-public",
            "playlist-modify-private",
        ]
    )
    return Spotify(auth_manager=SpotifyOAuth(scope=scope))


def search_spotify_track(
    title: str, artist: str, sp: Spotify, market: str = None
) -> str | None:
    """Search Spotify for a track that matches the queried title and artist

    Args:
        title (str): Spotify track title
        artist (str): Spotify track artist
        sp (Spotify): Spotify object
        market (str, optional): Spotify market, defaults to user's market if None

    Returns:
        str | None: Spotify track uri or None if not found
    """
    query = f"track:{title} artist:{artist}"
    params = {"q": query, "type": "track", "market": market}
    try:
        track_items = sp.search(
            params["q"],
            type=params["type"],
            market=params["market"],
        )["tracks"]["items"]
        if not track_items:
            return None
        return track_items[0]["uri"]
    except SpotifyException as e:
        print(f"❌ Error adding track {e.msg}")
        return None


def search_spotify_track_from_markets(
    title: str, artist: str, sp: Spotify, markets: list[str] = None
) -> str | None:
    """Wrapper for search_spotify_track, return the first result from results in the listed markets

    Args:
        title (str): Spotify track title
        artist (str): Spotify track artist
        sp (Spotify): Spotify object
        markets (list[str], optional): Spotify markets to search

    Returns:
        str | None: First Spotify track uri or None if not found
    """
    if not markets:
        print(f"Searching for {title} - {artist} in the user's market")
        return search_spotify_track(title=title, artist=artist, sp=sp)
    print(f"Searching for {title} - {artist} in the following markets: {markets}")
    for market in markets:
        track_uri = search_spotify_track(
            title=title, artist=artist, sp=sp, market=market
        )
        if track_uri:
            return track_uri


def create_spotify_playlist(
    playlist: list[YTSong], new_playlist_name: str, interactive_mode: bool
):
    """create a Spotify playlist with the given name from a YouTube playlist

    Args:
        playlist (list[YTSong]): YouTube playlist to convert to Spotify
        new_playlist_name (str): Spotify playlist name to be created
        interactive_mode (bool): If true, support manually adding songs that can't be found
    """
    sp = auth_to_spotify()
    sp_user_id = sp.current_user()["id"]

    new_playlist_id = sp.user_playlist_create(
        sp_user_id, new_playlist_name, public=False
    )["id"]

    uris_to_add = []
    tracks_not_found = []

    for index, track in enumerate(playlist):
        title, artist = track["title"], track["artist"]
        title_substrings = split_text_by_language(title)
        titles_to_check = [title] + title_substrings
        for title_to_check in titles_to_check:
            markets = list(
                get_country_codes_from_text(title_to_check)
                | get_country_codes_from_text(title_to_check)
            )
            track_uri = search_spotify_track_from_markets(
                title_to_check, artist, sp, markets
            )
            if track_uri:
                break
        while not track_uri and interactive_mode:
            user_input = input(
                f"❌ ({index+1}/{len(playlist)}) Unable to find [title] {title} [artist] {artist}\nPlease enter a title and artist comma-separated as it would appear in Spotify US to search again (or enter blank to skip): "
            )
            if not user_input:
                print("Skipping.")
                break
            user_input_parts = user_input.split(",", 1)
            if len(user_input_parts) != 2:
                print("Could not parse input.")
                continue
            title, artist = user_input_parts[0], user_input_parts[1]
            track_uri = search_spotify_track_from_markets(title, artist, sp, markets)
        if track_uri:
            print(
                f"✅ ({index+1}/{len(playlist)}) Found {title} - {artist}: {track_uri}"
            )
            uris_to_add.append(track_uri)
        else:
            print(f"❌ ({index+1}/{len(playlist)}) Not Found {title} - {artist}")
            tracks_not_found.append(f"{title} - {artist}")

    # Spotify only allows adding 100 tracks per request, iterate in chunks of 100
    step_count = 100
    for index in range(0, len(uris_to_add), step_count):
        end = (
            index + step_count
            if index + step_count <= len(uris_to_add)
            else len(uris_to_add)
        )
        sp.user_playlist_add_tracks(sp_user_id, new_playlist_id, uris_to_add[index:end])
    if tracks_not_found:
        print(
            "❌ Could not find the following tracks",
            json.dumps(tracks_not_found, indent=4, ensure_ascii=False),
        )
    print(f"🎉 Created new Spotify playlist {new_playlist_name}")
