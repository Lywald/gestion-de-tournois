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

    def __init__(self, menu_view):
        self.menu_view = menu_view
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
                        national_id=p["national_id"],
                        total_points=p.get("total_points", 0)
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
        self.menu_view.print_message(f"Player {first_name} {last_name} added successfully.")

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
                self.menu_view.print_message(f"Joueur {player.first_name} {player.last_name} ajouté.")
            else:
                self.menu_view.print_message("Joueur non trouvé.")

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
            self.menu_view.print_message("Index invalide")
            return

        while True:
            name = input("Entrez le nom du tour (ou 'done' pour terminer): ")
            if name.lower() == 'done':
                break
            if self.add_round_to_tournament(tournament_index, name):
                self.menu_view.print_message(f"Tour {name} ajouté au tournoi.")
            else:
                self.menu_view.print_message("Erreur lors de l'ajout du tour.")

        self.menu_view.print_message("Les tours ont été ajoutés et sauvegardés.")

    def display_reports(self):
        """Display the available reports menu."""
        while True:
            self.menu_view.print_message("\nRapports disponibles:")
            self.menu_view.print_message("1. Liste de tous les joueurs par ordre alphabétique")
            self.menu_view.print_message("2. Liste de tous les tournois")
            self.menu_view.print_message("3. Nom et dates du tournoi ouvert")
            self.menu_view.print_message("4. Liste des joueurs du tournoi par ordre alphabétique")
            self.menu_view.print_message("5. Liste de tous les tours du tournoi et de tous les matchs du tour")
            self.menu_view.print_message("6. Retour au menu principal")
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
                self.menu_view.print_message("Option invalide, veuillez réessayer.")

    def report_all_players(self):
        """Report: List all players in alphabetical order."""
        players_sorted = sorted(self.players_data, key=lambda p: (p.last_name, p.first_name))
        self.menu_view.print_message("\nListe de tous les joueurs par ordre alphabétique:")
        for player in players_sorted:
            self.menu_view.print_message(f"{player.first_name} {player.last_name} ({player.national_id})")
        input("Appuyez sur Entrée pour continuer...")

    def report_all_tournaments(self):
        """Report: List all tournaments."""
        self.menu_view.print_message("\nListe de tous les tournois:")
        for tournament in self.tournaments_data:
            self.menu_view.print_message(f"{tournament.name}")
        input("Appuyez sur Entrée pour continuer...")

    def report_tournament_details(self, current_tournament):
        """Report: Display the name and dates of the currently loaded tournament."""
        if current_tournament:
            self.menu_view.print_message(f"\nNom: {current_tournament.name}")
            self.menu_view.print_message(f"Dates: {current_tournament.start_date} - {current_tournament.end_date}")
        else:
            self.menu_view.print_message("Tournoi non sélectionné.")
        input("Appuyez sur Entrée pour continuer...")

    def report_tournament_players(self, current_tournament):
        """Report: List the players of the currently loaded tournament in alphabetical order."""
        if current_tournament:
            players_sorted = sorted(current_tournament.players, key=lambda p: (p.last_name, p.first_name))
            self.menu_view.print_message(f"\nListe alphabétique des joueurs du tournoi {current_tournament.name} :")
            for player in players_sorted:
                self.menu_view.print_message(f"{player.first_name} {player.last_name} ({player.national_id})")
        else:
            self.menu_view.print_message("Tournoi non sélectionné.")
        input("Appuyez sur Entrée pour continuer...")

    def report_tournament_rounds_and_matches(self, current_tournament):
        """Report: List all rounds of the currently loaded tournament and all matches of the round."""
        if current_tournament:
            self.menu_view.print_message(f"\nListe des tours du tournoi {current_tournament.name} et ses matchs:")
            for round in current_tournament.rounds:
                self.menu_view.print_message(f"Round: {round.name}")
                for match in round.matches:
                    self.menu_view.print_message(
                        f"  Match: {match.player1} ({match.score1}) vs {match.player2} ({match.score2})"
                    )
        else:
            self.menu_view.print_message("Tournoi non sélectionné.")
        input("Appuyez sur Entrée pour continuer...")

    def filter_players_and_load_tours(self, tournament_index):
        """Filter players and load tours based on the selected tournament."""
        tournaments_data = self.tournaments_data
        if not (0 <= tournament_index < len(tournaments_data)):
            for player in self.players_data:
                self.menu_view.print_message(
                    f"\t\tJoueur: {player.first_name} {player.last_name} ({player.national_id})"
                )
        else:
            selected_tournament = tournaments_data[tournament_index]
            tournament_players = [
                player.national_id for player in selected_tournament.players
            ]
            if not self.players_data:
                self.menu_view.print_message("Aucun joueur dans le tournoi")
            for player in self.players_data:
                if player.national_id in tournament_players:
                    self.menu_view.print_message(
                        f"\t\tJoueur: {player.first_name} {player.last_name} ({player.national_id})"
                    )

        if not selected_tournament.rounds:
            self.menu_view.print_message("\t\tAucun tour dans le tournoi")
        for round in selected_tournament.rounds:
            self.menu_view.print_message(f"\t\tTour: {round.name}")

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
                    self.menu_view.print_message(
                        f"Match: {match.player1} ({match.score1}) vs {match.player2} ({match.score2})"
                    )

    def run_tournament(self, tournament_index, display_winner_callback):
        """Run the tournament by calling the matchmaking controller."""
        if tournament_index is None:
            self.menu_view.print_message("Tournoi non sélectionné")
        else:
            self.run_matchmaking(tournament_index, display_winner_callback)
            self.menu_view.print_message("Le tournoi a été lancé avec succès.")
        input("Appuyez sur Entrée pour continuer...")

    def run_matchmaking(self, tournament_index, display_winner_callback):
        """
        Run the matchmaking process for the specified tournament.
        Args:
            tournament_index (int): Index of the tournament in the list.
            display_winner_callback (function): A callback function to display the winner of each round.
        """
        if isinstance(tournament_index, int) and 0 <= tournament_index < len(self.tournaments_data):
            tournament = self.tournaments_data[tournament_index]
            tournament.rounds = []  # Clear existing rounds to avoid duplication
            for player in tournament.players:
                player.tournament_points = 0  # Reset tournament points for each player
            matchmaking = Matchmaking(self.menu_view)
            all_round_winners = matchmaking.run_tournament(tournament)  # noqa: F841
            self.refresh_json_files()

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
        tournament.players = [Player(
            last_name=p["last_name"],
            first_name=p["first_name"],
            birth_date=datetime.strptime(p["birth_date"], "%Y-%m-%d").date(),
            national_id=p["national_id"],
            tournament_points=p.get("tournament_points", 0)
        ) for p in data["players"]]
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

    def handle_choice_1(self, current_tournament):
        """
        Handle the choice to load a tournament.
        Args:
            current_tournament: The current tournament object.
        Returns:
            The loaded tournament object.
        """
        tournaments = self.get_all_tournaments()
        if not tournaments:
            print("Aucun tournoi disponible")
        else:
            for i, tournament in enumerate(tournaments):
                print(f"{i + 1}. {tournament.name}")
            index = int(input(f"Num. de tournoi (1-{len(tournaments)}): "))
            index -= 1
            print(" ")
            print(" ")
            if 0 <= index < len(tournaments):
                current_tournament = tournaments[index]
                self.menu_view.print_header(current_tournament)
                self.filter_players_and_load_tours(index)
            else:
                print("Index invalide")
            input()
        return current_tournament

    def handle_choice_2(self, current_tournament):
        """
        Handle the choice to load matches for a specific round.
        Args:
            current_tournament: The current tournament object.
        """
        if current_tournament is None:
            print("Tournoi non sélectionné")
            input()
        else:
            tour_index = int(input("Entrez l'index du tour: ")) - 1
            tournament_index = self.tournaments_data.index(current_tournament)
            self.load_matches(tournament_index, tour_index)
            input()

    def handle_choice_3(self):
        """
        Handle the choice to add a new player.
        """
        print()
        print("Informations du joueur: (Echap ou entrée vide pour annuler)")
        last_name = input("Entrez le nom de famille du joueur: ")
        if len(last_name) == 0:
            return
        first_name = input("Entrez le prénom du joueur: ")
        if len(first_name) == 0:
            return
        birth_date = input("Date de naissance du joueur (YYYY-MM-DD): ")
        if len(birth_date) == 0:
            return
        national_id = input("Entrez l'identifiant national du joueur: ")
        if len(national_id) == 0:
            return
        self.add_player(last_name, first_name, birth_date, national_id)

    def handle_choice_4(self, current_tournament):
        """
        Handle the choice to add a new round to the loaded tournament.
        Args:
            current_tournament: The current tournament object.
        """
        if current_tournament is None:
            print("Tournoi non sélectionné")
            input()
        else:
            tournament_index = self.tournaments_data.index(current_tournament)
            self.add_tour(tournament_index)

    def handle_choice_5(self, current_tournament):
        """
        Handle the choice to run the tournament.
        Args:
            current_tournament: The current tournament object.
        """
        if current_tournament is None:
            print("Tournoi non sélectionné")
            input()
        else:
            tournament_index = self.tournaments_data.index(current_tournament)
            self.run_tournament(tournament_index, self.menu_view.display_winner)

    def handle_choice_6(self, current_tournament):
        """
        Handle the choice to display reports.
        Args:
            current_tournament: The current tournament object.
        """
        if current_tournament is None:
            print("Tournoi non sélectionné")
            input()
        else:
            while True:
                print("\nRapports disponibles:")
                print("1. Liste de tous les joueurs par ordre alphabétique")
                print("2. Liste de tous les tournois")
                print("3. Nom et dates du tournoi ouvert")
                print("4. Liste des joueurs du tournoi par ordre alphabétique")
                print("5. Liste de tous les tours du tournoi et de tous les matchs du tour")
                print("6. Retour au menu principal")
                choice = input("Choisissez une option: ")

                if choice == '1':
                    self.report_all_players()
                elif choice == '2':
                    self.report_all_tournaments()
                elif choice == '3':
                    self.report_tournament_details(current_tournament)
                elif choice == '4':
                    self.report_tournament_players(current_tournament)
                elif choice == '5':
                    self.report_tournament_rounds_and_matches(current_tournament)
                elif choice == '6':
                    break
                else:
                    print("Option invalide, veuillez réessayer.")

    def handle_choice_7(self):
        """
        Handle the choice to quit the application.
        Returns:
            False to indicate the application should quit.
        """
        print("Au revoir!")
        return False

    def handle_choice_0(self):
        """
        Handle the choice to add a new tournament.
        """
        print()
        name = input("Entrez le nom du tournoi: ")
        self.add_tournament(name)
