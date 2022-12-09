import updater
from random import randint, random
from player import *

class Monster:
    def __init__(self, name, attack, defense, health, room, exp):
        self.name = name
        self.attack = attack
        self.defense = defense
        self.health = health
        self.max_health = health
        self.room = room
        self.exp = exp
        room.add_monster(self)
        updater.register(self)
    def __repr__(self):
        return(f"This monster is a {self.name}, Attack: {self.attack}, Defense: {self.defense}, HP = {self.health}/{self.max_health}")
    def update(self):
        if randint(0,1) < .5: # 50% change the monster stays in a room verses leaves
            self.move_to(self.room.random_neighbor())
    def move_to(self, room):
        self.room.remove_monster(self)
        self.room = room
        room.add_monster(self)
    def is_alive(self):
        return self.health > 0
    def die(self):
        self.room.remove_monster(self)
        updater.deregister(self)
    def attack_player(self, player):
            return (player.lose_health(self.attack))
    def lose_health(self, damage):
        if damage <= 0:
            damage = 1
        print(f"{self.name} takes {damage} damage!")
        if self.defense - damage >= 0:
            self.defense -= damage
        else:
            self.health -= damage
        if self.health <= 0:
            self.health = 0
            print(f"You have defeated {self.name}!")
            return False
        else:
            print (f"{self.name} has {self.health}/{self.max_health} HP remaining \nDefense remaining: {self.defense}")
            return True

# Spawn Monsters
monster_names_list = ['Slime', 'Wolf', 'Undead', 'Goblin', 'Bandit', 'Zombie', 'Ghoul', 
                'Orc', 'Dark Knight', 'Gremlin', 'Werewolf', 'Golem', 'Witch', 'Valkyrie',
                'Vampire', 'Chimera', 'Giant', 'Dragon', 'Minotaur', 'Devil', 'Demon']
def spawn_monster(room, level):
    match level: #c there are three levels of monsters 1 is the easist to defeat, 2 medium, 3 hard 
        case 1:
            index = randint(0,6)
            weak_attack = randint(2,4)
            weak_defense = randint(0,3)
            weak_health = randint(10,15)
            # name, attack, defense, health, room, exp
            return Monster(monster_names_list[index], weak_attack, weak_defense, weak_health, room, 5)
        case 2:
            index = randint(7,13)
            med_attack = randint(4,6)
            med_defense = randint(3,5)
            med_health = randint(15,25)
            return Monster(monster_names_list[index], med_attack, med_defense, med_health, room, 10)
        case 3:
            index = randint(14,20)
            hard_attack = randint(6,10)
            hard_defense = randint(5,15)
            hard_health = randint(25,40)
            return Monster(monster_names_list[index], hard_attack, hard_defense, hard_health, room, 15)

# Randomly determine if a monster is present in a room or not.
# def random_spawn_monster():
#     if randint(0, 10) > 3:
#         return True
#     else:
#         return False