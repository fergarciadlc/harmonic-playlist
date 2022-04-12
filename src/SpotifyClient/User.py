from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    id: int
    display_name: str
    uri: str

    @classmethod
    def from_api_data(cls, data: dict) -> "User":
        """Create user from spotify data."""
        return cls(
            id=data["id"],
            display_name=data["display_name"],
            uri=data["uri"],
        )
