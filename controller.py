import json
from datetime import datetime

from models.player import Player
from models.tournament import Tournament
from models.round import Round
from models.match import Match


class Controller:
    """
    Controller class to manage players and tournaments data.
    Methods:
        __init__(): Initializes the controller and loads players and tournaments data.
        load_players(): Loads player data from a JSON file.
        load_tournaments(): Loads tournaments data from a JSON file.
        save_players(): Saves the current players data to a JSON file.
        save_tournaments(): Saves the current tournaments data to a JSON file.
        refresh_json_files(): Refreshes both players and tournaments JSON files with current data.
        add_player(last_name, first_name, birth_date, national_id): Adds a new player and updates the JSON file.
        add_tournament(tournament): Adds a new tournament and updates the JSON file.
        add_round_to_tournament(tournament_index, round_name): Adds a new round to a specified tournament.
        get_all_tournaments(): Returns a list of all tournaments.
        dict_to_tournament(data): Converts a dictionary to a Tournament object.
        dict_to_round(data): Converts a dictionary to a Round object.
    """

    def __init__(self):
        self.players_data = self.load_players()
        self.tournaments_data = self.load_tournaments()

    def load_players(self):
        """
        Load player data from a JSON file and return a list of Player objects.
        Returns an empty list if the file is not found or contains invalid JSON.
        """
        try:
            with open("data_players.json", "r") as file:
                data = json.load(file)
                return [
                    Player(
                        last_name=p["last_name"],
                        first_name=p["first_name"],
                        birth_date=datetime.strptime(
                            p["birth_date"], "%Y-%m-%d"
                        ).date(),
                        national_id=p["national_id"]
                    ) for p in data.get("players_data", [])
                ]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def load_tournaments(self):
        """
        Load tournaments from a JSON file.

        Returns:
            list: A list of tournament objects or an empty list if the file is not found or invalid.
        """
        try:
            with open("data_tournaments.json", "r") as file:
                data = json.load(file)
                return [
                    self.dict_to_tournament(t)
                    for t in data.get("tournaments_data", [])
                ]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_players(self):
        """Save players' data to a JSON file."""
        with open("data_players.json", "w") as file:
            json.dump(
                {"players_data": [
                    player.to_dict() for player in self.players_data
                ]},
                file,
                indent=4
            )

    def save_tournaments(self):
        """Save the current tournaments data to a JSON file."""
        with open("data_tournaments.json", "w") as file:
            json.dump(
                {"tournaments_data": [
                    t.to_dict() for t in self.tournaments_data
                ]},
                file,
                indent=4
            )

    def refresh_json_files(self):
        """Refresh the JSON files with the current data."""
        self.save_tournaments()
        self.save_players()

    def add_player(self, last_name, first_name, birth_date, national_id):
        """Adds a new player to the players_data list and updates the JSON files."""
        new_player = Player(last_name, first_name, birth_date, national_id)
        self.players_data.append(new_player)
        self.refresh_json_files()
        print(f"Player {first_name} {last_name} added successfully.")

    def add_tournament(self, tournament):
        """Adds a tournament to the list and updates the JSON files."""
        self.tournaments_data.append(tournament)
        self.refresh_json_files()
        print(f"Tournament {tournament.name} added successfully.")

    def add_round_to_tournament(self, tournament_index, round_name):
        """
        Adds a new round to the specified tournament.

        Args:
            tournament_index (int): Index of the tournament in the list.
            round_name (str): Name of the new round.

        Returns:
            bool: True if the round was added, False otherwise.
        """
        if 0 <= tournament_index < len(self.tournaments_data):
            new_round = Round(round_name)
            self.tournaments_data[tournament_index].add_round(new_round)
            self.refresh_json_files()
            return True
        return False

    def get_all_tournaments(self):
        """
        Get all tournaments data.
        
        Returns:
            list: List of all tournaments.
        """
        return self.tournaments_data

    def dict_to_tournament(self, data):
        """
        Converts a dictionary representation of a tournament into a Tournament object.

        Args:
            data (dict): A dictionary containing tournament data with the following keys:
            - name (str): The name of the tournament.
            - location (str): The location where the tournament is held.
            - start_date (str): The start date of the tournament in ISO format (YYYY-MM-DD).
            - end_date (str): The end date of the tournament in ISO format (YYYY-MM-DD).
            - number_of_rounds (int): The number of rounds in the tournament.
            - description (str): A description of the tournament.
            - rounds (list): A list of dictionaries, each representing a round.
            - players (list): A list of dictionaries, each representing a player.

        Returns:
            Tournament: An instance of the Tournament class populated with the provided data.
        """
        tournament = Tournament(
            name=data["name"],
            location=data["location"],
            start_date=datetime.fromisoformat(data["start_date"]).date(),
            end_date=datetime.fromisoformat(data["end_date"]).date(),
            number_of_rounds=data["number_of_rounds"],
            description=data["description"]
        )
        tournament.rounds = [self.dict_to_round(r) for r in data["rounds"]]
        tournament.players = [Player(**p) for p in data["players"]]
        return tournament

    def dict_to_round(self, data):
        """
        Turn a dictionary into a Round object.

        Args:
            data (dict): A dictionary with round details like:
            - "name" (str): The round's name.
            - "start_datetime" (str): When the round starts (in ISO format).
            - "end_datetime" (str or None): When the round ends (in ISO format) or None if it hasn't ended.
            - "matches" (list): A list of dictionaries for each match.

        Returns:
            Round: A Round object filled with the provided data.

        Note:
            The `start_datetime` and `end_datetime` are converted from ISO format strings
            to `datetime` objects using `datetime.fromisoformat`. This makes sure the datetime
            values are correctly parsed and can be used for datetime operations in the Round object.
        """
        round = Round(name=data["name"])
        round.start_datetime = datetime.fromisoformat(data["start_datetime"])
        round.end_datetime = (
            datetime.fromisoformat(data["end_datetime"])
            if data["end_datetime"]
            else None
        )
        round.matches = [Match(**m) for m in data["matches"]]
        return round
