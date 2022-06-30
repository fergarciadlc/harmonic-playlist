import logging
import urllib
from dataclasses import dataclass, field
from typing import Dict, List

from spotify import Client, Track, User
from spotify.endpoints import (
    url_add_items_to_playlist,
    url_audio_features_several_tracks,
    url_create_playlist,
    url_recommendations,
)
from spotify.harmony import Tonality

@dataclass
class HarmonicPlaylist:
    client: Client
    reference_track: Track
    tracks: List[Track] = field(default_factory=list)

    def generate(self, hard_filter: bool = True) -> None:
        """Generate sequence of tracks based on tonality from reference track.

        Args:
            hard_filter (bool, optional): If True, will filter only tracks 
                with same tonality or relative. Defaults to True.
        """
        # TODO: Refactor this
        natural_tracks = self._get_recommendations_by_tone(kind="natural")
        natural_tracks = self._batch_audio_features_for_tracks(natural_tracks)
        relative_tracks = self._get_recommendations_by_tone(kind="relative")
        relative_tracks = self._batch_audio_features_for_tracks(relative_tracks)

        if hard_filter:
            natural_tracks = self._filter_by_tone_or_relative(natural_tracks)
            relative_tracks = self._filter_by_tone_or_relative(relative_tracks)
        self.tracks = self.tracks + natural_tracks + relative_tracks
        self.tracks.insert(0, self.reference_track)

    def export_playlist(self, user: User) -> None:
        """Export playlist into user's profile.

        Args:
            user (User): Generic user class
        """
        playlist_id = self._create_playlist(
            user=user,
            description=(
                "Harmonic playlist for "
                f"{self.reference_track.name} by {self.reference_track.artists} "
                f"in {self.reference_track.tonality.key_signature}"
            ),
        )
        self._add_tracks_to_playlist(playlist_id=playlist_id)
        logging.info(f"{len(self.tracks)} tracks exported to playlist")

    def _add_tracks_to_playlist(self, playlist_id: str, position: int = 0) -> None:
        """Add tracks to playlist

        Args:
            playlist_id (str): Playlist id.
            position (int, optional): The position to insert the items, a zero-based index 
                For example, to insert the items in the first position: position=0; 
                to insert the items in the third position: position=2. Defaults to 0.
        """
        url = url_add_items_to_playlist.format(playlist_id=playlist_id)
        json_body = {"position": position, "uris": [track.uri for track in self.tracks]}
        self.client.post_json_request(url=url, json_body=json_body)

    def _create_playlist(
        self,
        user: User,
        name: str = "",
        public: bool = False,
        collaborative: bool = False,
        description: str = "Harmonic playlist to match tonality",
    ) -> str:
        """Create new playlist in current user's profile.

        Args:
            user (User): Generic user class
            name (str, optional): Name of the playlist. Defaults to "".
            public (bool, optional): Set playlist to public. Defaults to True.
            collaborative (bool, optional): Set collaborative playlist. Defaults to False.
            description (str, optional): Playlist's description. 
                Defaults to "Harmonic playlist to match tonality".

        Returns:
            str: Created playlist id.
        """
        default_name = f"Harmonic Playlist: {self.reference_track.name}"
        logging.info("Creating new playlist")
        if not name:
            name = input(
                f"Enter playlist name,"
                f" press enter to use default name: '{default_name}'"
                ">"
            )
        playlist_name = name if name else default_name
        logging.info(f"Playlist name: '{playlist_name}")
        data = self.client.post_json_request(
            url=url_create_playlist.format(user_id=user.id),
            json_body={
                "name": playlist_name,
                "public": public,
                "collaborative": collaborative,
                "description": description,
            },
        )
        logging.debug(data)
        return data["id"]

    def _get_recommendations_by_tone(
        self, kind: str = "natural", limit: int = 100
    ) -> List[Track]:
        """Get recommendations by reference track's tonality.

        Args:
            kind (str, optional): Type of tonality "natural" or "relative". 
                Defaults to "natural".
            limit (int, optional): Number of tracks to retrieve from API
                from 1 to 100. Defaults to 100.

        Returns:
            List[Track]: List of tracks retrieved from API.
        """
        if not self.reference_track.tonality:
            self.reference_track.get_audio_features()
        assert (
            self.reference_track.tonality.key_signature is not None
        ), f"No tone available for this track :( {self.reference_track}"

        tone_by_kind = {
            "natural": self.reference_track.tonality,
            "relative": self.reference_track.tonality.relative_key(),
        }

        tone = tone_by_kind[kind]

        query_params = {
            "seed_tracks": self.reference_track.id,
            "limit": limit,
            "target_key": tone.key,
            "target_mode": tone.mode,
        }
        data = self._get_api_recommendations(query_params)
        tracks = [Track.from_spotify_track_object(d) for d in data["tracks"]]
        return tracks

    def _get_api_recommendations(self, query_params: Dict) -> Dict:
        """Get recommendations from spotify API

        For further details refer to
        https://developer.spotify.com/documentation/web-api/reference/#/operations/get-recommendations

        Args:
            query_params (Dict): Query params for detailed recommendations request

        Returns:
            Dict: JSON response from API.
        """
        query_str = urllib.parse.urlencode(query_params)
        url = f"{url_recommendations}?{query_str}"
        data = self.client.get_json_request(url)
        logging.debug(f"Tracks retrieved from API: {len(data['tracks'])}")
        return data

    def _batch_audio_features_for_tracks(self, tracks: List[Track]) -> List[Track]:
        """Get audio features for several tracks from API

        Args: tracks (List[Track]): List of tracks to get features. Maximum 100 tracks.
        Returns:  List[Track]: Input list of tracks with audio features.
        """
        ids = [track.id for track in tracks]
        ids = urllib.parse.urlencode({"ids": ",".join(ids)})
        url = f"{url_audio_features_several_tracks}?{ids}"
        audio_features = self.client.get_json_request(url)
        tracks_with_audio_features = []
        for track, audio_f in zip(tracks, audio_features["audio_features"]):
            assert (
                track.id == audio_f["id"]
            ), f"No match id track and audio features: {track}"
            track.audio_features = audio_f
            track.tonality = Tonality(mode=audio_f["mode"], key=audio_f["key"])
            tracks_with_audio_features.append(track)
        return tracks_with_audio_features

    def _filter_by_tone_or_relative(self, tracks: List[Track]) -> List[Track]:
        """Filter tracks by tonlaity        

        Args: tracks (List[Track]): List of tracks to filter
        Raises: ValueError: If track has no tonality defined from API.
        Returns: List[Track]: List of filtered tracks by tonality.
        """
        filtered_tracks = []
        for track in tracks:
            if not track.tonality:
                raise ValueError(f"No tonality for track {track}")
            if track.tonality not in (
                self.reference_track.tonality,
                self.reference_track.tonality.relative_key(),
            ):
                logging.debug(f"Ignoring track: {track}")
                continue
            filtered_tracks.append(track)
        return filtered_tracks

    def preview(self) -> str:
        """Returns preview of current tracks on playlist."""
        preview_string = []
        for n, track in enumerate(self.tracks):
            preview_string.append(
                f"{str(n).zfill(2)}. [{track.tonality.key_signature}] --> {track.name} by {track.artists}"
            )
        return "\n".join(preview_string)

    def to_dataframe(self):
        """List of tracks in dataframe format.

        Returns:
            pd.DataFrame: Current tracks in data frame format.
        """
        import pandas as pd

        from spotify.track import TARGET_AUDIO_FEATURES

        data = []
        for track in self.tracks:
            tr = {
                "name": track.name,
                "artists": track.artists,
                "id": track.id,
                "key_signature": track.tonality.key_signature,
            }
            for feature in TARGET_AUDIO_FEATURES:
                tr[feature] = track.audio_features[feature]
            data.append(tr)
        return pd.DataFrame(data)


header = """
 _   _                                  _       ______ _             _ _     _   
| | | |                                (_)      | ___ \ |           | (_)   | |  
| |_| | __ _ _ __ _ __ ___   ___  _ __  _  ___  | |_/ / | __ _ _   _| |_ ___| |_ 
|  _  |/ _` | '__| '_ ` _ \ / _ \| '_ \| |/ __| |  __/| |/ _` | | | | | / __| __|
| | | | (_| | |  | | | | | | (_) | | | | | (__  | |   | | (_| | |_| | | \__ \ |_ 
\_| |_/\__,_|_|  |_| |_| |_|\___/|_| |_|_|\___| \_|   |_|\__,_|\__, |_|_|___/\__|
                                                                __/ |            
                                                                |___/             
"""

def display_header() -> None:
    print(header)
