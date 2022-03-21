import logging
import urllib
from SpotifyClient.Track import Track
from SpotifyClient import Client
from SpotifyClient.endpoints import url_recommendations


class HarmonicPlaylist:
    def __init__(self, client: Client, reference_track: Track):
        self.client = client
        self.reference_track = reference_track
        self.tracks = []

    def get_song_recommendations(self, limit=100):
        query_params = {
            "seed_tracks": self.reference_track.id,
            "limit": limit,
        }
        data = self._get_recommendations(query_params)
        return data

    def _get_recommendations(self, query_params):
        query_str = urllib.parse.urlencode(query_params)
        url = f"{url_recommendations}?{query_str}"
        data = self.client.get_json_response(url)
        logging.debug(data)
        return data
