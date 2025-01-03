import json
from datetime import datetime
from models.player import Player
from models.tournament import Tournament
from models.round import Round
from models.match import Match


class Controller:
    def __init__(self):
        self.players_data = self.load_players()
        self.tournaments_data = self.load_tournaments()

    def load_players(self):
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
        with open("data_players.json", "w") as file:
            json.dump(
                {"players_data": [
                    player.to_dict() for player in self.players_data
                ]},
                file,
                indent=4
            )

    def save_tournaments(self):
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
        new_player = Player(last_name, first_name, birth_date, national_id)
        self.players_data.append(new_player)
        self.refresh_json_files()
        print(f"Player {first_name} {last_name} added successfully.")

    def add_tournament(self, tournament):
        self.tournaments_data.append(tournament)
        self.refresh_json_files()
        print(f"Tournament {tournament.name} added successfully.")

    def add_round_to_tournament(self, tournament_index, round_name):
        if 0 <= tournament_index < len(self.tournaments_data):
            new_round = Round(round_name)
            self.tournaments_data[tournament_index].add_round(new_round)
            self.refresh_json_files()
            return True
        return False

    def get_all_tournaments(self):
        return self.tournaments_data

    def dict_to_tournament(self, data):
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
        round = Round(name=data["name"])
        round.start_datetime = datetime.fromisoformat(data["start_datetime"])
        round.end_datetime = (
            datetime.fromisoformat(data["end_datetime"])
            if data["end_datetime"]
            else None
        )
        round.matches = [Match(**m) for m in data["matches"]]
        return round
