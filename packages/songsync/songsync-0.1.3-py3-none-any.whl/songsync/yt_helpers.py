"""YouTube helper functions"""
import dataclasses
from ytmusicapi import YTMusic


@dataclasses.dataclass
class YTSong:
    """Class representing a YouTube track"""

    title: str
    artist: str


def get_yt_playlist(playlist_id: str) -> list[YTSong]:
    """fetch and parse playlist from YouTube

    Args:
        playlist_id (str): YouTube playlist ID

    Returns:
        list[YTSong]: list of YouTube tracks
    """
    ytmusic = YTMusic()

    # Max size of a YouTube playlist is 5000
    tracks = ytmusic.get_playlist(playlist_id, limit=5000)["tracks"]

    playlist = []
    for track in tracks:
        title = track["title"]
        artist = track["artists"][0]["name"]
        playlist.append({"title": title, "artist": artist})
    return playlist
