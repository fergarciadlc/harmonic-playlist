from HarmonicPlaylist import HarmonicPlaylist
from SpotifyClient.Track import Track
from SpotifyClient import Client
import os
import logging

ENV_TOKEN = "SPOTIFY_AUTH_TOKEN"


os.environ[
    "SPOTIFY_AUTH_TOKEN"
] = "BQAnFv_OZRyNCWXGVti0NcsBjEIOS1ER9P7cL-JOwNaIgFI_HksdbM-1cwQd3JLKEZZo7ACB11CgrAZPaocu24rO26MHHeEZtq_Gmtwl3lulniM63kuDZb1p7TtyCdUKQiQp9X-f9QL8j6RcarVyKy52PK_LXcwn2lSKKJ3Ije3pyjRbxY9sBzG8gn0wRoBBZu5tzv4Tq6uft8xZAd4JBsa5L5wpKWWItYZwNnyiNqim0QRUO2xAxdy8R6b1fBKLfj0-wBvlwMMFXLordkgysQ"


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
    t1 = Track.from_track_id(track_id=ref_track_id, client=client)
    t2 = Track("asdfs")
    ts = Track.from_list_of_ids(
        ["7ouMYWpwJ422jRcDASZB7P", "4VqPOruhp5EdPBeR92t6lQ", "2takcwOaAZWiXQijPHIx7B"],
        client=client,
    )
    pl = HarmonicPlaylist(client=client, reference_track=t1)
