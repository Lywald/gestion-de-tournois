import json
from datetime import datetime

from models.player import Player
from models.tournament import Tournament
from models.round import Round
from models.match import Match
from controllers.matchmaking import Matchmaking  # Import Matchmaking class


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

    def add_tournament(self, name):
        """
        Add a new tournament with the given name.
        Prompts the user for tournament details such as location, start and end dates,
        number of rounds, and description. Also allows adding players to the tournament
        by their national ID.
        Args:
            name (str): The name of the tournament.
        """
        location = input("Entrez le lieu du tournoi: ")
        start_date_str = input("Date de début du tournoi (YYYY-MM-DD): ")
        end_date_str = input("Date de fin du tournoi (YYYY-MM-DD): ")
        number_of_rounds = int(input("Entrez le nombre de tours: "))
        description = input("Entrez la description du tournoi: ")

        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

        new_tournament = Tournament(name, location, start_date, end_date,
                                    number_of_rounds, description)

        while True:
            national_id = input("ID national du joueur ('done' pour finir): ")
            if national_id.lower() == 'done':
                break
            player = next((p for p in self.players_data
                           if p.national_id == national_id), None)
            if player:
                new_tournament.add_player(player)
                print(f"Joueur {player.first_name} {player.last_name} ajouté.")
            else:
                print("Joueur non trouvé.")

        self.tournaments_data.append(new_tournament)
        self.refresh_json_files()
        input("Tournoi ajouté. Appuyez sur Entrée pour continuer...")

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

    def add_tour(self, tournament_index):
        """
        Adds rounds to a specified tournament by index.
        Args:
            tournament_index (int): The index of the tournament to add rounds to.
        Prompts the user to enter round names until 'done' is entered.
        Updates the tournament data after adding rounds.
        """
        if not (0 <= tournament_index < len(self.tournaments_data)):
            print("Index invalide")
            return

        while True:
            name = input("Entrez le nom du tour (ou 'done' pour terminer): ")
            if name.lower() == 'done':
                break
            if self.add_round_to_tournament(tournament_index, name):
                print(f"Tour {name} ajouté au tournoi.")
            else:
                print("Erreur lors de l'ajout du tour.")

        print("Les tours ont été ajoutés et sauvegardés.")

    def display_reports(self):
        """Display the available reports menu."""
        while True:
            print("\nRapports disponibles:")
            print("1. Liste de tous les joueurs par ordre alphabétique")
            print("2. Liste de tous les tournois")
            print("3. Nom et dates d’un tournoi donné")
            print("4. Liste des joueurs du tournoi par ordre alphabétique")
            print("5. Liste de tous les tours du tournoi et de tous les matchs du tour")
            print("6. Retour au menu principal")
            choice = input("Choisissez une option: ")

            if choice == '1':
                self.report_all_players()
            elif choice == '2':
                self.report_all_tournaments()
            elif choice == '3':
                self.report_tournament_details()
            elif choice == '4':
                self.report_tournament_players()
            elif choice == '5':
                self.report_tournament_rounds_and_matches()
            elif choice == '6':
                break
            else:
                print("Option invalide, veuillez réessayer.")

    def report_all_players(self):
        """Report: List all players in alphabetical order."""
        players_sorted = sorted(self.players_data, key=lambda p: (p.last_name, p.first_name))
        print("\nListe de tous les joueurs par ordre alphabétique:")
        for player in players_sorted:
            print(f"{player.first_name} {player.last_name} ({player.national_id})")
        input("Appuyez sur Entrée pour continuer...")

    def report_all_tournaments(self):
        """Report: List all tournaments."""
        print("\nListe de tous les tournois:")
        for tournament in self.tournaments_data:
            print(f"{tournament.name}")
        input("Appuyez sur Entrée pour continuer...")

    def report_tournament_details(self):
        """Report: Display the name and dates of a given tournament."""
        tournament_name = input("Entrez le nom du tournoi: ")
        tournament = next((t for t in self.tournaments_data if t.name == tournament_name), None)
        if tournament:
            print(f"\nNom: {tournament.name}")
            print(f"Dates: {tournament.start_date} - {tournament.end_date}")
        else:
            print("Tournoi non trouvé.")
        input("Appuyez sur Entrée pour continuer...")

    def report_tournament_players(self):
        """Report: List the players of a tournament in alphabetical order."""
        tournament_name = input("Entrez le nom du tournoi: ")
        tournament = next((t for t in self.tournaments_data if t.name == tournament_name), None)
        if tournament:
            players_sorted = sorted(tournament.players, key=lambda p: (p.last_name, p.first_name))
            print(f"\nListe des joueurs du tournoi {tournament.name} par ordre alphabétique:")
            for player in players_sorted:
                print(f"{player.first_name} {player.last_name} ({player.national_id})")
        else:
            print("Tournoi non trouvé.")
        input("Appuyez sur Entrée pour continuer...")

    def report_tournament_rounds_and_matches(self):
        """Report: List all rounds of the tournament and all matches of the round."""
        tournament_name = input("Entrez le nom du tournoi: ")
        tournament = next((t for t in self.tournaments_data if t.name == tournament_name), None)
        if tournament:
            print(f"\nListe de tous les tours du tournoi {tournament.name} et de tous les matchs du tour:")
            for round in tournament.rounds:
                print(f"Round: {round.name}")
                for match in round.matches:
                    print(f"  Match: {match.player1} ({match.score1}) vs {match.player2} ({match.score2})")
        else:
            print("Tournoi non trouvé.")
        input("Appuyez sur Entrée pour continuer...")

    def filter_players_and_load_tours(self, tournament_index):
        """Filter players and load tours based on the selected tournament."""
        tournaments_data = self.tournaments_data
        if not (0 <= tournament_index < len(tournaments_data)):
            for player in self.players_data:
                print(f"\t\tPlayer: {player.first_name} {player.last_name} "
                      f"({player.national_id})")
        else:
            selected_tournament = tournaments_data[tournament_index]
            tournament_players = [
                player.national_id for player in selected_tournament.players
            ]
            if not self.players_data:
                print("Aucun joueur dans le tournoi")
            for player in self.players_data:
                if player.national_id in tournament_players:
                    print(f"\t\tPlayer: {player.first_name} {player.last_name} "
                          f"({player.national_id})")

        if not selected_tournament.rounds:
            print("\t\tAucun tour dans le tournoi")
        for round in selected_tournament.rounds:
            print(f"\t\tRound: {round.name}")

    def load_matches(self, tournament_index, tour_index):
        """Load matches for the selected tour."""
        tournaments_data = self.tournaments_data
        if 0 <= tournament_index < len(tournaments_data):
            selected_tournament = tournaments_data[tournament_index]
            tours = selected_tournament.rounds
            if tour_index >= 0 and tour_index < len(tours):
                selected_tour = tours[tour_index]
                matches = selected_tour.matches
                for match in matches:
                    print(f"Match: {match.player1} ({match.score1}) vs "
                          f"{match.player2} ({match.score2})")

    def run_tournament(self, tournament_index):
        """Run the tournament by calling the matchmaking controller."""
        if tournament_index is None:
            print("Tournoi non sélectionné")
        else:
            self.run_matchmaking(tournament_index)
            print("Le tournoi a été lancé avec succès.")
        input("Appuyez sur Entrée pour continuer...")

    def run_matchmaking(self, tournament_index):
        """
        Run the matchmaking process for the specified tournament.
        Args:
            tournament_index (int): Index of the tournament in the list.
        """
        if isinstance(tournament_index, int) and 0 <= tournament_index < len(self.tournaments_data):
            tournament = self.tournaments_data[tournament_index]
            Matchmaking.run_tournament(tournament)
            self.refresh_json_files()
            print(f"Matchmaking completed for tournament: {tournament.name}")

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
        round.matches = [
            Match(
                player1=Player(**m["player1"]) if m["player1"] else None,
                score1=m["score1"],
                player2=Player(**m["player2"]) if m["player2"] else None,
                score2=m["score2"]
            ) for m in data["matches"]
        ]
        return round
