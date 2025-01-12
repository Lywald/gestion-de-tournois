from .player import Player


class Match:
    """
    A class to represent a match between two players.
    Attributes:
        player1 (Player): The first player.
        score1 (float): The score of the first player.
        player2 (Player): The second player.
        score2 (float): The score of the second player.
    Methods:
        to_dict(): Converts the match to a dictionary.
        __repr__(): Returns a string representation of the match.
    """

    def __init__(self, player1: Player, score1: float,
                 player2: Player, score2: float):
        self.player1 = player1
        self.score1 = score1
        self.player2 = player2
        self.score2 = score2

    def to_dict(self):
        """Convert match info to a dictionary."""
        return {
            "player1": self.player1.to_dict() if self.player1 else None,
            "score1": self.score1,
            "player2": self.player2.to_dict() if self.player2 else None,
            "score2": self.score2
        }

    def __repr__(self):
        """Returns a string representation of the match with players and their scores."""
        return (
            f"Match: {self.player1} ({self.score1}) vs "
            f"{self.player2} ({self.score2})"
        )
