import os
import sys

if os.name == 'nt':
    import msvcrt
else:
    import tty
    import termios

from controller import Controller


class MenuView:
    """
    Menu view for displaying and navigating the main menu.
    Methods:
        __init__(): Initialize the menu view.
        print_header(current_tournament): Print the header for the menu.
        get_key(): Get a single key press from the user.
        main_menu(controller, current_tournament): Display the main menu and handle user input.
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
            "\tCharger un tournoi",
            "\tCharger les matchs",
            "\tAjouter un tournoi",
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


def handle_choice_0(controller, menu_view, current_tournament):
    tournaments = controller.get_all_tournaments()
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
            controller.filter_players_and_load_tours(index)
        else:
            print("Index invalide")
        input()
    return current_tournament


def handle_choice_1(controller):
    tournament_index = int(input("Entrez l'index du tournoi: ")) - 1
    tour_index = int(input("Entrez l'index du tour: ")) - 1
    controller.load_matches(tournament_index, tour_index)


def handle_choice_2(controller):
    print()
    name = input("Entrez le nom du tournoi: ")
    controller.add_tournament(name)


def handle_choice_3(controller):
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
    controller.add_player(last_name, first_name, birth_date, national_id)


def handle_choice_4(controller):
    tournament_index = int(input("Index du tournoi chargé: ")) - 1
    controller.add_tour(tournament_index)


def handle_choice_5(controller, current_tournament):
    if current_tournament is None:
        print("Tournoi non sélectionné")
        input()
    else:
        tournament_index = controller.tournaments_data.index(current_tournament)
        controller.run_tournament(tournament_index)


def handle_choice_6(controller):
    controller.display_reports()


def handle_choice_7():
    print("Au revoir!")
    return False


if __name__ == "__main__":
    controller = Controller()
    menu_view = MenuView()
    current_tournament = None

    print("Bienveue dans le gestionnaire de tournois d'échecs!")

    while True:
        choice = menu_view.main_menu(controller, current_tournament)

        if choice == 0:
            current_tournament = handle_choice_0(controller, menu_view, current_tournament)
        elif choice == 1:
            handle_choice_1(controller)
        elif choice == 2:
            handle_choice_2(controller)
        elif choice == 3:
            handle_choice_3(controller)
        elif choice == 4:
            handle_choice_4(controller)
        elif choice == 5:
            handle_choice_5(controller, current_tournament)
        elif choice == 6:
            handle_choice_6(controller)
        elif choice == 7:
            if not handle_choice_7():
                break
        else:
            print("Option invalide, veuillez réessayer.")
