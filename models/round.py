from datetime import datetime
from typing import List

from .match import Match


class Round:
    """
    A class to represent a round in a tournament.
    Attributes:
    -----------
    name : str
        The name of the round.
    start_datetime : datetime
        The start date and time of the round.
    end_datetime : datetime or None
        The end date and time of the round, initially set to None.
    matches : List[Match]
        A list of matches in the round.
    Methods:
    --------
    end_round():
        Sets the end date and time of the round to the current date and time.
    add_match(match: Match):
        Adds a match to the list of matches in the round.
    to_dict():
        Converts the round object to a dictionary.
    __repr__():
        Returns a string representation of the round object.
    """

    def __init__(self, name: str):
        self.name = name
        self.start_datetime = datetime.now()
        self.end_datetime = None
        self.matches: List[Match] = []

    def end_round(self):
        """ Marks the end of the round by setting the end time to the current datetime. """
        self.end_datetime = datetime.now()

    def add_match(self, match: Match):
        """ Adds a match to the list of matches."""
        self.matches.append(match)

    def to_dict(self):
        """
        Converts the round object to a dictionary.

        Returns:
            dict: A dictionary with the round's name, start and end datetimes,
                  and a list of matches.
        """
        return {
            "name": self.name,
            "start_datetime": self.start_datetime.isoformat(),
            "end_datetime": (self.end_datetime.isoformat()
                             if self.end_datetime else None),
            "matches": [match.to_dict() for match in self.matches]
        }

    def __repr__(self):
        """Return a string representation of the Round instance, showing its name and the number of matches."""
        return f"Round {self.name} ({len(self.matches)} matches)"
