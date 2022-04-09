from HarmonicPlaylist import HarmonicPlaylist
from SpotifyClient.Track import Track
from SpotifyClient import Client
from SpotifyClient.User import User
import os
import logging
import argparse

ENV_TOKEN = "SPOTIFY_AUTH_TOKEN"


def get_env_variable(env_var) -> str:
    try:
        env = os.environ[env_var]
        return env
    except KeyError:
        logging.error(f"Undefined env var: {env_var}")
        raise


def display_header() -> None:
    print(r"  _   _                                  _       ______ _             _ _     _   ")
    print(r" | | | |                                (_)      | ___ \ |           | (_)   | |  ")
    print(r" | |_| | __ _ _ __ _ __ ___   ___  _ __  _  ___  | |_/ / | __ _ _   _| |_ ___| |_ ")
    print(r" |  _  |/ _` | '__| '_ ` _ \ / _ \| '_ \| |/ __| |  __/| |/ _` | | | | | / __| __|")
    print(r" | | | | (_| | |  | | | | | | (_) | | | | | (__  | |   | | (_| | |_| | | \__ \ |_ ")
    print(r" \_| |_/\__,_|_|  |_| |_| |_|\___/|_| |_|_|\___| \_|   |_|\__,_|\__, |_|_|___/\__|")
    print(r"                                                                 __/ |            ")
    print(r"                                                                |___/             ")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", dest="debug", action="store_true", required=False)
    parser.add_argument("--track_id", dest="track_id", default="", required=False)
    args = parser.parse_args()

    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.getLogger().setLevel(log_level)

    auth_token = get_env_variable(ENV_TOKEN)
    client = Client(auth_token=auth_token)
    ref_track_id = args.track_id if args.track_id else "7EZC6E7UjZe63f1jRmkWxt"

    ref_track = Track.from_track_id(ref_track_id, client)
    display_header()
    print("* * * * * * * * * * * * * * * * * * * *")
    print(f"Reference track: \n{ref_track.name}\nby: {ref_track.artists}")
    print("* * * * * * * * * * * * * * * * * * * *")
    hp = HarmonicPlaylist(client=client, reference_track=ref_track)
    hp.generate(hard_filter=True)
    # df = hp.to_dataframe()
    # logging.info(df)
    logging.info("Preview:")
    logging.info("\n" + hp.preview())
    user = User.from_api_data(client.get_json_request("https://api.spotify.com/v1/me"))

    hp.export_playlist(user)
    print("Enjoy your new playlist! :)")


if __name__ == "__main__":
    main()
