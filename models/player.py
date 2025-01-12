from datetime import date, datetime


class Player:
    """
    A class to represent a player.
    Attributes:
        last_name (str): The player's last name.
        first_name (str): The player's first name.
        birth_date (date): The player's birth date.
        national_id (str): The player's national ID as a chess player. 
    Methods:
        to_dict(): Converts player info to a dictionary.
        __repr__(): Returns a string representation of the player.
    """

    def __init__(self, last_name: str, first_name: str,
                 birth_date: date, national_id: str):
        self.last_name = last_name
        self.first_name = first_name
        if isinstance(birth_date, str):
            self.birth_date = datetime.strptime(birth_date, "%Y-%m-%d").date()
        else:
            self.birth_date = birth_date
        self.national_id = national_id

    def to_dict(self):
        """Convert player info to a dictionary."""
        return {
            "last_name": self.last_name,
            "first_name": self.first_name,
            "birth_date": self.birth_date.isoformat(),
            "national_id": self.national_id
        }

    def __repr__(self):
        """Returns a string representation of the player with first name, last name, and national ID."""
        return f"{self.first_name} {self.last_name} ({self.national_id})"
