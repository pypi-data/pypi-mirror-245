"""Module converting YouTube playlists to Spotify playlists"""
from songsync import yt_helpers, sp_helpers


class SongSync:
    """YT and Spotify converter"""

    def __init__(self, interactive_mode=False) -> None:
        self.interactive_mode = interactive_mode

    def convert_yt_spotify(
        self, yt_playlist_id: str, spotify_playlist_name: str
    ) -> None:
        """convert YT playlist to Spotify playlist

        Args:
            yt_playlist_id (str): YouTube playlist ID
            spotify_playlist_name (str): Spotify playlist name
        """
        yt_playlist = yt_helpers.get_yt_playlist(playlist_id=yt_playlist_id)

        sp_helpers.create_spotify_playlist(
            playlist=yt_playlist,
            new_playlist_name=spotify_playlist_name,
            interactive_mode=self.interactive_mode,
        )
