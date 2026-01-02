from star_wars_game import mission_battle, mission_training, mission_smuggling
from game_system import GameSystem


def main():
    """
    реализация самой игры
    """
    system = GameSystem()
    print("STAR WARS: Galactic Missions")

    # меню входа/регистрации
    while True:
        print("\n1. Registration")
        print("2. Log in")
        print("3. Exit")

        choice = input("Choice: ")

        if choice == "1":
            if system.register():
                break
        elif choice == "2":
            if system.login():
                break
        elif choice == "3":
            print("May the Force be with you!")
            return
        else:
            print("Wrong choice.")

    # основной игровой цикл
    while True:
        info = system.get_player_info()

        # отображение информации об игроке
        print(f"Player: {system.current_player}")
        print(f"Rank: {info['rank']}")
        print(f"Missions: {info['missions']}")
        print(f"Artifacts: {len(info['artifacts'])}/{8}")

        if info['artifacts']:
            print("Your artifacts:")
            for artifact in info['artifacts']:
                print(f"  - {artifact}")

        # меню выбора миссии
        print("\nChoose a mission:")
        print("1. Space Battle (difficult)")
        print("2. Jedi Test (medium)")
        print("3. Smuggled Flight (medium)")
        print("4. Exit")

        choice = input("\nYour choice: ")

        success = False
        artifact = None

        # запуск выбранной миссии
        if choice == "1":
            success, artifact = mission_battle()
        elif choice == "2":
            success, artifact = mission_training()
        elif choice == "3":
            success, artifact = mission_smuggling()
        elif choice == "4":
            print("I'm going back to the base")
            break
        else:
            print("Wrong choice.")
            continue

        # обработка результатов миссии
        if success and artifact:
            print(f"\nMission accomplished! You get artifact: {artifact}")
            info = system.get_player_info()
            # проверка наличия артефакта у игрока
            if artifact in info['artifacts']:
                print(f"\nYou already have this artifact!")
                print("Looking for alternative artifact")

                alternative_artifact = system.get_alternative_artifact(artifact)
                print(f"You receive alternative artifact: {alternative_artifact}")

                # предложение сохранить альтернативный артефакт
                save = input(f"Add artifact '{alternative_artifact}' to your collection? (yes/no): ").lower()

                if save == "yes":
                    if system.add_artifact_to_player(alternative_artifact):
                        print(f"Artifact '{alternative_artifact}' added to your collection!")

                        # проверка завершения коллекции
                        new_info = system.get_player_info()
                        print(f"\nProgress: {len(new_info['artifacts'])}/8 artifacts collected")

                        if len(new_info['artifacts']) == 8:
                            print("\nYou've collected all artifacts!")
                            print("You are now a true Jedi Master!")
                    else:
                        print("Failed to save artifact.")
                else:
                    print("The artifact was left behind.")
            else:
                print(f"\nAdding artifact '{artifact}' to your collection")
                if system.add_artifact_to_player(artifact):
                    print(f"Artifact '{artifact}' successfully added!")

                    # проверка завершения коллекции
                    new_info = system.get_player_info()
                    print(f"\nProgress: {len(new_info['artifacts'])}/8 artifacts collected")

                    if len(new_info['artifacts']) == 8:
                        print("You've collected ALL artifacts!")
                        print("You are now a true Jedi Master!")
                else:
                    print("Failed to add artifact.")

        elif not success:
            print("\nThe mission failed. Try again!")

        input("\nPress Enter to continue")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nThe game is interrupted.")
    except Exception as e:
        print(f"Mistake: {e}")
