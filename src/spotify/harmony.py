from dataclasses import dataclass
from typing import List, Optional, Tuple

KEYS = ("C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B")
MODES = (0, 1)
MODE_MAP = {0: "m", 1: ""}  # 0: minor, 1: major


@dataclass
class Tonality:
    mode: int = None
    key: int = -1

    @property
    def key_signature(self) -> Optional[str]:
        """Tonality in string format"""
        if self.key == -1 or self.mode is None:
            return None
        return KEYS[self.key] + MODE_MAP[self.mode]

    def relative_key(self) -> "Tonality":
        """Converts current tonality to it's relative key"""
        if self.key == -1 or self.mode is None:
            raise ValueError("No key defined")
        new_key, new_mode = self.key_converter(key=self.key, mode=self.mode)
        return self._from_new_key(key=new_key, mode=new_mode)

    @classmethod
    def _from_new_key(cls, key: int, mode: int):
        return cls(key=key, mode=mode)

    @staticmethod
    def key_converter(key: int, mode: int) -> Tuple[int, int]:
        """Relative key calculation"""
        offset = 9 if mode == 1 else 3
        if key + offset > 11:
            offset -= 12
        new_key = key + offset
        new_mode = 0 if mode == 1 else 1
        return new_key, new_mode

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(key={self.key}, mode={self.mode}, "
            f"key_signature='{self.key_signature}')"
        )


def chromatic_chords(mode: int) -> List[Tonality]:
    return [Tonality(key=n, mode=mode) for n in range(12)]


if __name__ == "__main__":
    c = Tonality(key=0, mode=1)
    d = Tonality(key=2, mode=1)
    g = Tonality(key=7, mode=1)
    a = Tonality(key=9, mode=1)
    b = Tonality(key=11, mode=1)
    x = Tonality(key=-1, mode=1)
    print(c)

    major_chords = chromatic_chords(mode=1)
    for chord in major_chords:
        print(f"{chord.key_signature} --> {chord.relative_key().key_signature}")

    print("=====")
    print("=====")

    minor_chords = chromatic_chords(mode=0)
    for chord in minor_chords:
        print(f"{chord.key_signature} --> {chord.relative_key().key_signature}")
