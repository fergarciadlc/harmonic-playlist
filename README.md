# Harmonic Playlist

Python implementation for composing a spotify playlist that match the Key and style
from a reference track.

## Installation
Clone the repository, install dependencies:

    pip install -r requirements.txt


### Spotify Auth Token
Generate a spotify auth token from https://developer.spotify.com/ and save it into an environment variable:

    SPOTIFY_AUTH_TOKEN=token-from-spotify

## Usage
Run the man script with Python 3.7 or above:

    python src/main.py --track_id <track_id> [--debug]

If the track id is not defined from the cli flag you can manually edit the default track id in `main.py`.