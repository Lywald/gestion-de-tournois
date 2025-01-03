from datetime import datetime
from typing import List
from .match import Match


class Round:
    def __init__(self, name: str):
        self.name = name
        self.start_datetime = datetime.now()
        self.end_datetime = None
        self.matches: List[Match] = []

    def end_round(self):
        self.end_datetime = datetime.now()

    def add_match(self, match: Match):
        self.matches.append(match)

    def to_dict(self):
        return {
            "name": self.name,
            "start_datetime": self.start_datetime.isoformat(),
            "end_datetime": (self.end_datetime.isoformat()
                             if self.end_datetime else None),
            "matches": [match.__dict__ for match in self.matches]
        }

    def __repr__(self):
        return f"Round {self.name} ({len(self.matches)} matches)"
