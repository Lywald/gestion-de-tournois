import json
import os
import sys
from datetime import datetime

if os.name == 'nt':
    import msvcrt
else:
    import tty
    import termios

from controller import Controller
from models.tournament import Tournament
from models.player import Player

asciiHeader = """
                                                         

"""

class MainView:
    """
    Main view for managing tournaments and players.
    Methods:
        __init__(): Initialize the view and load data.
        load_tournaments(): Load tournaments from a JSON file.
        load_players(): Load players from a JSON file.
        filter_players_and_load_tours(tournament_index): Filter players and load tours for a tournament.
        load_matches(tournament_index, tour_index): Load matches for a specific tour in a tournament.
        add_tournament(name): Add a new tournament with user input details.
        add_player(last_name, first_name, birth_date, national_id): Add a new player.
        add_tour(tournament_index): Add rounds to a specified tournament.
        display_reports(): Display the reports menu.
        report_all_players(): List all players alphabetically.
        report_all_tournaments(): List all tournaments.
        report_tournament_details(): Show details of a specific tournament.
        report_tournament_players(): List players of a specific tournament alphabetically.
        report_tournament_rounds_and_matches(): List all rounds and matches of a specific tournament.
    """
    def __init__(self):
        self.controller = Controller()
        self.tournaments_data = self.controller.tournaments_data
        self.players_data = self.controller.players_data
        self.load_tournaments()
        self.load_players()

    def load_tournaments(self):
        """Load tournaments from data_tournaments.json."""
        try:
            with open("data_tournaments.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                self.tournaments_data = [
                    self.controller.dict_to_tournament(t)
                    for t in data.get("tournaments_data", [])
                ]
                if not self.tournaments_data:
                    print("Aucun tournoi disponible")
                else:
                    print(f"{len(self.tournaments_data)} tournois chargés")
                for tournament in self.tournaments_data:
                    print(f"Tournoi: {tournament.name}")
        except (FileNotFoundError, json.JSONDecodeError):
            print("Erreur lors du chargement des tournois")

    def load_players(self):
        """Load all players from the data_players.json."""
        try:
            with open("data_players.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                self.players_data = [
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
            self.players_data = []

    def filter_players_and_load_tours(self, tournament_index):
        """Filter players and load tours based on the selected tournament."""
        if not (0 <= tournament_index < len(self.tournaments_data)):
            for player in self.players_data:
                print(f"\t\tPlayer: {player.first_name} {player.last_name} "
                      f"({player.national_id})")
        else:
            selected_tournament = self.tournaments_data[tournament_index]
            tournament_players = [
                player.national_id for player in selected_tournament.players
            ]
            if not self.controller.players_data:
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
        if 0 <= tournament_index < len(self.tournaments_data):
            selected_tournament = self.tournaments_data[tournament_index]
            tours = selected_tournament.rounds
            if tour_index >= 0 and tour_index < len(tours):
                selected_tour = tours[tour_index]
                matches = selected_tour.matches
                for match in matches:
                    print(f"Match: {match.player1} ({match.score1}) vs "
                          f"{match.player2} ({match.score2})")

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

        self.controller.add_tournament(new_tournament)
        input("Tournoi ajouté. Appuyez sur Entrée pour continuer...")

    def add_player(self, last_name, first_name, birth_date, national_id):
        """ Add a new player to the tournament. """
        self.controller.add_player(last_name, first_name, birth_date,
                                   national_id)

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
            if self.controller.add_round_to_tournament(tournament_index, name):
                print(f"Tour {name} ajouté au tournoi.")
            else:
                print("Erreur lors de l'ajout du tour.")

        print("Les tours ont été ajoutés et sauvegardés.")
        self.tournaments_data = self.controller.get_all_tournaments()

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

class MenuView:
    """
    Menu view for displaying and navigating the main menu.
    Methods:
        __init__(): Initialize the menu view.
        print_header(current_tournament): Print the header for the menu.
        get_key(): Get a single key press from the user.
        main_menu(view, current_tournament): Display the main menu and handle user input.
    """
    def __init__(self):
        pass

    def print_header(self, current_tournament):
        """
        Clears the console and prints the header for the chess tournament management system.

        Args:
            current_tournament (object): The current tournament object. It should have a 'name' attribute.
                                         If None, a message indicating no tournament is loaded will be displayed.

        Returns:
            None
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\t\tGESTION DE TOURNOIS D'ECHECS")
        print("")
        if current_tournament:
            print(f"\t\tTOURNOI: {current_tournament.name}\t\t")
        else:
            print("\t\t_________________________________________________________")
            print("\t\t   Aucun Tournoi Chargé                                  \t\t")
            print("\t\t_________________________________________________________")

    def get_key(self):
        """
        Get a single key press from the user (without needing him to press Enter).

        Returns:
            key (bytes or str): The key pressed by the user. On Windows, returns a byte string.
                                On Unix-like systems, returns a single character string.
        """
        if os.name == 'nt':
            key = msvcrt.getch()
            if key == b'\xe0':  # Arrow keys are preceded by '\xe0'
                key = msvcrt.getch()
            return key
        else:
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                key = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return key

    def main_menu(self, view, current_tournament):
        """
        Show the main menu and let the user navigate with arrow keys.
        Args:
            view: The view object to render the menu.
            current_tournament: The current tournament object to show in the header.
        Returns:
            int: The index of the selected menu option.
        Navigation:
            - Use the up arrow key to move up.
            - Use the down arrow key to move down.
            - Press Enter to select the highlighted option.
        """
        options = [
            "\tCharger un tournoi",
            "\tCharger les matchs",
            "\tAjouter un tournoi",
            "\tAjouter un joueur",
            "\tAjouter un tour au tournoi chargé",
            "\tRapports",
            "\tQuitter"
        ]
        selected_index = 0

        while True:
            self.print_header(current_tournament)
            print("")
            
            offset = "\t\t"
            for i, option in enumerate(options):
                if i == selected_index:
                    print(offset + " >>>> " f"{option}")
                else:
                    print(offset + option)
            
            k = 0
            while k < 5:
                print()
                k += 1

            key = self.get_key()
            if key == b'H':  # Up arrow key
                selected_index = (selected_index - 1) % len(options)
            elif key == b'P':  # Down arrow key
                selected_index = (selected_index + 1) % len(options)
            elif key == b'\r':  # Enter key
                return selected_index

def handle_choice_0(view, menu_view, current_tournament):
    tournaments = view.controller.get_all_tournaments()
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
            menu_view.print_header(current_tournament)
            view.filter_players_and_load_tours(index)
        else:
            print("Index invalide")
        input()
    return current_tournament

def handle_choice_1(view):
    tournament_index = int(input("Entrez l'index du tournoi: ")) - 1
    tour_index = int(input("Entrez l'index du tour: ")) - 1
    view.load_matches(tournament_index, tour_index)

def handle_choice_2(view):
    print()
    name = input("Entrez le nom du tournoi: ")
    view.add_tournament(name)

def handle_choice_3(view):
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
    view.add_player(last_name, first_name, birth_date, national_id)

def handle_choice_4(view):
    tournament_index = int(input("Index du tournoi chargé: ")) - 1
    view.add_tour(tournament_index)

def handle_choice_5(view):
    view.display_reports()

def handle_choice_6():
    print("Au revoir!")
    return False

if __name__ == "__main__":
    view = MainView()
    menu_view = MenuView()
    current_tournament = None
 
    print("Bienveue dans le gestionnaire de tournois d'échecs!")

    while True:
        choice = menu_view.main_menu(view, current_tournament)

        if choice == 0:
            current_tournament = handle_choice_0(view, menu_view, current_tournament)
        elif choice == 1:
            handle_choice_1(view)
        elif choice == 2:
            handle_choice_2(view)
        elif choice == 3:
            handle_choice_3(view)
        elif choice == 4:
            handle_choice_4(view)
        elif choice == 5:
            handle_choice_5(view)
        elif choice == 6:
            if not handle_choice_6():
                break
        else:
            print("Option invalide, veuillez réessayer.")
