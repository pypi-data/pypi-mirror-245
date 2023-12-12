from dataclasses import dataclass
from sport_event import SportEvent

@dataclass
class SportFilter:
    title: list[str]
    sport: list[str]

    @classmethod
    def is_filter(self, sportEvent: SportEvent) -> bool:
        if not self.title and not self.sport:
            return False
        if self.title:
            if len([title for title in self.title if title in sportEvent.title]) == 0:
                return False
        if self.sport:
            if len([sport for sport in self.sport if sport in sportEvent.sport]) == 0:
                return False
        return True
        