import os
import sys

if os.name == 'nt':
    import msvcrt
else:
    import tty
    import termios


class MenuView:
    """
    Menu view for displaying and navigating the main menu.
    Methods:
        __init__(): Initialize the menu view.
        print_header(current_tournament): Print the header for the menu.
        get_key(): Get a single key press from the user.
        main_menu(controller, current_tournament): Display the main menu and handle user input.
        print_message(message): Print a message to the console.
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
            print(f"\t\tTOURNOI OUVERT: {current_tournament.name}\t\t")
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

    def main_menu(self, controller, current_tournament):
        """
        Show the main menu and let the user navigate with arrow keys.
        Args:
            controller: The controller object to manage the data.
            current_tournament: The current tournament object to show in the header.
        Returns:
            int: The index of the selected menu option.
        Navigation:
            - Use the up arrow key to move up.
            - Use the down arrow key to move down.
            - Press Enter to select the highlighted option.
        """
        options = [
            "\tCréer un tournoi",
            "\tCharger un tournoi",
            "\tAfficher les matchs",
            "\tAjouter un joueur",
            "\tAjouter un tour au tournoi chargé",
            "\tLancer le tournoi",
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

    def display_winner(self, round_number, winners):
        """
        Display the winner(s) of a round.
        Args:
            round_number (int): The round number.
            winners (list): A list of players who won the round.
        """
        winner_names = ", ".join(f"{winner.first_name} {winner.last_name}" for winner in winners)
        print(f"Gagnant(s) du tour {round_number}: {winner_names}")

    def print_message(self, message):
        """
        Print a message to the console.
        Args:
            message (str): The message to print.
        """
        print(message)
