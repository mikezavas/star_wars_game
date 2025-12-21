import random


class StarWarsShip:
    '''
    родительский класс кораблей
    '''

    def __init__(self, title, hp, speed, color, damage, shield):
        self.title = title
        self.hp = hp
        self.speed = speed
        self.color = color
        self.damage = damage
        self.shield = shield
        self.is_alive = True

    def get_damage(self, damage):
        '''
        получение урона
        :param damage: кол-во урона
        '''
        self.hp -= damage
        self._update_alive()

    def _update_alive(self):
        '''
        смотрим, жив ли корабль
        '''
        if self.hp <= 0:
            self.is_alive = False
            print(f"{self.title} is destroyed")

    def get_heal(self, heal):
        '''
        лечит корабль
        :param heal: кол-во, полученного hp
        '''
        if self.is_alive:
            self.hp += heal
            print(f"{self.title} restored {heal} hp")
        else:
            print(f"{self.title} cannot be healed!!")

    def attack(self, target):
        '''
        атакует вражеский корабль
        :param target: цель для атаки
        :return:
        '''
        if self.is_alive and target.is_alive:
            target.get_damage(self.damage)
            print(f"{self.title} attacks {target.title}")

        if not target.is_alive:
            print(f"{target.title} is already dead")

        if not self.is_alive:
            print(f"{self.title} cannot attack")


class XWing(StarWarsShip):
    '''
    истребитель с торпедами
    '''

    def __init__(self, title):
        super().__init__(title, hp=150, speed=200, color="#FF0000", damage=40, shield=50)
        self.torpedoes = 3

    def use_torpedo(self, target):
        if self.torpedoes > 0 and self.is_alive and target.is_alive:
            self.torpedoes -= 1
            target.get_damage(self.damage * 2)
            print(f"{self.title} shot a torpedo at {target.title}")
        else:
            print("The torpedoes are over")


class TIEFighter(StarWarsShip):
    """
    СИД-истребитель, который может уклоняться от атак
    """

    def __init__(self, title):
        super().__init__(title, hp=120, speed=220, color="#FFFFFF", damage=40, shield=50)
        self.evasion = 0.3

    def try_evade(self):
        return random.random() < self.evasion


class DeathStar(StarWarsShip):
    '''
    Звезда смерти - босс, имеет кол-во жизней
    '''

    def __init__(self, tittle):
        super().__init__(tittle, hp=500, speed=50, color="#000000", damage=60, shield=100)
        self.lives = 2

    def regenerate(self):
        if not self.is_alive and self.lives > 0:
            self.lives -= 1
            self.hp = 250
            self.is_alive = True
            print(f"{self.title} comes to life - the fight continues! {self.lives} lives left!")
        elif not self.is_alive and self.lives < 0:
            print(f"{self.title} is defeated!")
        else:
            print(f"{self.title} is alive")
