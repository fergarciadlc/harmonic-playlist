# from SpotifyClient.Track import Track
# from typing import Sequence, Tuple
from dataclasses import dataclass

KEYS = ("C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B")
MODES = (0, 1)
MODE_MAP = {0: "m", 1: ""}  # 0: minor, 1: major


@dataclass
class Tonality:
    mode: int
    key: int = -1

    @property
    def key_signature(self) -> str:
        if self.key == -1:
            return "n/a"
        return KEYS[self.key] + MODE_MAP[self.mode]

    def relative_key(self):
        if self.key == -1:
            raise ValueError("No key defined")
        if self.mode == 1:
            offset_to_minor = 9
            if self.key + offset_to_minor > 11:
                offset_to_minor -= 12
            return Tonality(
                mode=0,
                key=self.key + offset_to_minor
            )
        elif self.mode == 0:
            pass


def chromatic_chords(mode=1):
    return [Tonality(key=n, mode=mode) for n in range(12)]


# def filter_by_tonality(tracks: Sequence[Track], target: Tuple) -> Sequence[Track]:
#     pass


if __name__ == "__main__":
    c = Tonality(key=0, mode=1)
    d = Tonality(key=2, mode=1)
    g = Tonality(key=7, mode=1)
    a = Tonality(key=9, mode=1)
    print(c)

    major_chords = chromatic_chords(mode=1)
    for chord in major_chords:
        print(f"{chord.key_signature} --> {chord.relative_key().key_signature}")

    print("=====")

    minor_chords = chromatic_chords(mode=0)
    for chord in minor_chords:
        print(f"{chord.key_signature} --> {chord.relative_key().key_signature}")
