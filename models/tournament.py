from datetime import date
from typing import List

from .round import Round
from .player import Player


class Tournament:
    """
    A class to represent a Tournament.
    Attributes:
        name (str): The name of the tournament.
        location (str): The location where the tournament is held.
        start_date (date): The start date of the tournament.
        end_date (date): The end date of the tournament.
        number_of_rounds (int): The number of rounds in the tournament (default is 4).
        description (str): A brief description of the tournament.
        rounds (List[Round]): A list to store the rounds of the tournament.
        players (List[Player]): A list to store the players participating in the tournament.
    """
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
        """
        Adds a player to the tournament.

        Args:
            player (Player): The player to add.
        """
        self.players.append(player)

    def add_round(self, round: Round):
        """
        Add a round to the tournament.

        Args:
            round (Round): The round to add to the tournament.
        """
        self.rounds.append(round)

    def to_dict(self):
        """
        Converts the Tournament object to a dictionary representation.

        This method serializes the Tournament object into a dictionary format,
        which includes all relevant attributes of the tournament such as name,
        location, start and end dates, number of rounds, description, rounds,
        and players. The dates are converted to ISO format strings, and the
        rounds and players are also converted to dictionaries using their
        respective `to_dict` methods.

        Returns:
            dict: A dictionary representation of the Tournament object.
        """
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
        """
        Returns a string representation of the Tournament instance, showing its name,
        number of players, and number of rounds.
        """
        return (
            f"Tournament {self.name} with {len(self.players)} players and "
            f"{len(self.rounds)} rounds"
        )
