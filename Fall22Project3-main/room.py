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
        self.exits.append([exit_name, destination])
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

###############################################################################
# # STORE (not implimented yet)
class Store(Room):
    def __init__(self):
        super().__init__(description="Welcome to the store here you can buy potions and gear for your adventures")
        self.store_weapons = {1:Machete(), 2:PocketKnife()}
        self.store_armor = {1:Helmet(), 2:WristGuards()}

    def shop(self,player):
        shopping = True
        while shopping:
            clear()
            decision = int(input('Get: 1. Potions\n2. Weapons\n3. Armor\n4. Leave Shop'))
            match decision:
                case 1: # Buying potions
                    potions_to_buy = int(input(f"You have {player.potions} potions and {player.money} coins, how many potions would you like to buy?"))
                    if potions_to_buy == 0:
                        print("Next time please buy something!")
                        input("Press Enter to go back to the Store.")
                        continue
                    if potions_to_buy > 10: potions_to_buy = 10; print("You can't carry more than 10 potions we will assume you want 10 potions")
                    if player.potions + potions_to_buy > 10: potions_to_buy = potions_to_buy - player.potions; print("You don't have space on your inventory for that amount of potions, we will max out your potions to 10.")
                    if (potions_to_buy * 5) > player.money:
                        print("You don't have enough money to buy that many potions, please select a lower number.")
                        input("Press Enter to go back to the Store.")
                        continue
                    else:
                        player.potions += potions_to_buy
                        player.money -= potions_to_buy * 5
                        print(f"Thanks for your purchase! you now have {player.potions} potions\nCome back soon!")
                        input("Press Enter to go back to the Store.")
                        continue
                case 2:
                    weapon_to_buy = ""
                    print(f"You have {player.money} coins, what weapon do you want to buy?\n")
                    for key, item in self.store_weapons.items():
                        print(f"[{key}] {item.name}: ${item.value}\n")
                    weapon_to_buy = input("Type the number of the weapon you want to buy:")
                    if int(weapon_to_buy) not in self.store_weapons.keys():
                        print("The store doesn't have this item")
                        input("Press Enter to go back to the Store.")
                        continue
                    else:
                        weapon = self.store_weapons[weapon_to_buy]
                        if weapon.value > player.money:
                            print("You don't have enough money to buy that many potions, please select a lower number.")
                            input("Press Enter to go back to the Store.")
                            continue
                        elif weapon in player.items:
                            confirm = input("You already have this item, are your sure you want to buy another? y/n").lower()
                            if confirm.startswith('n'):
                                input("Press Enter to go back to the Store.")
                                continue
                            else:
                                player.buy_item(self, weapon, weapon_to_buy)
                                input("Press Enter to go back to the Store.")
                                continue
                        else:
                            player.buy_item(self, weapon, weapon_to_buy)
                            input("Press Enter to go back to the Store.")
                            continue
                case 3:
                    armor_to_buy = ""
                    print(f"You have {player.money} coins, what armor do you want to buy?\n")
                    for key, item in self.store_armor.items():
                        print(f"[{key}] {item.name}: ${item.value}\n")
                    armor_to_buy = input("Type the number of the armor you want to buy:")
                    if int(armor_to_buy) not in self.store_armor.keys():
                        print("The store doesn't have this item")
                        input("Press Enter to go back to the Store.")
                        continue
                    else:
                        armor = self.store_armor[armor_to_buy]
                        if armor.value > player.money:
                            print("You don't have enough money to buy that many potions, please select a lower number.")
                            input("Press Enter to go back to the Store.")
                            continue
                        elif armor in player.items:
                            confirm = input("You already have this item, are your sure you want to buy another? y/n").lower()
                            if confirm.startswith('n'):
                                input("Press Enter to go back to the Store.")
                                continue
                            else:
                                player.buy_item(self, armor, armor_to_buy)
                                input("Press Enter to go back to the Store.")
                                continue
                        else:
                            player.buy_item(self, armor, armor_to_buy)
                            input("Press Enter to go back to the Store.")
                            continue                
                case 4: #leave the shop
                    break
                case _:
                    print("Please type only 1,2,3 or 4 on your keyboard to choose an option.")
                    continue

###############################################################################
# # LOCKED ROOM  (not finished)

# class LockedRoom(Room):
#     def __init__(self):
#         super().__init__(description="A Locked Room")
#         self.opened = False
#         self.locked = True

#     def intro_text(self):
#         if not self.opened and self.locked:
#             print("You stumble upon a locked door, you need a key to enter!")
#             return
#         else:
#              print("You already unlocked this room and found a longsword. It is now empty. You must press on.")
#              return
    
#     def unlocks(self):
#         if self.opened == False and self.locked==True:
#             self.opened = True
#             self.locked = False
#             print("The door unlocks and you find a closet with a longsword inside a display case! You pick up the longsword.")
    
#     def intro_text(self):
#         if not self.opened and self.locked:
#             print("You stumble upon a locked door, you need a key to enter!")
#             return
#         else:
#              print("You already unlocked this room and found a longsword. It is now empty. You must press on.")
#              return


# class LockedDoorWithKeypad():
#     def __init__(self, description ="A locked door", unlock_code=None):
#         self.desc = description
#         self.unlock_code = unlock_code
#         self.prompt = "Enter keypad code to unlock the door"
#         self.locked = True

#     def password_unlock(self):
#         while True:
#             code = input("Password: ****** (or type 'cancel'")
#             if (code == None) or (code.lower() == "cancel"):
#                 print("Cancelled request")
#                 return
#             try:
#                 intcode = int(code)
#             except:
#                 print("Keypad code not acccepted.")
#                 continue
#             if intcode != self.unlock_code:
#                 print("Keypad code not acccepted.")
#                 continue
#             break
#         print("Keypad code accepted!")
#         self.locked = False
 