import logging
import urllib
from SpotifyClient.Track import Track
from SpotifyClient import Client
from SpotifyClient.endpoints import url_recommendations, url_audio_features_several_tracks
from SpotifyClient.harmony import Tonality
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

    def generate(self):
        # TODO: Refactor this
        natural_tracks = self._get_recommendations_by_tone(kind="natural")
        natural_tracks = self._batch_audio_features_for_tracks(natural_tracks)
        natural_tracks = self._filter_by_tone_or_relative(natural_tracks)
        relative_tracks = self._get_recommendations_by_tone(kind="relative")
        relative_tracks = self._batch_audio_features_for_tracks(relative_tracks)
        relative_tracks = self._filter_by_tone_or_relative(relative_tracks)
        self.tracks = self.tracks + natural_tracks + relative_tracks

    def _get_recommendations_by_tone(self, kind="natural", limit: int = 100):
        if not self.reference_track.tonality:
            self.reference_track.get_audio_features()
        assert (
                self.reference_track.tonality.key_signature is not None
        ), f"No tone available for this track :( {self.reference_track}"

        if kind == "natural":
            tone = self.reference_track.tonality
        elif kind == "relative":
            tone = self.reference_track.tonality.relative_key()

        query_params = {
            "seed_tracks": self.reference_track.id,
            "limit": limit,
            "target_key": tone.key,
            "target_mode": tone.mode,
        }
        data = self._get_api_recommendations(query_params)
        tracks = [Track.from_spotify_track_object(d) for d in data["tracks"]]
        return tracks

    def _get_api_recommendations(self, query_params):
        query_str = urllib.parse.urlencode(query_params)
        url = f"{url_recommendations}?{query_str}"
        data = self.client.get_json_response(url)
        logging.debug(f"Tracks retrieved from API: {len(data['tracks'])}")
        return data

    def _batch_audio_features_for_tracks(self, tracks: List[Track]):
        ids = [track.id for track in tracks]
        ids = urllib.parse.urlencode({"ids": ",".join(ids)})
        url = f"{url_audio_features_several_tracks}?{ids}"
        audio_features = self.client.get_json_response(url)
        tracks_with_audio_features = []
        for track, audio_f in zip(tracks, audio_features["audio_features"]):
            assert track.id == audio_f["id"], f"No match id track and audio features: {track}"
            track.audio_features = audio_f
            track.tonality = Tonality(
                mode=audio_f["mode"],
                key=audio_f["key"]
            )
            tracks_with_audio_features.append(track)
        return tracks_with_audio_features

    def _filter_by_tone_or_relative(self, tracks: List[Track]):
        filtered_tracks = []
        for track in tracks:
            if not track.tonality:
                raise ValueError(f"No tonality for track {track}")
            if track.tonality not in (self.reference_track.tonality, self.reference_track.tonality.relative_key()):
                logging.debug(f"Ignoring track: {track}")
                continue
            filtered_tracks.append(track)
        return filtered_tracks
