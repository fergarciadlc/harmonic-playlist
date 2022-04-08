from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    id: int
    display_name: str
    email: str
    uri: str

    @classmethod
    def from_api_data(cls, data: dict):
        return cls(
            id=data["id"],
            display_name=data["display_name"],
            email=data["email"],
            uri=data["uri"],
        )
