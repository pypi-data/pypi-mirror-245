"""Module converting YouTube playlists to Spotify playlists"""
from songsync import yt_helpers, sp_helpers


class SongSync:
    """YT and Spotify converter"""

    def __init__(self, interactive_mode=False) -> None:
        self.interactive_mode = interactive_mode

    def convert_yt_spotify(
        self, yt_playlist_id: str, spotify_playlist_name: str
    ) -> (str, list[str]):
        """convert YT playlist to Spotify playlist

        Args:
            yt_playlist_id (str): YouTube playlist ID
            spotify_playlist_name (str): Spotify playlist name

        Returns:
            str: id of created Spotify playlist
            list[str]: tracks not found
        """
        yt_playlist = yt_helpers.get_yt_playlist(playlist_id=yt_playlist_id)

        spotify_playlist_id, tracks_not_found = sp_helpers.create_spotify_playlist(
            playlist=yt_playlist,
            new_playlist_name=spotify_playlist_name,
            interactive_mode=self.interactive_mode,
        )
        return spotify_playlist_id, tracks_not_found
