from HarmonicPlaylist import HarmonicPlaylist
from SpotifyClient.Track import Track
from SpotifyClient import Client
import os
import logging

ENV_TOKEN = "SPOTIFY_AUTH_TOKEN"


def get_env_variable(env_var):
    try:
        env = os.environ[env_var]
        return env
    except KeyError:
        logging.error(f"Undefined env var: {env_var}")
        raise


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    auth_token = get_env_variable(ENV_TOKEN)
    client = Client(auth_token=auth_token)
    ref_track_id = "6w8yBI2vthyN9UnwO4UBWb"
    ref_track = Track(ref_track_id)
    harmonic_playlist = HarmonicPlaylist(client=client, reference_track=ref_track)
    data = harmonic_playlist.get_song_recommendations()


# if __name__ == "__main__":
#     logging.getLogger().setLevel(logging.DEBUG)
#     main()
