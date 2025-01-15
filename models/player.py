from datetime import date, datetime


class Player:
    def __init__(self, last_name: str, first_name: str,
                 birth_date: date, national_id: str, total_points: int = 0, tournament_points: int = 0):
        self.last_name = last_name
        self.first_name = first_name
        if isinstance(birth_date, str):
            self.birth_date = datetime.strptime(birth_date, "%Y-%m-%d").date()
        else:
            self.birth_date = birth_date
        self.national_id = national_id
        self.total_points = total_points
        self.tournament_points = tournament_points

    def to_dict(self):
        """Convert player info to a dictionary."""
        return {
            "last_name": self.last_name,
            "first_name": self.first_name,
            "birth_date": self.birth_date.isoformat(),
            "national_id": self.national_id,
            "total_points": self.total_points,
            "tournament_points": self.tournament_points
        }

    def __repr__(self):
        """Returns a string representation of the player with first name, last name, national ID, and total points."""
        return (f"{self.first_name} {self.last_name} ({self.national_id}) - "
                f"Total Points: {self.total_points}, Tournament Points: {self.tournament_points}")
