from HarmonicPlaylist import HarmonicPlaylist
from SpotifyClient.Track import Track
from SpotifyClient import Client
from SpotifyClient.User import User
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
    ref_track_id = "73mcHfIXc38Z9gt4UDqwqx"
    ref_track = Track.from_track_id(ref_track_id, client)
    hp = HarmonicPlaylist(client=client, reference_track=ref_track)
    # hp.get_song_recommendations()
    # print(f"Data of size {len(data['tracks'])}")
    hp.generate(hard_filter=True)
    df = hp.to_dataframe()
    print("Preview:")
    print(hp.preview())

    user = User.from_api_data(client.get_json_response("https://api.spotify.com/v1/me"))




# if __name__ == "__main__":
#     logging.getLogger().setLevel(logging.DEBUG)
#     main()
