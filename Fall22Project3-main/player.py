import os
from item import *
from monster import *
from random import randint, random
import time

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Player:
    def __init__(self):
        self.alive = True
        self.location = None
        self.items = []
        self.money = 0
        self.equipped = []

        self.health = 50
        self.attack = 1
        self.defense = 0
        self.exp = 0
        self.level = 1
        self.max_health = 60
        self.max_xp = 10
        self.max_level = 10
        self.potions = 1

    # is called on the 'me' case in main to show the player info
    def __repr__(self):
        print(f"These are your current stats:\nHealth: {self.health}\nLevel: {self.level}\nAttack: {self.attack}\nDefense: {self.defense}\nExp: {self.exp}\n")
        print(f"Equipped Items: {self.equipped} \nMoney: {self.money} \nPotions: {self.potions}")
        return input("Press enter to continue...")

    # goes in specified direction if possible, returns True if not possible returns False
    def go_direction(self, direction):
        new_location = self.location.get_destination(direction.lower())
        if new_location is not None:
            self.location = new_location
            return True
        return False

    ###############################################################################
    # CODE INVOLVING INVENTORY ITEMS
    def pickup(self, item):
        self.items.append(item)
        item.loc = self
        self.location.remove_item(item)
    def drop(self,item):
        if item in self.items:
            self.remove_item(item)
            item.put_in_room(self.location)
        return
    def drop_equipped(self,item):
        if item in self.equipped:
            self.equipped.remove(item)
            item.put_in_room(self.location)
            if isinstance(item, Weapon):
                self.attack -= item.damage
            elif isinstance(item, Armor):
                self.defense -= item.defense
        return 
    def add_item(self, item):
        self.items.append(item)
    def remove_item(self, item):
        self.items.remove(item)
    def get_item_by_name(self, name):
        for i in self.items:
            if i.name.lower() == name.lower():
                return i
        for j in self.equipped:
            if j.name.lower() == name.lower():
                return j
        return False
    def show_inventory(self):
        clear()
        print("You are currently carrying:")
        print()
        for i in self.items:
            print(i.name)
        print()
        input("Press enter to continue...")
    def equip_weapon(self,weapon):
        self.equipped.append(weapon)
        self.remove_item(weapon)
        self.attack += weapon.damage
        print(f"You have equipped {weapon}")
        return input("Press enter to continue...")
    def equip_armor(self,armor):
        self.equipped.append(armor)
        self.remove_item(armor)
        self.defense += armor.defense
        print(f"You have equipped {armor}")
        return input("Press enter to continue...")
    def unequip(self, item):
        self.equipped.remove(item)
        self.items.append(item)
        if isinstance(item, Weapon):
            self.attack -= item.damage
        else:
            self.defense -= item.defense
        print(f"You have unequipped {item.name}")
        return input("Press enter to continue...")

    ###############################################################################
    # ATTACKING & LEVELING
    def attack_enemy(self, monster):
        return (monster.lose_health(self.attack))
    def lose_health(self, damage):
        if damage <= 0:
            damage = 1
        print(f"You take {damage} damage!")
        if self.defense - damage >= 0:
            self.defense -= damage
        else:
            self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.alive = False
            print("You have been died! Goodbye!")
            input("Press Enter")
            return False
        else:
            print(f"You have {self.health}/{self.max_health} health remaining")
            return True

    def attack_options(self, monster):
        if self.level >= 30:
            print("\nYou are at max level so you won't level up anymore, but you can still get potions and money from the monsters you defeat.\n")
            input("Press Enter to continue.")
        keep_fighting = True
        while keep_fighting == True:
            clear()
            combat = True
            while combat == True:
                try:
                    # Let the player know how much hp they have and how many potions
                    print(f"HP:{self.health}/{self.max_health}")
                    print(f"Potions:{self.potions}")
                    decision = int(input('\nWhat do you want to do?\n[1] Attack\n[2] Use potion\n[3] Flee\n'))
                    match decision:
                        case 1:
                            clear()
                            combat = self.attack_enemy(monster) # player attacks first
                            if combat == True:
                                print(f"Carefull {monster.name} is attacking now!") # monster attacks player
                                combat = monster.attack_player(self)
                            else:
                                monster.die()
                                self.exp += monster.exp
                                if self.level >= self.max_level: self.exp = 0
                                self.money += randint(1,3) #Gives 1-3 coins for win
                                print (f"You gained {self.money} coins.")
                                # The player has 1/4 chances of getting some potions if not maxed on potions
                                if (random()*100 < 25 and self.potions < 10):
                                        random_potions = randint (1, 2)
                                        print("What's that? It seems like the monster was carrying some potions.\n You got {potions} more potion(s)".format(potions = random_potions))
                                        self.potions += random_potions
                                        if self.potions > 10: 
                                            self.potions = 10
                                            print("\nYou are carrying the maximum amount of potions.")
                                # calling leveling up
                                if self.exp >= self.max_xp:
                                    self.level_up()
                        case 2: # If the player choose to use a potion, call the use_potion method
                            clear()
                            self.use_potion()
                        case 3:
                            print(f"You have run away from {monster.name}")
                            break
                        case _: # In case the player writes anything else
                            clear()
                            print("Please type only 1 or 2 on your keyboard to choose an option.\n")
                            continue
                except ValueError:
                    # In case the player writes a value that is not a number
                    clear()
                    print("Sorry I didn't get that please try again.\n")
            if self.health == 0: break # if the player dies in combat
            keep_fighting = False
            input("Press enter to continue...")
    
    def level_up(self):
        while self.exp >= self.max_xp:
            self.level += 1
            if self.level >= self.max_level:
                print("You have reached the maximum level you can get")
                self.level = self.max_level
                self.exp = 0
                return 0
            self.health += 5
            self.max_health += 5
            self.exp -= self.max_xp
            self.attack += 0.5
            print (f"You leveled up! you are now level {self.level}")

    ###############################################################################
    # HEALING + SLEEPING
    def heal(self):
        self.health += round(self.max_health * 0.2)
        if self.health > self.max_health:
            self.health = self.max_health
        print(f'You used a potion and have now {self.health}/{self.max_health} HP')
    def use_potion(self):
        if self.potions > 0:
            while True:
                if self.health == self.max_health:
                    print(f'You already have your max health')
                    return input("Press enter to continue...")
                else:
                    self.heal()
                    self.potions -= 1
                    print(f'You now have {self.potions} potions left')
                    return input("Press enter to continue...")
        else: print('You don\'t have any potions left'); return input("Press enter to continue...")

    def sleep(self):
        ask = input("Are you sure you want to sleep? [yes][no] \n").lower()
        if ask == 'no':
            return
        elif ask =='yes':
            sleep_time = randint(2,6)
            for i in range(0,sleep_time):
                print("...player is sleeping...")
                time.sleep(1)
                if self.health < self.max_health: #can't have more than max health
                    self.health += 1
            if randint(0, 10) > 5: # random chance of being attacked by a monster in sleep
                self.monster_during_rest()
            else:
                print(f"After a peaceful rest players HP is now {self.health}/{self.max_health}")
                input("Press enter to continue...")
    def monster_during_rest(self):
        location = self.location
        monster = spawn_monster(location,1) #spawns a weak monster
        print(f"You abrubtly wake from your slumber to the sound of a {monster.name} rushing toward you!")
        monster.attack_player(self)
        input("Press enter to continue...")
        self.attack_options(monster)

    def regenerate_heal(self):
        while self.health<self.max_health:
            clear()
            self.health+=1
            print(f"HP:{self.health}/{self.max_health}")
            time.sleep(1)


    ###############################################################################
    # Buying Items
    def buy_item(self, store, item, index):
        self.add_item(item)
        self.money-= item.value
        print(f"Thanks for your purchase! you now have {item}!\nCome back soon!")
        if isinstance(item, Weapon):
            store.store_weapons.pop(index)
        elif isinstance(item, Armor):
            store.store_armor.pop(index)

    ###############################################################################
    # Using Key
    # def use_key(self, room):
    #     best_key = None
    #     if room.locked:
    #         for item in self.items:
    #             if isinstance(item, items.Key):
    #                 if room.key == room.unique:
    #                     best_key = item.unique
    #                     room.locked = False
    #                     print("\n\tYou use {}!".format(item.name))
    #                     break
    #                 best_key = item.unique
    #         if best_key == None:
    #             print("\n\tYou don't have any keys!\n")

