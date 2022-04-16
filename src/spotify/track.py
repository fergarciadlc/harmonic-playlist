import urllib
from dataclasses import dataclass, field
from typing import Dict, List

from spotify import Client
from spotify.endpoints import (
    url_audio_features_for_track,
    url_get_several_tracks,
    url_get_track,
)
from spotify.harmony import Tonality

TARGET_AUDIO_FEATURES = [
    "acousticness",
    "danceability",
    "duration_ms",
    "energy",
    "instrumentalness",
    "key",
    "liveness",
    "loudness",
    "mode",
    "speechiness",
    "tempo",
    "time_signature",
]


@dataclass
class Track:
    id: str
    name: str = None
    artists: List[str] = field(default_factory=list)
    tonality: Tonality = None
    audio_features: Dict = field(default_factory=dict)
    api_data: Dict = field(default_factory=dict, repr=False)
    client: Client = None

    @property
    def uri(self) -> str:
        """Spotify URI string"""
        if not self.api_data:
            return f"spotify:track:{self.id}"
        return self.api_data["uri"]

    def get_audio_features(self, inplace: bool = True) -> Dict:
        """Get audio features from track

        Args:
            inplace (bool, optional): Alter track instance with audio features. Defaults to True.

        Returns:
            Dict: Audio features.
        """
        assert self.client is not None, "No client defined"
        url = url_audio_features_for_track + self.id
        audio_features = self.client.get_json_request(url)
        if self.audio_features is not None and inplace:
            self.audio_features = audio_features
            self.tonality = Tonality(
                key=audio_features["key"], mode=audio_features["mode"]
            )
        return audio_features

    @staticmethod
    def _get_track_information(track_id: str, client: Client) -> Dict:
        """Get tracks information from API."""
        url = url_get_track + track_id
        track_data = client.get_json_request(url)
        return track_data

    @classmethod
    def from_track_id(cls, track_id: str, client: Client) -> "Track":
        """Create track from track id"""
        track_data = cls._get_track_information(track_id=track_id, client=client)
        return cls(
            id=track_data["id"],
            name=track_data["name"],
            artists=[a["name"] for a in track_data["artists"]],
            api_data=track_data,
            client=client,
        )

    @classmethod
    def from_list_of_ids(cls, track_ids: List[str], client: Client) -> List["Track"]:
        """Returns list of tracks from tracks ids"""
        query_params = {"ids": ",".join(track_ids)}
        query_str = urllib.parse.urlencode(query_params)
        url = f"{url_get_several_tracks}?{query_str}"
        tracks_data = client.get_json_request(url)
        return [
            cls(
                id=data["id"],
                name=data["name"],
                artists=[a["name"] for a in data["artists"]],
                api_data=data,
            )
            for data in tracks_data["tracks"]
        ]

    @classmethod
    def from_spotify_track_object(cls, api_data: Dict) -> "Track":
        """Create track from spotify track's data"""
        return cls(
            id=api_data["id"],
            name=api_data["name"],
            artists=[a["name"] for a in api_data["artists"]],
            api_data=api_data,
        )
