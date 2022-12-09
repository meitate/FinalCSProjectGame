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
