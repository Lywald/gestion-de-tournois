from controller import Controller
from view import MenuView

if __name__ == "__main__":
    menu_view = MenuView()
    controller = Controller(menu_view)
    current_tournament = None

    print("Bienvenue dans le gestionnaire de tournois d'échecs!")

    while True:
        choice = menu_view.main_menu(controller, current_tournament)

        if choice == 0:
            controller.handle_choice_0()
        elif choice == 1:
            current_tournament = controller.handle_choice_1(current_tournament)
        elif choice == 2:
            controller.handle_choice_2(current_tournament)
        elif choice == 3:
            controller.handle_choice_3()
        elif choice == 4:
            controller.handle_choice_4(current_tournament)
        elif choice == 5:
            controller.handle_choice_5(current_tournament)
        elif choice == 6:
            controller.handle_choice_6(current_tournament)
        elif choice == 7:
            if not controller.handle_choice_7():
                break
        else:
            print("Option invalide, veuillez réessayer.")
