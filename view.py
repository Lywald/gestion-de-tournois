import sys
import json
from controller import Controller
from models.tournament import Tournament
from datetime import datetime
from models.player import Player
from models.round import Round

class MainView:
    def __init__(self):
        self.controller = Controller()
        self.tournaments_data = self.controller.tournaments_data
        self.players_data = self.controller.players_data
        self.load_tournaments()
        self.load_players()

    def load_tournaments(self):
        """Load tournaments from the tournaments_data key in data_tournaments.json."""
        try:
            with open("data_tournaments.json", "r") as file:
                data = json.load(file)
                self.tournaments_data = [self.controller.dict_to_tournament(t) for t in data.get("tournaments_data", [])]
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
            with open("data_players.json", "r") as file:
                data = json.load(file)
                self.players_data = [Player(
                    last_name=p["last_name"],
                    first_name=p["first_name"],
                    birth_date=datetime.strptime(p["birth_date"], "%Y-%m-%d").date(),
                    national_id=p["national_id"]
                ) for p in data.get("players_data", [])]
        except (FileNotFoundError, json.JSONDecodeError):
            self.players_data = []

    def filter_players_and_load_tours(self, tournament_index):
        """Filter players and load tours based on the selected tournament. If no tournament is selected, load all players."""
        if tournament_index < 0 or tournament_index >= len(self.tournaments_data):
            for player in self.players_data:
                print(f"Player: {player.first_name} {player.last_name} ({player.national_id})")
        else:
            selected_tournament = self.tournaments_data[tournament_index]
            tournament_players = [player.national_id for player in selected_tournament.players]
            if not self.players_data:
                print("Aucun joueur dans le tournoi")
            for player in self.players_data:
                if player.national_id in tournament_players:
                    print(f"Player: {player.first_name} {player.last_name} ({player.national_id})")
        
        if not selected_tournament.rounds:
            print("Aucun tour dans le tournoi")
        for round in selected_tournament.rounds:
            print(f"Round: {round.name}")

    def load_matches(self, tournament_index, tour_index):
        """Load matches for the selected tour."""
        if tournament_index >= 0 and tournament_index < len(self.tournaments_data):
            selected_tournament = self.tournaments_data[tournament_index]
            tours = selected_tournament.rounds
            if tour_index >= 0 and tour_index < len(tours):
                selected_tour = tours[tour_index]
                matches = selected_tour.matches
                for match in matches:
                    print(f"Match: {match.player1} ({match.score1}) vs {match.player2} ({match.score2})")

    def add_tournament(self, name):
        location = input("Entrez le lieu du tournoi: ")
        start_date_str = input("Entrez la date de début du tournoi (YYYY-MM-DD): ")
        end_date_str = input("Entrez la date de fin du tournoi (YYYY-MM-DD): ")
        number_of_rounds = int(input("Entrez le nombre de tours: "))
        description = input("Entrez la description du tournoi: ")

        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

        new_tournament = Tournament(name, location, start_date, end_date, number_of_rounds, description)

        while True:
            national_id = input("Entrez l'identifiant national du joueur à ajouter (ou 'done' pour terminer): ")
            if national_id.lower() == 'done':
                break
            player = next((p for p in self.players_data if p.national_id == national_id), None)
            if player:
                new_tournament.add_player(player)
                print(f"Joueur {player.first_name} {player.last_name} ajouté au tournoi.")
            else:
                print("Joueur non trouvé.")

        self.controller.add_tournament(new_tournament)

    def add_player(self, last_name, first_name, birth_date, national_id):
        self.controller.add_player(last_name, first_name, birth_date, national_id)

    def add_tour(self, tournament_index):
        if tournament_index < 0 or tournament_index >= len(self.tournaments_data):
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

def printTournoiHeader(current_tournament):
    print("\033c", end="")
    if current_tournament:
        print(f"\033[1;30;47mTOURNOI EN COURS: {current_tournament.name}\033[0m")
    else:
        print(f"\033[1;30;47mAUCUN TOURNOI EN COURS\033[0m")

if __name__ == "__main__":
    view = MainView()
    current_tournament = None
    while True:
        '''printTournoiHeader()
        if current_tournament:
            print(f"\033[1;30;47mTOURNOI EN COURS: {current_tournament.name}\033[0m")
        else:
            print(f"\033[1;30;47mAUCUN TOURNOI EN COURS\033[0m")'''
        print("\nOptions:")
        print("1. Charger un tournoi")
        print("2. Charger les matchs")
        print("3. Ajouter un tournoi")
        print("4. Ajouter un joueur")
        print("5. Ajouter un tour au tournoi chargé")
        print("6. Rapport: Liste de tous les joueurs")
        print("7. Quitter")
        choice = input("Choisissez une option (1-7): ")

        if choice == "1":
            tournaments = view.controller.get_all_tournaments()
            if not tournaments:
                print("Aucun tournoi disponible")
            else:
                for i, tournament in enumerate(tournaments):
                    print(f"{i + 1}. {tournament.name}")
                index = int(input("Sélectionnez un tournoi (1-{}): ".format(len(tournaments)))) - 1
                print(" ")
                print(" ")
                printTournoiHeader(tournaments[index])
                if 0 <= index < len(tournaments):
                    current_tournament = tournaments[index]
                    view.filter_players_and_load_tours(index)
                else:
                    print("Index invalide")
        elif choice == "2":
            tournament_index = int(input("Entrez l'index du tournoi: ")) - 1
            tour_index = int(input("Entrez l'index du tour: ")) - 1
            view.load_matches(tournament_index, tour_index)
        elif choice == "3":
            name = input("Entrez le nom du tournoi: ")
            view.add_tournament(name)
        elif choice == "4":
            last_name = input("Entrez le nom de famille du joueur: ")
            first_name = input("Entrez le prénom du joueur: ")
            birth_date = input("Entrez la date de naissance du joueur (YYYY-MM-DD): ")
            national_id = input("Entrez l'identifiant national du joueur: ")
            view.add_player(last_name, first_name, birth_date, national_id)
        elif choice == "5":
            tournament_index = int(input("Entrez l'index du tournoi chargé: ")) - 1
            view.add_tour(tournament_index)
        elif choice == "6":
            for player in view.controller.players_data:
                print(f"Player: {player.first_name} {player.last_name} ({player.national_id})")
        elif choice == "7":
            print("Au revoir!")
            break
        else:
            print("Option invalide, veuillez réessayer.")
