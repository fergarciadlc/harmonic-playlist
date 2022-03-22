import logging
import urllib
from SpotifyClient.Track import Track
from SpotifyClient import Client
from SpotifyClient.endpoints import url_recommendations
from dataclasses import dataclass, field
from typing import Sequence


@dataclass
class HarmonicPlaylist:
    client: Client
    reference_track: Track
    tracks: Sequence[Track] = field(default_factory=list)

    def get_song_recommendations(self, limit: int = 100) ->  None:
        query_params = {
            "seed_tracks": self.reference_track.id,
            "limit": limit,
        }
        data = self._get_recommendations(query_params)
        data = self._filter_by_key(key=1, mode=0)

    def _get_recommendations(self, query_params):
        query_str = urllib.parse.urlencode(query_params)
        url = f"{url_recommendations}?{query_str}"
        data = self.client.get_json_response(url)
        logging.debug(data)
        return data
