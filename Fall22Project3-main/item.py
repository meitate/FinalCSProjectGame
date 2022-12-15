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
        
    def format_item(item):
        return "{0} {1}\n".format(item['count'], item['name'])

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
        super().__init__(name="Machete",desc= "a machete good for hacking mosters to death", damage = 10, value = 10)
    def __repr__(self):
        return self.name
class OPWeapon(Weapon):
    def __init__(self):
        super().__init__(name="Lightsaber",desc= "a OP weapon for serious players", damage = 20, value = 50)
    def __repr__(self):
        return self.name
################################################
# Armor
class Armor(Item):
    def __init__(self, name, desc, defense, value):
        super().__init__(name, desc, defense, value)
        self.defense = defense
    def __str__(self):
            return "{}\n=====\n{}\nValue: {}\nDamage: {}".format(self.name, self.desc, self.value, self.defense)

class BrestPlate(Armor):
    def __init__(self):
        super().__init__(name = "Brest Plate", desc= "A brest plate made of Iron",  value = 5, defense = 5)
    def __repr__(self):
        return self.name
class Helmet(Armor):
    def __init__(self):
        super().__init__(name = "Helmet", desc= "A helmet made of Iron", value = 6, defense = 3)
    def __repr__(self):
        return self.name
class WristGuards(Armor):
    def __init__(self):
        super().__init__(name = "Wrist Guards", desc= "wrist guards made of Iron", value = 5, defense = 3)
    def __repr__(self):
        return self.name

################################################
# Key + Locked stuff 
class Key(Item):
    def __init__(self):
        super().__init__(name="Key", desc="A small golden key! I wonder what it unlocks?")
        self.key = True
    def __repr__(self) -> str:
        return self.name

opweapon = OPWeapon()
class LockBox(Item):
    def __init__(self):
        super().__init__(name = "lock box", desc = "A locked box! I wonder what's inside?\nOnce opened I could use this as a detachable storage unit!")
        self.storage = [opweapon]
        self.locked = True
        self.size_limit = 4 # fits 5 items since the list index starts at 0
        self.space_left = self.size_limit - len(self.storage) 

    def unlock(self):
        clear()
        print("This lock box unlocks if you write the correct answer to this riddle:")
        answer = input("What four-letter word can be written forward, backward, or upside down, and can still be read from left to right?\n")
        if str(answer) == "NOON":
            self.locked = False
            print("Lock box has been unlocked. Type 'open lock box' to see your options")
            input("Press enter to continue...")
        elif str(answer).upper() == "NOON":
            print("Almost right, case matters here!")
            input("Press enter to continue...")
        else:
            print("Wrong answer")
            input("Press enter to continue...")
    def __repr__(self):
        return self.name
    def add_item(self, item):
        if len(self.storage) < self.size_limit:
            self.storage.append(item)
    def remove_item(self, item):
        self.storage.remove(item)
    def get_item_by_name(self, name):
        for i in self.storage:
            if i.name.lower() == name.lower():
                return i
        return False
    def show_inventory(self):
        clear()
        print("This lock box contains:")
        for i in self.storage:
            print(i.name)
        input("Press enter to continue...")
    def menu_choice(self,player):
        opened = True
        while opened:
            try:
                box_choice = int(input("What do you want to do: [1]add items [2]remove items [3]display the contents [4]exit?\n"))
                if box_choice == 3:
                    self.show_inventory()
                    opened = False
                elif box_choice == 4:
                    opened = False
                elif box_choice == 1:
                    item = str(input("What do you want to put in the lock box that is currently in your inventory?\n"))
                    checkitem = player.get_item_by_name(item)
                    if checkitem != False:
                        print(f"You put {checkitem.name} from your inventory into the lockbox, you can put {self.space_left} more items in the box")
                        self.add_item(checkitem)
                        player.remove_item(checkitem)
                        input("Press enter to continue...")
                        opened = False
                    else:
                        print("No such item.")
                        input("Press enter to continue...")
                        opened = False
                else:
                    item = str(input("What do you want to remove from the lock box and put it in your inventory?\n"))
                    checkitem = self.get_item_by_name(item)
                    if checkitem != False:
                        print(f"You added {checkitem.name} to your inventory from the lockbox, it now has {self.space_left} item capacity")
                        self.remove_item(checkitem)
                        player.add_item(checkitem)
                        input("Press enter to continue...")
                        opened = False
                    else:
                        print("No such item.")
                        input("Press enter to continue...")
                        opened = False
            except ValueError:
                clear()
                print("Sorry I didn't get that please try again.\n")