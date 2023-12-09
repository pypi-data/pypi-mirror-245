from dataclasses import dataclass
from sport_event import SportEvent

@dataclass
class SportFilter:
    title: list[str]
    sport: list[str]

    @classmethod
    def is_filter(cls, sportEvent: SportEvent) -> bool:
        if not cls.title and not cls.sport:
            return False
        if cls.title:
            if len([title for title in cls.title if title in sportEvent.title]) == 0:
                return False
        if cls.sport:
            if len([sport for sport in cls.sport if sport in sportEvent.sport]) == 0:
                return False
        return True
        