from HarmonicPlaylist import HarmonicPlaylist
from SpotifyClient.Track import Track
from SpotifyClient import Client
from SpotifyClient.User import User
import os
import logging
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--debug", dest="debug", action="store_true", required=False)

ENV_TOKEN = "SPOTIFY_AUTH_TOKEN"


def get_env_variable(env_var):
    try:
        env = os.environ[env_var]
        return env
    except KeyError:
        logging.error(f"Undefined env var: {env_var}")
        raise


if __name__ == "__main__":
    args = parser.parse_args()
    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.getLogger().setLevel(log_level)
    auth_token = get_env_variable(ENV_TOKEN)
    client = Client(auth_token=auth_token)
    ref_track_id = "2xWqdBkscAqh0JTVms1f0f"
    ref_track = Track.from_track_id(ref_track_id, client)
    logging.info(f"Reference track: {ref_track}")
    hp = HarmonicPlaylist(client=client, reference_track=ref_track)
    hp.generate(hard_filter=True)
    # df = hp.to_dataframe()
    # logging.info(df)
    logging.info("Preview:")
    logging.info("\n" + hp.preview())
    user = User.from_api_data(client.get_json_request("https://api.spotify.com/v1/me"))

    hp.export_playlist(user)
