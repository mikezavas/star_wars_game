import json
import os
from getpass import getpass
import random


class GameSystem:
    def __init__(self):
        self.players_file = "players.json"
        self.artifacts_file = "artifacts.json"
        self.current_player = None  # текущий авторизованный игрок
        self._init_files()

    def _init_files(self):
        '''
        инициализация файлов сохранения
        '''
        if not os.path.exists(self.players_file):
            with open(self.players_file, 'w') as file:
                json.dump({}, file) # создаем пустой файл игроков

        if not os.path.exists(self.artifacts_file):
            artifacts = [
                "The Kayber Crystal",  # "Кристалл Кайбера"
                "Lightsaber",  # "Световой меч"
                "Holocron of the Jedi",  # "Голокрон джедаев"
                "Death Star Blueprints",  # "Чертежи Звезды Смерти"
                "Key to the Temple",  # "Ключ от храма"
                "Shield of the Mandalorian",  # "Щит мандалорца"
                "Droid R2",  # "Дроид R2"
                "Map of the Galaxy"  # "Карта Галактики"
            ]
            with open(self.artifacts_file, 'w') as file:
                json.dump(artifacts, file)

    def register(self):
        '''
        Регистрация игрока
        '''
        print("-Registration-")
        username = input("Enter your nickname: ")
        password = getpass("Enter your password: ")

        with open(self.players_file, 'r') as file:
            players = json.load(file)

        if username in players:
            print("This nickname is already taken")
            return False

        players[username] = {
            "password": password,
            "artifacts": [],
            "rank": "Private",
            "missions": 0
        }

        with open(self.players_file, 'w') as file:
            json.dump(players, file)

        self.current_player = username
        print(f"Welcome, {username}!")
        return True

    def login(self):
        """
        Вход в систему
        """
        print("Log in to the system")
        username = input("nickname: ")
        password = getpass("password: ")

        with open(self.players_file, 'r') as file:
            players = json.load(file)

        if username not in players or players[username]["password"] != password:
            print("Incorrect data")
            return False

        self.current_player = username
        print(f"Welcome back, {username}")
        return True

    def add_artifact_to_player(self, artifact_name):
        """
        Добавляем артефакт игроку
        """
        if self.current_player is None:
            print("No player is logged in!")
            return False

        with open(self.players_file, 'r') as file:
            players = json.load(file)

        # Проверяем, есть ли уже этот артефакт
        if artifact_name in players[self.current_player]["artifacts"]:
            print(f"You already have the artifact: {artifact_name}")
            return False

        players[self.current_player]["artifacts"].append(artifact_name)
        players[self.current_player]["missions"] += 1

        # обновление ранга в зависимости от количества артефактов
        artifact_count = len(players[self.current_player]["artifacts"])
        if artifact_count >= 6:
            players[self.current_player]["rank"] = "Jedi Master"
        elif artifact_count >= 4:
            players[self.current_player]["rank"] = "Jedi Knight"
        elif artifact_count >= 2:
            players[self.current_player]["rank"] = "Padawan"
        else:
            players[self.current_player]["rank"] = "Initiate"

        try:
            with open(self.players_file, 'w') as file:
                json.dump(players, file, indent=4)
            return True
        except Exception as e:
            print(f"Error saving player data: {e}")
            return False


    def get_available_artifacts(self):
        """
        Получаем список доступных артефактов (тех, которых нет у игрока)
        """
        if self.current_player is None:
            return []

        with open(self.players_file, 'r') as file:
            players = json.load(file)

        with open(self.artifacts_file, 'r') as file:
            all_artifacts = json.load(file)

        player_artifacts = players[self.current_player]["artifacts"]
        available_artifacts = [a for a in all_artifacts if a not in player_artifacts]

        return available_artifacts

    def get_random_artifact(self):
        """
        Получаем случайный артефакт из доступных
        """
        available_artifacts = self.get_available_artifacts()

        if not available_artifacts:
            print("You have collected all artifacts!")
            # генерация новых артефактов при сборе всех старых
            new_artifacts = [
                "New Crystal",  # "Новый кристалл"
                "Ancient Scroll",  # "Древний свиток"
                "Imperial Technology",  # "Технология имперцев"
                "Sector Map",  # "Карта сектора"
                "The key to the base",  # "Ключ от базы"
                "Shield matrix",  # "Щитовая матрица"
                "Hyperdrive core",  # "Ядро гипердвигателя"
                "Intelligence data"  # "Данные разведки"
            ]

            with open(self.artifacts_file, 'w') as file:
                json.dump(new_artifacts, file)

            return random.choice(new_artifacts)

        return random.choice(available_artifacts)

    def get_alternative_artifact(self, current_artifact):
        """
        Получаем альтернативный артефакт, если текущий уже есть у игрока
        """
        available_artifacts = self.get_available_artifacts()

        if current_artifact in available_artifacts:
            available_artifacts.remove(current_artifact)

        if not available_artifacts:
            print("You have collected all available artifacts!")
            special_artifacts = [
                "Special Force Crystal",
                "Legendary Lightsaber",
                "Ancient Jedi Holocron",
                "Mandalorian Beskar Armor",
                "Sith Artifact",
                "Millennium Falcon Model"
            ]
            return random.choice(special_artifacts)

        return random.choice(available_artifacts)

    def get_player_info(self):
        """
        получаем информацию об игроке
        """
        if self.current_player is None:
            return None

        with open(self.players_file, 'r') as file:
            players = json.load(file)

        return players.get(self.current_player, {})
