import logging
import urllib
from SpotifyClient.Track import Track
from SpotifyClient.User import User
from SpotifyClient import Client
from SpotifyClient.endpoints import (
    url_recommendations,
    url_audio_features_several_tracks,
    url_create_playlist,
    url_add_items_to_playlist,
)
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

    def generate(self, hard_filter: bool = True):
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

    def export_playlist(self, user: User):
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

    def _add_tracks_to_playlist(self, playlist_id: str, position: int = 0):
        url = url_add_items_to_playlist.format(playlist_id=playlist_id)
        json_body = {"position": position, "uris": [track.uri for track in self.tracks]}
        self.client.post_json_request(url=url, json_body=json_body)

    def _create_playlist(
        self,
        user: User,
        name: str = "",
        public: bool = True,
        collaborative: bool = False,
        description: str = "Harmonic playlist to match tonality",
    ) -> str:
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
        data = self.client.get_json_request(url)
        logging.debug(f"Tracks retrieved from API: {len(data['tracks'])}")
        return data

    def _batch_audio_features_for_tracks(self, tracks: List[Track]):
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

    def _filter_by_tone_or_relative(self, tracks: List[Track]):
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

    def preview(self):
        preview_string = []
        for n, track in enumerate(self.tracks):
            preview_string.append(
                f"{str(n).zfill(2)}. [{track.tonality.key_signature}] --> {track.name} by {track.artists}"
            )
        return "\n".join(preview_string)

    def to_dataframe(self):
        import pandas as pd
        from SpotifyClient.Track import TARGET_AUDIO_FEATURES

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
