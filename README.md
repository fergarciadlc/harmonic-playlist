# Harmonic Playlist

Python implementation for composing a spotify playlist that match the Key and style
from a reference track.

## Installation
Clone the repository, install dependencies:

    pip install -r requirements.txt


### Spotify Auth Token
Generate a spotify auth token from https://developer.spotify.com/ and save it into an environment variable:

    SPOTIFY_AUTH_TOKEN=token-from-spotify

Make sure that the generated token includes the following scopes for create and add tracks to playlists:

- playlist-modify-private
- playlist-modify-public

For more information refer to Spotify API official documentation:
https://developer.spotify.com/documentation/general/guides/authorization/


## Usage
Run the man script with Python 3.7 or above:

    python src/main.py --track_id <track_id> [--debug]

If the track id is not defined from the cli flag you can manually edit the default track id in `main.py`.


### Example Output:
```
> python src/main.py --track_id 7EZC6E7UjZe63f1jRmkWxt

 _   _                                  _       ______ _             _ _     _
| | | |                                (_)      | ___ \ |           | (_)   | |
| |_| | __ _ _ __ _ __ ___   ___  _ __  _  ___  | |_/ / | __ _ _   _| |_ ___| |_
|  _  |/ _` | '__| '_ ` _ \ / _ \| '_ \| |/ __| |  __/| |/ _` | | | | | / __| __|
| | | | (_| | |  | | | | | | (_) | | | | | (__  | |   | | (_| | |_| | | \__ \ |_
\_| |_/\__,_|_|  |_| |_| |_|\___/|_| |_|_|\___| \_|   |_|\__,_|\__, |_|_|___/\__|
                                                                __/ |
                                                                |___/

INFO:root:* * * * * * * * * * * * * * * * * * * *
INFO:root:Reference track:
Zombie
by: ['The Cranberries']
INFO:root:* * * * * * * * * * * * * * * * * * * *
INFO:root:Preview:
INFO:root:
00. [G] --> Zombie by ['The Cranberries']
01. [G] --> Ode To My Family by ['The Cranberries']
02. [G] --> Creep by ['Radiohead']
03. [G] --> It's The End Of The World As We Know It (And I Feel Fine) by ['R.E.M.']
04. [G] --> Two Princes by ['Spin Doctors']
05. [G] --> Last Kiss by ['Pearl Jam']
06. [G] --> Fly Away by ['Lenny Kravitz']
07. [G] --> Linger by ['The Cranberries']
08. [G] --> Blaze Of Glory - From "Young Guns II" Soundtrack by ['Jon Bon Jovi']
09. [G] --> Drive by ['R.E.M.']
10. [G] --> Karma Police by ['Radiohead']
11. [G] --> Go West - 2003 Remaster by ['Pet Shop Boys']
12. [G] --> Stand by Me by ['Oasis']
13. [G] --> Candy by ['Iggy Pop']
14. [G] --> Lift Me Up by ['Moby']
15. [G] --> Man On The Moon by ['R.E.M.']
16. [G] --> Cornflake Girl by ['Tori Amos']
17. [G] --> Sweet Child O' Mine by ['Sheryl Crow']
18. [G] --> Spaceman by ['4 Non Blondes']
19. [G] --> Beautiful James by ['Placebo']
20. [G] --> Call Me When You're Sober by ['Evanescence']
21. [G] --> Imitation Of Life by ['R.E.M.']
22. [G] --> Linger by ['The Cranberries']
23. [G] --> Belfast Child - Remastered 2002 by ['Simple Minds']
24. [G] --> I'll Stand by You by ['Pretenders']
25. [G] --> Closing Time by ['Semisonic']
26. [Em] --> Zombie - Acoustic Version by ['The Cranberries']
27. [Em] --> Bring Me To Life by ['Evanescence']
28. [Em] --> Weak by ['Skunk Anansie']
29. [Em] --> Epic by ['Faith No More']
30. [Em] --> Black by ['Pearl Jam']
31. [Em] --> Rock You Like A Hurricane by ['Scorpions']
32. [Em] --> Promises by ['The Cranberries']
33. [Em] --> Disarm - Remastered by ['The Smashing Pumpkins']
34. [Em] --> Street Spirit (Fade Out) by ['Radiohead']
35. [Em] --> I Will Survive by ['CAKE']
36. [Em] --> Take Me Out by ['Franz Ferdinand']
37. [Em] --> Push It - 2018 - Remaster by ['Garbage']
38. [Em] --> Animal Instinct by ['The Cranberries']
39. [Em] --> Billie Jean by ['Chris Cornell']
40. [Em] --> People Are Strange by ['The Doors']
41. [Em] --> Wake Me When It's Over by ['The Cranberries']
42. [G] --> Creep by ['Radiohead']
INFO:root:Creating new playlist
Enter playlist name, press enter to use default name: 'Harmonic Playlist: Zombie'>
INFO:root:Playlist name: 'Harmonic Playlist: Zombie
INFO:root:43 tracks exported to playlist
INFO:root:Enjoy your new playlist! :)
```
