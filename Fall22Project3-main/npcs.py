import updater
from random import randint
from player import *
from room import *

class Npc:
    def __init__(self, name, room):
            self.name = name
            self.room = room
            room.add_npc(self)
            updater.register(self)
    def __repr__(self):
        return self.name
    def update(self):
        return
    def die(self):
        self.room.remove_npc(self)
        updater.deregister(self)

    ###############################################################################
    # NPC MINI-GAMES
    def game_coin(self,player):
        try:
            interact = int(input("You have entered a room an see an old man in the corner. \n[1]Interact\n[2]Don't Incteract\n"))
            match interact:
                case 1:
                    clear()
                    print("Hello! Want to play a game to win coins, it requires one coin from you")
                    play = input("Play: [yes] or [no]\n")
                    clear()
                    if player.money <= 0:
                        print("Old man: Come back when you have some money")
                    elif play.lower() == 'yes':
                        player.money -=1
                        print("Old man: *flips a coin*")
                        print("Old man: Well...? Heads or tails?")
                        coin = randint(1, 2)
                        response = False
                        # while True:
                        while not response:
                            guess = input("[1]Heads or [2]Tails\n>")
                            clear()
                            if guess.isdigit():
                                number = int(guess)
                                if 2 >= number >= 1:
                                    response = True
                                    if number == coin:
                                        print("Old man: Damn... you beat me! Here is 3 coins including the one you gave me")
                                        player.money+=3
                                        print(f"Player recived 3 coins and now has a total of {player.money} coins")
                                    else:
                                        print("Old man: HAHAHA, thanks for the money kid!")
                                
                                else:
                                    print("Old man: That is a stupid guess...")
                            else:
                                print("Old man: I didn't catch that...")
                    else:
                        print("Old man: quit wasting my time chap")
                case 2:
                    print("You decide not to talk to the old man")
                case _: 
                    print("Seems that you couldn't make a decision")
        except ValueError:
                    # In case the player writes a value that is not a number
                    clear()
                    print("Old man: quit wasting my time chap")
        input("Press enter to continue...")

    def choose_door(self,player):
        door = ""
        print("In front of you, you see two doors. A talking head above the door states:")
        print("Through one door is something good, and through the other is something bad!")
        while door != "1" and door != "2":
            print("Which door will you go into? (1 or 2)", end=" ")
            door = input()
        clear()
        print(f"You approach the door...")
        time.sleep(1)
        print("The door ratttles open and you step in...")
        time.sleep(1)
        friendly_door = randint(1, 2)
        if int(door) == friendly_door:
            print("You have entered the friendly door, behind it is a bag of coins! You grab the coins and head back as you leave both doors diappear")
            player.money += 15
            print (f"You gained {player.money} coins!")
            input("Press enter to continue...")
        else:
            print("You walked into a room with no floor, you fall hundreds of feel and land on a pile of spikes")
            print("You have died")
            player.alive = False

    # def playagain(self) -> bool:
    #   return input("Would you like to play again (Yes/No)? ").lower().startswith("y")

    ###################################################################################
    # SHOPPING INTERACTIONS
    def shop(self,player):
        shopping = True
        while shopping:
            try:
                clear()
                decision = int(input('Get:\n[1]Potions\n[2]Weapons\n[3]Armor\n[4]Leave Shop\n'))
                match decision:
                    case 1: # Buying potions, the player can only carry up to 10 potions
                        potions_to_buy = int(input(f"You have {player.potions} potions and {player.money} coins, how many potions would you like to buy?\n"))
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
                        clear()
                        store_weapons = {1:Machete(), 2:PocketKnife()}
                        print(f"You have {player.money} coins, what weapon do you want to buy:")
                        for key, item in store_weapons.items():
                            print(f"[{key}] {item.name}, damage: {item.damage} --> Cost: {item.value} coins")
                        weapon_to_buy = input("Type the number of the weapon you want to buy: ")
                        if int(weapon_to_buy) not in store_weapons.keys():
                            print("The store doesn't have this item")
                            input("Press Enter to go back to the Store.")
                            continue
                        else:
                            weapon = store_weapons.get(int(weapon_to_buy))
                            if weapon.value > player.money:
                                print("You don't have enough money to buy that item")
                                input("Press Enter to go back to the Store.")
                                continue
                            # elif weapon in player.items:
                            #     confirm = input("You already have this item, are your sure you want to buy another? y/n").lower()
                            #     if confirm.startswith('n'):
                            #         input("Press Enter to go back to the Store.")
                            #         continue
                            #     else:
                            #         clear()
                            #         player.add_item(weapon)
                            #         player.money-= weapon.value
                            #         print(f"Thanks for your purchase! you now have {weapon.name}!\nCome back soon!")
                            #         store_weapons.pop(int(weapon_to_buy))
                            #         input("Press Enter to go back to the Store.")
                            #         continue
                            else:
                                clear()
                                player.add_item(weapon)
                                player.money = player.money - weapon.value
                                print(f"Thanks for your purchase! You now have {weapon.name}!\nCome back soon!")
                                store_weapons.pop(int(weapon_to_buy))
                                input("Press Enter to go back to the Store.")
                                continue
                    case 3:
                        clear()
                        store_armor = {1:Helmet(), 2:WristGuards()}
                        print(f"You have {player.money} coins, what armor do you want to buy:")
                        for key, item in store_armor.items():
                            print(f"[{key}] {item.name}: ${item.value}")
                        armor_to_buy = int(input("Type the number of the armor you want to buy: "))
                        if armor_to_buy not in store_armor.keys():
                            print("The store doesn't have this item")
                            input("Press Enter to go back to the Store.")
                            continue
                        else:
                            armor = store_armor.get(armor_to_buy)
                            if armor.value > player.money:
                                print("You don't have enough money to buy that item")
                                input("Press Enter to go back to the Store.")
                                continue
                            # elif armor in player.items:
                            #     confirm = input("You already have this item, are your sure you want to buy another? y/n").lower()
                            #     if confirm.startswith('n'):
                            #         input("Press Enter to go back to the Store.")
                            #         continue
                            #     else:
                            #         clear()
                            #         player.add_item(armor)
                            #         player.money-= armor.value
                            #         print(f"Thanks for your purchase! you now have {armor.name}!\nCome back soon!")
                            #         store_armor.pop(armor_to_buy)
                            #         input("Press Enter to go back to the Store.")
                            #         continue
                            else:
                                clear()
                                player.add_item(armor)
                                player.money = player.money - armor.value
                                print(f"Thanks for your purchase! you now have {armor.name}!\nCome back soon!")
                                store_armor.pop(armor_to_buy)
                                input("Press Enter to go back to the Store.")
                                continue
                    case 4: #leave the shop
                        break
                    case _:
                        print("Please type only 1,2,3 or 4 on your keyboard to choose an option.")
                        input("Press Enter to go back to the Store.")
                        continue
            except ValueError:
                        print("Not a valid command")
                        input("Press Enter to go back to the Store.")
                        continue
