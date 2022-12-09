import os
import random

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Item:
    def __init__(self, name, desc, damage=0, value=0, defense =0):
        self.name = name
        self.desc = desc
        self.loc = None
        self.damage = damage
        self.value = value

    def __str__(self):
        return "{}\n=====\n{}\nValue: {}\n".format(self.name, self.desc, self.value)

    def describe(self):
        clear()
        print(self.desc)
        input("Press enter to continue...")
    def put_in_room(self, room):
        self.loc = room
        room.add_item(self)    

################################################
# Weapons
class Weapon(Item):
    def __init__(self, name, desc, damage, value):
        super().__init__(name, desc, damage, value)
        self.damage = damage
    def __str__(self):
            return "{}\n=====\n{}\nValue: {}\nDamage: {}".format(self.name, self.desc, self.value, self.damage)

class Rock(Weapon):
    def __init__(self):
        super().__init__(name = "Rock", desc= "A dull rock for bludgeoning", damage = 5, value = None)
    def __repr__(self):
        return self.name
class PocketKnife(Weapon):
    def __init__(self):
        super().__init__(name="Pocketknife",desc= "a small pocketknife", damage = 7, value = 5)
    def __repr__(self):
        return self.name
class Machete(Weapon):
    def __init__(self):
        super().__init__(name="Machete",desc= "a machete good for hacking mosters to death", damage = 15, value = 10)
    def __repr__(self):
        return self.name

################################################
# Armor
class Armor(Item):
    def __init__(self, name, desc, value, defense):
        super().__init__(name, desc, value, defense)
        self.defense = defense
    def __str__(self):
            return "{}\n=====\n{}\nValue: {}\nDamage: {}".format(self.name, self.desc, self.value, self.defense)

class BrestPlate(Armor):
    def __init__(self):
        super().__init__(name = "Brest Plate", desc= "A brest plate made of Iron", defense = 5, value = 5)
    def __repr__(self):
        return self.name
class Helmet(Armor):
    def __init__(self):
        super().__init__(name = "Helmet", desc= "A helmet made of Iron", defense = 3, value = 5)
    def __repr__(self):
        return self.name
class WristGuards(Armor):
    def __init__(self):
        super().__init__(name = "Wrist Guards", desc= "wrist guards made of Iron", defense = 3, value = 5)
    def __repr__(self):
        return self.name

################################################
# Key 
class Key(Item):
    def __init__(self):
        super().__init__(name="Key", desc="A small golden key! I wonder what it unlocks?")
        self.key = True