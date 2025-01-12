from models.round import Round


"""

GÉNÉRATION DES PAIRES
● Au début du premier tour, mélangez tous les joueurs de façon aléatoire.
● Chaque tour est généré dynamiquement en fonction des résultats des joueurs dans
le tournoi en cours.
○ Triez tous les joueurs en fonction de leur nombre total de points dans le
tournoi.
○ Associez les joueurs dans l’ordre (le joueur 1 avec le joueur 2, le joueur 3
avec le joueur 4 et ainsi de suite.)
○ Si plusieurs joueurs ont le même nombre de points, vous pouvez les choisir
de façon aléatoire.
○ Lors de la génération des paires, évitez de créer des matchs identiques
(c’est-à-dire les mêmes joueurs jouant plusieurs fois l’un contre l’autre).
■ Par exemple, si le joueur 1 a déjà joué contre le joueur 2,
associez-le plutôt au joueur 3.
● Mettez à jour les points de tous les joueurs après chaque tour et répétez le
processus de triage et d’association jusqu'à ce que le tournoi soit terminé.
● Un tirage au sort des joueurs définira qui joue en blanc et qui joue en noir ; il n'est
donc pas nécessaire de mettre en place un équilibrage des couleurs.

DÉROULEMENT DE BASE DU TOURNOI
● Un tournoi a un nombre de tours défini.
● Chaque tour est une liste de matchs.
○ Chaque match consiste en une paire de joueurs.
● À la fin du match, les joueurs reçoivent des points selon leurs résultats.
○ Le gagnant reçoit 1 point.
○ Le perdant reçoit 0 point.

"""

import random
from models.match import Match


class Matchmaking:
    """
    A class to handle matchmaking logic for tournaments.
    Methods:
        create_matches(players): Create matches for a given list of players.
        run_tournament(tournament): Run the tournament round by round.
    """

    @staticmethod
    def create_matches(players):
        """
        Create matches for a given list of players.
        Args:
            players (list): A list of Player objects.
        Returns:
            list: A list of Match objects.
        """
        matches = []
        random.shuffle(players)
        for i in range(0, len(players), 2):
            if i + 1 < len(players):
                player1 = players[i]
                player2 = players[i + 1]
                score1, score2 = Matchmaking.assign_scores(player1, player2)
                matches.append(Match(player1, score1, player2, score2))
        return matches

    @staticmethod
    def assign_scores(player1, player2):
        """
        Assign scores to players for a match.
        Args:
            player1 (Player): The first player.
            player2 (Player): The second player.
        Returns:
            tuple: A tuple containing the scores of player1 and player2.
        """
        winner = random.choice([player1, player2])
        if winner == player1:
            return 1, 0
        else:
            return 0, 1

    @staticmethod
    def run_tournament(tournament):
        """
        Run the tournament round by round.
        Args:
            tournament (Tournament): The tournament object.
        """
        for round_number in range(tournament.number_of_rounds):
            print(f"Starting Round {round_number + 1}")
            matches = Matchmaking.create_matches(tournament.players)
            new_round = Round(name=f"Round {round_number + 1}")
            new_round.matches = matches
            tournament.add_round(new_round)
            Matchmaking.update_player_scores(matches)
            tournament.players.sort(key=lambda p: p.total_points, reverse=True)
            print(f"Round {round_number + 1} completed")

        print("Tournament completed. Final scores:")
        for player in tournament.players:
            print(f"{player.first_name} {player.last_name}: {player.total_points} points")

    @staticmethod
    def update_player_scores(matches):
        """
        Update the scores of players based on the match results.
        Args:
            matches (list): A list of Match objects.
        """
        for match in matches:
            match.player1.total_points += match.score1
            match.player2.total_points += match.score2
