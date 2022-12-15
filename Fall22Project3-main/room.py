from random import randint
from item import *
import time

class Room:
    def __init__(self, description):
        self.desc = description
        self.monsters = []
        self.npcs = []
        self.exits = []
        self.items = []
    def add_exit(self, exit_name, destination):
        if exit_name not in self.exits:
            self.exits.append([exit_name, destination])
            return True
        else:
            return False
    def get_destination(self, direction):
        for e in self.exits:
            if e[0] == direction:
                return e[1]
        return None
    def connect_rooms(room1, dir1, room2, dir2):
        #creates "dir1" exit from room1 to room2 and vice versa
        room1.add_exit(dir1, room2)
        room2.add_exit(dir2, room1)
    def exit_names(self):
        return [x[0] for x in self.exits]
    def add_item(self, item):
        self.items.append(item)
    def remove_item(self, item):
        self.items.remove(item)
    def add_monster(self, monster):
        self.monsters.append(monster)
    def remove_monster(self, monster):
        self.monsters.remove(monster)
    def add_npc(self,npc):
        self.npcs.append(npc)
    def remove_npc(self,npc):
        self.npcs.remove(npc)
    def has_items(self):
        return self.items != []
    def get_item_by_name(self, name):
        for i in self.items:
            if i.name.lower() == name.lower():
                return i
        return False
    def has_monsters(self):
        return self.monsters != []
    def get_monster_by_name(self, name):
        for i in self.monsters:
            if i.name.lower() == name.lower():
                return i
        return False
    def random_neighbor(self):
        return random.choice(self.exits)[1]
    def has_npcs(self):
        return self.npcs != []
    def get_npc_by_name(self, name):
        for i in self.npcs:
            if i.name.lower() == name.lower():
                return i
        return False

class IntroRoom(Room):
    def __init__(self):
        super().__init__(description ="Starting room \nHello! Quick tip before you jump into the game! Type 'help' in to your terminal to get a display of actions you can take")

class Store(Room): # all store interactions are done via the store clerk in npcs
    def __init__(self):
        super().__init__(description="Welcome to the store here you can buy potions and gear for your adventures")

###############################################################################
# LOCKED ROOMS

class LockedRoom(Room):
    def __init__(self):
        super().__init__(description="A room with a locked door, you need a key to enter!")
        self.opened = False
        self.locked = True
    def unlock_room(self):
        if self.opened == False and self.locked==True:
            clear()
            self.opened = True
            self.locked = False
            print("The door unlocks and you step inside!")
            input("Press enter to continue...")
        return

class LockedDoorWithKeypad(Room):
    def __init__(self):
        super().__init__(description="A locked door with a keypad")
        self.unlock_code = 123456
        self.opened = False
        self.locked = True
        self.box = True
    def password_unlock(self):
        if self.opened == False and self.locked == True:
            while True:
                code = input("Input Password: ****** (or type 'cancel')\n")
                if (code == None) or (code.lower() == "cancel"):
                    print("Canceling request")
                    time.sleep(1)
                    return
                try:
                    intcode = int(code)
                except:
                    clear()
                    print("Keypad code not acccepted.")
                    continue
                if intcode != self.unlock_code:
                    clear()
                    print("Keypad code not acccepted.")
                    continue
                break
            clear()
            print("Keypad code accepted!")
            input("Press enter to open door...")
            clear()
            print("You open the door and find a little lock box inside. Ugh yet another locked item!")
            input("Press enter to continue...")
            #self.description = "A unlocked door with keypad"
            self.locked = False
            self.opened = True
        else:
            self.box = False
            clear()
            print("\nYou already unlocked the door in this room.")
            input("Press enter to continue...")

###############################################################################
# REGENERATION ROOM
class Regeneration(Room):
    def __init__(self):
        super().__init__(description = "You have entered a room where you can regenerate health")
        self.healing = True
        
    def player_regenerate(self, player):
        try:
            while self.healing == True:
                print("Press Ctrl-C to stop regeneration")
                if player.health < player.max_health:
                    player.health += 1
                    self.healing = True
                    print(f"{player.name}'s HP is now: {player.health}/{player.max_health}")
                    time.sleep(1)
                    clear()
                else:
                    print("You already have max health")
                    self.healing = False
        except KeyboardInterrupt:
            pass