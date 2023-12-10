from dataclasses import dataclass

@dataclass
class FreeGame:
    game: str
    expiry_date: str
    store: str
    url: str

    @classmethod
    def from_webscrape(cls, input):
        return cls(*input)