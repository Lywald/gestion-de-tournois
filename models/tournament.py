from datetime import date
from typing import List
from .round import Round
from .player import Player


class Tournament:
    def __init__(
        self, name: str, location: str, start_date: date, end_date: date,
        number_of_rounds: int = 4, description: str = ""
    ):
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.number_of_rounds = number_of_rounds
        self.description = description
        self.rounds: List[Round] = []
        self.players: List[Player] = []

    def add_player(self, player: Player):
        self.players.append(player)

    def add_round(self, round: Round):
        self.rounds.append(round)

    def to_dict(self):
        return {
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "number_of_rounds": self.number_of_rounds,
            "description": self.description,
            "rounds": [round.to_dict() for round in self.rounds],
            "players": [player.to_dict() for player in self.players]
        }

    def __repr__(self):
        return (
            f"Tournament {self.name} with {len(self.players)} players and "
            f"{len(self.rounds)} rounds"
        )
