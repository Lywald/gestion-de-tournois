from .player import Player


class Match:
    def __init__(self, player1: Player, score1: float,
                 player2: Player, score2: float):
        self.player1 = player1
        self.score1 = score1
        self.player2 = player2
        self.score2 = score2

    def __repr__(self):
        return (
            f"Match: {self.player1} ({self.score1}) vs "
            f"{self.player2} ({self.score2})"
        )
