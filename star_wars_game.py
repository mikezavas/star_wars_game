import random
import time
from ships import XWing, TIEFighter, DeathStar
from game_system import GameSystem


def mission_battle():
    """
    первая ветка: космическая битва:
    игрок управляет кораблями против Death Star
    """
    print("The mission: fight with the Death Star!")
    # создание кораблей игрока
    player1 = XWing("starfighter")
    player2 = XWing("resurgent")
    player3 = XWing("МК75")

    # создание вражеских кораблей
    death_star = DeathStar("Death Star")
    tie1 = TIEFighter("TIE Alfa")
    tie2 = TIEFighter("TIE Beta")

    rebel_ships = [player1, player2, player3]
    imperial_ships = [death_star, tie1, tie2]

    round_num = 1

    # основной цикл битвы
    while (any(s.is_alive for s in rebel_ships) and
           any(s.is_alive for s in imperial_ships)):

        print(f"\nRound {round_num}")

        # ход игрока
        if player1.is_alive:
            print("\nYour actions:")
            print("1.Fight TIE Fighter")
            print("2.Shoot a torpedo at a Death Star")

            choice = input("Choice: ")

            if choice == "1":
                # поиск живых целей
                alive_ties = [s for s in imperial_ships if
                              s.is_alive and isinstance(s, TIEFighter)]
                if alive_ties:
                    target = random.choice(alive_ties)
                    player1.attack(target)
                else:
                    print("Target not found!")
            elif choice == "2":
                if death_star.is_alive:
                    player1.use_torpedo(death_star)
                else:
                    print("The target is destroyed!")
            else:
                print("Wrong choice!")

        # ход союзников
        for ship in [player2, player3]:
            if ship.is_alive:
                alive_enemies = [s for s in imperial_ships if s.is_alive]
                if alive_enemies:
                    target = random.choice(alive_enemies)
                    ship.attack(target)
        # ход врагов
        for ship in imperial_ships:
            if ship.is_alive:
                alive_rebels = [s for s in rebel_ships if s.is_alive]
                if alive_rebels:
                    target = random.choice(alive_rebels)
                    ship.attack(target)
        # регенерация Звезды Смерти
        if not death_star.is_alive:
            death_star.regenerate()

        round_num += 1
        time.sleep(1)
    # проверка победы
    if death_star.lives <= 0 and not death_star.is_alive:
        print("\nVictory! The Death Star has been destroyed!!")
        return True, "Death Star Blueprints"
    else:
        print("\nThe mission failed!")
        return False, None


def mission_training():
    """
    вторая ветка: обучение джедая
    игрок проходит испытания на Дагоба.
    """
    print("Mission: the jedi trials")

    print("Yoda: 'You have to pass the tests'")
    # тест 1: угадывание числа
    print("\nTest 1: Power control")
    secret = random.randint(1, 6)
    print(secret)
    for attempt in range(3):
        try:
            guess = int(input(f"Guess the number from 1 to 7 (try {attempt + 1}/3): "))
            if guess == secret:
                print("Right! The power is strong in you.")
                break
            elif attempt == 2:
                print("You failed the test.")
                return False, None
            else:
                print("Wrong. Try again.")
        except ValueError:
            print("Enter a number!")

        except KeyboardInterrupt:
            print("\nTest interrupted!")
            raise

    print("\nTest 2: Lightsaber combat")
    # тест 2: бой на световых мечах
    player_hp = 60
    droid_hp = 60

    while player_hp > 0 and droid_hp > 0:
        print(f"\nYour hp: {player_hp} | Droid hp: {droid_hp}")
        print("Choose an action: attack, defend, evasion")

        choice = input("Your move: ").lower()
        droid_choice = random.choice(["attack", "defend", "evasion"])

        print(f"Droid: {droid_choice}")

        # логика боя с выбором действий
        if choice == "attack" and droid_choice != "defend":
            droid_hp -= 30
            print("You got it!")
        elif choice == "defend" and droid_choice == "attack":
            print("You blocked the shot!")
        elif choice == "evasion" and droid_choice == "attack":
            print("You evade!")
        elif choice == "evasion" and droid_choice != "attack":
            print("No one is injured: keep going!")

        if droid_hp > 0 and droid_choice == "attack" and choice != "defend":
            player_hp -= 20
            print("The droid attacked you!")

    if player_hp > 0:
        print("\nYou've won! The test is passed.")
        return True, "Lightsaber"
    else:
        print("\nYou've lost. We need to train more.")
        return False, None


def mission_smuggling():
    """
    третья ветка: Контрабандный рейс.
    игрок помогает доставить груз на Татуин.
    """
    print("Mission: Smuggling race")

    print("Han Solo: 'We need to deliver the cargo without the Imperials noticing.'")
    # начальные ресурсы
    credits = 500
    ship_hp = 200
    ship_shield = 50

    print(f"\nYour resources:")
    print(f"Credits {credits}")
    print(f"Ship: hp={ship_hp}, shield={ship_shield}")

    # покупка улучшений
    print("\nWhat will you buy?")
    print("1. Repair kit (+50 hp, 100 credits)")
    print("2. Shield Booster (+30 shield, 150 credits)")
    print("3. Nothing")

    choice = input("Choice: ")

    if choice == "1" and credits >= 100:
        ship_hp += 50
        credits -= 100
        print("A repair kit has been purchased!")
    elif choice == "2" and credits >= 150:
        ship_shield += 30
        credits -= 150
        print("The shield booster is installed!")
    else:
        print("You decided to save money.")

    print("\nThere is an asteroid field ahead!")

    # прохождение астероидного поля
    for i in range(3):
        action = input(f"Sector {i + 1}/3. Where to fly? (left/right/straight): ").lower()

        if random.random() > 0.4:
            print("successful move!")
        else:
            damage = random.randint(20, 40)
            if ship_shield > 0:
                shield_damage = min(damage, ship_shield)
                ship_shield -= shield_damage
                damage -= shield_damage
            ship_hp -= damage
            print(f"Collision! Damage: {damage}")

    if ship_hp <= 0:
        print("\nThe ship has been destroyed! The mission has failed.")
        return False, None

    # избегание патруля
    print("\nImperial patrol! How to evade?")
    print("1. Hyperjump (70% success)")
    print("2. Hide (50% success)")
    print("3. Deceive (30% success)")

    choice = input("Выбор: ")

    success = {"1": 0.7, "2": 0.5, "3": 0.3}

    if random.random() < success.get(choice, 0.5):
        print("Success! You've escaped the patrol.")
        return True, "Map of the Galaxy"
    else:
        print("You've been discovered! The mission has failed.")
        return False, None


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
