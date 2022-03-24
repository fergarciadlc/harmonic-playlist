import logging
import urllib
from SpotifyClient.Track import Track
from SpotifyClient import Client
from SpotifyClient.endpoints import url_recommendations
from dataclasses import dataclass, field
from typing import List


@dataclass
class HarmonicPlaylist:
    client: Client
    reference_track: Track
    tracks: List[Track] = field(default_factory=list)

    def get_song_recommendations(self, limit: int = 100):
        query_params = {
            "seed_tracks": self.reference_track.id,
            "limit": limit,
        }
        data = self._get_api_recommendations(query_params)
        for d in data["tracks"]:
            self.tracks.append(Track.from_spotify_track_object(d))

    def _get_api_recommendations(self, query_params):
        query_str = urllib.parse.urlencode(query_params)
        url = f"{url_recommendations}?{query_str}"
        data = self.client.get_json_response(url)
        logging.debug(f"Tracks retrieved from API: {len(data['tracks'])}")
        return data
