import argparse
import logging
import os

from harmonic_playlist import HarmonicPlaylist, display_header
from spotify import Client, Track, User
from spotify.endpoints import url_get_current_user_profile

ENV_TOKEN = "SPOTIFY_AUTH_TOKEN"


def get_env_variable(env_var) -> str:
    try:
        env = os.environ[env_var]
        return env
    except KeyError:
        logging.error(f"Undefined env var: {env_var}")
        raise


def main() -> None:
    # Initial Configuration
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", dest="debug", action="store_true", required=False)
    parser.add_argument("--track_id", dest="track_id", default="", required=False)
    parser.add_argument("--not_filter", dest="not_filter", action="store_true", required=False)

    args = parser.parse_args()

    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.getLogger().setLevel(log_level)

    # Auth process
    auth_token = get_env_variable(ENV_TOKEN)
    client = Client(auth_token=auth_token)
    user = User.from_api_data(client.get_json_request(url_get_current_user_profile))

    # Getting reference track
    # Default: Zombie by The Cranberries
    ref_track_id = args.track_id if args.track_id else "7EZC6E7UjZe63f1jRmkWxt"
    ref_track = Track.from_track_id(ref_track_id, client)

    # Initializing process
    display_header()
    logging.info("* * * * * * * * * * * * * * * * * * * *")
    logging.info(f"Reference track: \n{ref_track.name}\nby: {ref_track.artists}")
    logging.info("* * * * * * * * * * * * * * * * * * * *")
    hp = HarmonicPlaylist(client=client, reference_track=ref_track)
    hp.generate(hard_filter=not args.not_filter) # Default True
    logging.info("Preview:")
    logging.info("\n" + hp.preview())

    # Exporting playlist
    hp.export_playlist(user)
    logging.info("Enjoy your new playlist! :)")


if __name__ == "__main__":
    main()
