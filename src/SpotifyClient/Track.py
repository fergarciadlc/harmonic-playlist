from dataclasses import dataclass, field
from SpotifyClient import Client
from typing import Sequence, Dict, List
from SpotifyClient.endpoints import (
    url_get_track,
    url_get_several_tracks,
    url_audio_features_for_track,
    url_audio_features_several_tracks,
)
from SpotifyClient.harmony import Tonality
import urllib



@dataclass
class Track:
    id: str
    name: str = None
    artists: Sequence[str] = field(default_factory=list)
    tonality: Tonality = None
    audio_features: Dict = field(default_factory=dict)
    api_data: Dict = field(default_factory=dict, repr=False)
    client: Client = None

    @property
    def uri(self) -> str:
        if not self.api_data:
            return f"spotify:track:{self.id}"
        return self.api_data["uri"]

    def get_audio_features(self, inplace: bool = True):
        assert self.client is not None, "No client defined"
        url = url_audio_features_for_track + self.id
        audio_features = self.client.get_json_response(url)
        if self.audio_features is not None and inplace:
            self.audio_features = audio_features
            self.tonality = Tonality(
                key=audio_features["key"], mode=audio_features["mode"]
            )
        return audio_features

    @staticmethod
    def _get_track_information(track_id: str, client: Client) -> Dict:
        url = url_get_track + track_id
        track_data = client.get_json_response(url)
        return track_data

    @classmethod
    def from_track_id(cls, track_id: str, client: Client) -> "Track":
        track_data = cls._get_track_information(track_id=track_id, client=client)
        return cls(
            id=track_data["id"],
            name=track_data["name"],
            artists=[a["name"] for a in track_data["artists"]],
            api_data=track_data,
            client=client,
        )

    @classmethod
    def from_list_of_ids(
        cls, track_ids: Sequence[str], client: Client
    ) -> Sequence["Track"]:
        query_params = {"ids": ",".join(track_ids)}
        query_str = urllib.parse.urlencode(query_params)
        url = f"{url_get_several_tracks}?{query_str}"
        tracks_data = client.get_json_response(url)
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
    def from_spotify_track_object(cls, api_data: Dict):
        return cls(
            id=api_data["id"],
            name=api_data["name"],
            artists=[a["name"] for a in api_data["artists"]],
            api_data=api_data,
        )
