from HarmonicPlaylist import HarmonicPlaylist
from SpotifyClient.Track import Track
from SpotifyClient import Client
from SpotifyClient.User import User
import os
import logging
import argparse


ENV_TOKEN = "SPOTIFY_AUTH_TOKEN"


def get_env_variable(env_var):
    try:
        env = os.environ[env_var]
        return env
    except KeyError:
        logging.error(f"Undefined env var: {env_var}")
        raise

def display_header():
    print("  _   _                                  _       ______ _             _ _     _   ")
    print(" | | | |                                (_)      | ___ \ |           | (_)   | |  ")
    print(" | |_| | __ _ _ __ _ __ ___   ___  _ __  _  ___  | |_/ / | __ _ _   _| |_ ___| |_ ")
    print(" |  _  |/ _` | '__| '_ ` _ \ / _ \| '_ \| |/ __| |  __/| |/ _` | | | | | / __| __|")
    print(" | | | | (_| | |  | | | | | | (_) | | | | | (__  | |   | | (_| | |_| | | \__ \ |_ ")
    print(" \_| |_/\__,_|_|  |_| |_| |_|\___/|_| |_|_|\___| \_|   |_|\__,_|\__, |_|_|___/\__|")
    print("                                                                 __/ |            ")
    print("                                                                |___/             ")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", dest="debug", action="store_true", required=False)
    args = parser.parse_args()
    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.getLogger().setLevel(log_level)
    auth_token = get_env_variable(ENV_TOKEN)
    client = Client(auth_token=auth_token)
    ref_track_id = "2WfaOiMkCvy7F5fcp2zZ8L"
    ref_track = Track.from_track_id(ref_track_id, client)
    display_header()
    logging.info("* * * * * * * * * * * * * * * * * * * *")
    logging.info(f"Reference track: \n{ref_track.name}\nby: {ref_track.artists}")
    logging.info("* * * * * * * * * * * * * * * * * * * *")
    hp = HarmonicPlaylist(client=client, reference_track=ref_track)
    hp.generate(hard_filter=True)
    # df = hp.to_dataframe()
    # logging.info(df)
    logging.info("Preview:")
    logging.info("\n" + hp.preview())
    user = User.from_api_data(client.get_json_request("https://api.spotify.com/v1/me"))

    hp.export_playlist(user)
