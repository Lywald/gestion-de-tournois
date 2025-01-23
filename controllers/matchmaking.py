from models.round import Round
import random
from models.match import Match


class Matchmaking:
    """
    A class to handle matchmaking logic for tournaments.
    Methods:
        __init__(menu_view): Initialize the matchmaking with a MenuView instance.
        create_matches(players): Create matches for a given list of players.
        run_tournament(tournament): Run the tournament round by round.
    """

    def __init__(self, menu_view):
        self.menu_view = menu_view

    def create_matches(self, players):
        """
        Create matches for a given list of players.
        Args:
            players (list): A list of Player objects.
        Returns:
            list: A list of Match objects.
        """
        matches = []
        random.shuffle(players)  # Shuffle players for the first round
        for i in range(0, len(players) - 1, 2):
            player1 = players[i]
            player2 = players[i + 1]
            score1, score2 = self.assign_scores(player1, player2)
            matches.append(Match(player1, score1, player2, score2))

        # Handle odd player count by pairing the last player with a "bye" (free win)
        if len(players) % 2 == 1:
            last_player = players[-1]
            matches.append(Match(last_player, 1, None, 0))  # Last player gets a free win

        return matches

    def assign_scores(self, player1, player2):
        """
        Assign scores to players for a match.
        Args:
            player1 (Player): The first player.
            player2 (Player): The second player.
        Returns:
            tuple: A tuple containing the scores of player1 and player2.
        """
        winner = random.choice([player1, player2])  # Randomly choose a winner for demonstration
        if winner == player1:
            return 1, 0  # Player 1 wins
        else:
            return 0, 1  # Player 2 wins

    def run_tournament(self, tournament):
        """
        Run the tournament round by round.
        Args:
            tournament (Tournament): The tournament object.
        Returns:
            list: A list of winners for each round.
        """
        all_round_winners = []
        for round_number in range(tournament.number_of_rounds):
            self.menu_view.print_message(f"Début du tour {round_number + 1}")

            # Create matches for this round
            matches = self.create_matches(tournament.players)
            new_round = Round(name=f"Tour {round_number + 1}")
            new_round.matches = matches
            tournament.add_round(new_round)

            # Update player scores based on match results
            self.update_player_scores(matches)

            # Sort players by points for the next round
            tournament.players.sort(key=lambda p: p.tournament_points, reverse=True)

            # Determine the winners of this round
            round_winners = self.determine_round_winners(matches)

            # Add the winners of this round to the global list
            all_round_winners.append(round_winners)

            # Display the winners of this round
            self.display_round_winners(round_number, round_winners)

        # Display the final scores of the tournament
        self.display_final_scores(tournament)

        return all_round_winners

    def determine_round_winners(self, matches):
        """
        Determine the winners of the current round's matches.
        Args:
            matches (list): A list of Match objects.
        Returns:
            list: A list of winners for the current round.
        """
        round_winners = []
        for match in matches:
            if match.player2 is None:  # Bye match
                round_winners.append(match.player1)
                self.menu_view.print_message(
                    f"Gagnant du match (exempté): {match.player1.first_name} {match.player1.last_name}"
                )
            elif match.score1 > match.score2:
                round_winners.append(match.player1)  # Player 1 wins
                self.menu_view.print_message(
                    f"Gagnant du match: {match.player1.first_name} {match.player1.last_name}"
                )
            elif match.score2 > match.score1:
                round_winners.append(match.player2)  # Player 2 wins
                self.menu_view.print_message(
                    f"Gagnant du match: {match.player2.first_name} {match.player2.last_name}"
                )
            else:
                # In case of a draw, both players are considered winners
                round_winners.extend([match.player1, match.player2])
                self.menu_view.print_message(
                    f"Égalité: {match.player1.first_name} {match.player1.last_name} "
                    f"et {match.player2.first_name} {match.player2.last_name}"
                )
        return round_winners

    def display_round_winners(self, round_number, round_winners):
        """
        Display the winners of the current round.
        Args:
            round_number (int): The round number.
            round_winners (list): A list of winners for the current round.
        """
        winner_names = ", ".join(f"{winner.first_name} {winner.last_name}" for winner in round_winners)
        self.menu_view.print_message(f"Gagnant(s) du tour {round_number + 1}: {winner_names}")

    def display_final_scores(self, tournament):
        """
        Display the final scores of the tournament.
        Args:
            tournament (Tournament): The tournament object.
        """
        self.menu_view.print_message("Tournoi terminé. Scores finaux :")
        for player in tournament.players:
            self.menu_view.print_message(f"{player.first_name} {player.last_name} : {player.tournament_points} points")

    def update_player_scores(self, matches):
        """
        Update the scores of players based on the match results.
        Args:
            matches (list): A list of Match objects.
        """
        for match in matches:
            if match.player2 is not None:  # Skip bye matches
                match.player1.tournament_points += match.score1
                match.player1.total_points += match.score1
                match.player2.tournament_points += match.score2
                match.player2.total_points += match.score2
            else:
                match.player1.tournament_points += 1  # Bye match gives 1 point
                match.player1.total_points += 1
