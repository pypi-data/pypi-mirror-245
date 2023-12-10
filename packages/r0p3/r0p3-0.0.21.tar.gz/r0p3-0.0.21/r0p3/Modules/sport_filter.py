from dataclasses import dataclass
from r0p3.Modules.sport_event import SportEvent

@dataclass
class SportFilter:
    title: list[str]
    sport: list[str]

    def is_filter(cls, sportEvent: SportEvent) -> bool:
        if not cls.title and not cls.sport:
            return False
        if cls.title:
            if len([title for title in cls.title if title.lower() in sportEvent.title.lower()]) == 0:
                return False
        if cls.sport:
            if len([sport for sport in cls.sport if sport.lower() in sportEvent.sport.lower()]) == 0:
                return False
        return True
        