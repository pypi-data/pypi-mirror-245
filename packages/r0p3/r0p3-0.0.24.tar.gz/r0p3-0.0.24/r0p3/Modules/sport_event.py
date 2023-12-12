from dataclasses import dataclass

@dataclass
class SportEvent:
    title: str
    time: str
    sport: str

    @classmethod
    def from_webscrape(cls, input):
        return cls(*input)