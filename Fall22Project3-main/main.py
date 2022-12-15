from room import *
from player import *
from item import *
from monster import *
import os
import updater
import random
import time
from names import *
from npcs import *
import pickle
from colorama import Fore, Style

# TODO
# Events
# make sure map is layed out okay, and that everything is initialized well
# text-doc explaining game

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# Global variables
store = Store()
shop = Npc("Store clerk", store)
lockedroom = LockedRoom()
lockedcoderoom = LockedDoorWithKeypad()
regenroom = Regeneration()
key = Key()
rock = Rock()
bplate = BrestPlate()
scroll = Item("Scroll", "A small scroll displaying the numbers 123456. I wonder if this is useful")
player = Player("Bob")
startroom = IntroRoom()
lockbox = LockBox()

##############################################################################################
# Game play menu and save/load game options
def main():
    clear()
    print("New Game")
    print("Load Game")
    print("Exit")
    option = input("What do you want to do: ").lower()
    if option == "new game":
        start()
    elif option == "load game":
        loadgame()
    else:
        clear()
        gameplay_menu()

def loadgame():
    #option = input("What do you want to do: ").lower()
    try:
        with open("save_state_1", "rb") as save:
            SaveVars = pickle.load(save)
            load(SaveVars)
    except:
        input("There is no saved game in the directory")
        main()

def start():
    clear()
    print("Hello welcome to an adventure game")
    name = str(input("What is your name? \n"))
    global player
    player = Player(name)
    clear()
    print("...loading...")
    time.sleep(1)
    print("...booting up game...")
    time.sleep(1)
    clear()

def load(save):
    global player
    global world
    player = save[0]
    world = save[1]
    input(f"Welcome back {player.name}, we missed you! Press enter to continue")

# One save slate: only saves the player, the and how the world was layed out (good if I expanded the world to make rooms locations random).
# Doesn't save specific items being present/not present in a room or the location of monster upon save.
def savegame():
    while True:
        ask = input("Do you want to save?\n--> ").upper()
        if ask == "Y" or ask == "YES":
            SaveVars = [player, world]
            with open("save_state_1", "wb") as save:
                pickle.dump(SaveVars, save)
                input(f"You saved your current status and world, press enter to continue")
        elif ask == "N" or ask == "NO":
            return
        else:
            print("Sorry, that does not compute with me! Please try again!")
            continue
        break

def gameplay_menu():
    play = False
    while play == False:
        try:
            choice = int(input("Do you want to play the game?\n[1]Play\n[2]Quit\n"))
            command_success = False
            match choice:
                case 1:
                    main()
                    command_success = True
                    break
                case 2:
                    command_success = False
                    while not command_success:
                        confirm = input("Are you sure you want to quit? y/n\n>")
                        if confirm.lower() == 'y':
                            quit()
                        elif confirm.lower() == 'n':
                            command_success = True
                            clear()
                            return gameplay_menu()
                        else:
                            clear()
                            print("Invalid reply...")
                            return gameplay_menu()
                case _:
                    command_success = False
                    clear()
                    print("Not a valid command")
                    return gameplay_menu()
        except ValueError:
                        # In case the player writes a value that is not a number
                        clear()
                        print("Not a valid command")
                        command_success = False

##############################################################################################
# Create a specific world layout
def create_world():
    a = Room("You are in the blue room")
    b = Room("You are in the gray room")
    c = Room("You are in the gold room")
    d = Room("You are in the black room")
    Room.connect_rooms(a, "east", b, "west")
    Room.connect_rooms(c, "east", d, "west")
    Room.connect_rooms(a, "south", lockedroom, "north")
    Room.connect_rooms(a, "north", c, "south")
    Room.connect_rooms(b, "north", d, "south")
    Room.connect_rooms(store, "north", b, "south")
    Room.connect_rooms(lockedcoderoom, "north", store, "south")
    Room.connect_rooms(lockedcoderoom, "east", startroom, "west")
    Room.connect_rooms(startroom, "south", c, "north")
    rooms_list = [a,b,c,d]
    old_man = Npc("Old man", rooms_list[random.randint(0,3)])
    head = Npc("Talking head", rooms_list[random.randint(0,3)])
    key.put_in_room(rooms_list[random.randint(0,3)])
    rock.put_in_room(startroom)
    bplate.put_in_room(rooms_list[random.randint(0,3)])
    player.location = startroom
    scroll.put_in_room(rooms_list[random.randint(0,3)])
    monster = spawn_monster(rooms_list[random.randint(0,3)],1) #attack, defense, max_health, room, level
    monster_lvl2 = spawn_monster(rooms_list[random.randint(0,3)],2)

def print_situation():
    clear()
    print(Fore.GREEN + player.location.desc + Style.RESET_ALL)
    if player.location.has_monsters():
        print("This room contains the following monsters:")
        for m in player.location.monsters:
            print(Fore.RED + m.name + Style.RESET_ALL)
    # continueously spawns monsters
    if player.location.has_monsters() == False:
        random_spawn_monster(player.location)
    if player.location.has_npcs():
        print("This room contains the following npcs:")
        for m in player.location.npcs:
            print(Fore.YELLOW + m.name + Style.RESET_ALL)
    if player.location.has_items():
        print("This room contains the following items:")
        for i in player.location.items:
            print(Fore.BLUE + i.name + Style.RESET_ALL)
    print("You can go in the following directions:")
    for e in player.location.exit_names():
        print(Fore.MAGENTA + e + Style.RESET_ALL)
    if player.location == regenroom:
        print(Fore.GREEN + "Type 'heal' to start regenerating" + Style.RESET_ALL)

def show_help():
    clear()
    print("go <direction> -- moves you in the given direction")
    print("wait -- waits a turn/waits for a monster to leave")
    print("attack <monster> -- starts fight options")
    print("inventory -- opens your inventory")
    print("me -- look at your players stats, money and equipped items")
    print("pickup <item> -- picks up the item")
    print("drop <item> -- drops the item")
    print("inspect <item> -- look at the items desciption in inventory or in the players location")
    print("equip <item> -- equip a weapon for more attack power and/or equip defensive items")
    print("unequip <item> -- unequip a weapon or defensive item")
    print("heal -- consumes potion to heal 20 precent of health")
    print("sleep -- regain a little bit of health by sleeping for a random amount of time (beware enemies can attack you in your sleep!)")
    print("talk_to <npc> -- interact with an npc")
    print("unlock -- unlocks room if player has a key, or if there is a keypad on the door. (Note: use key word 'open <item>' on the lock box instead)")
    print("quit -- quits the game")
    print()
    input("Press enter to continue...")


if __name__ == "__main__":
    gameplay_menu()
    global world
    world = create_world()
    #world = create_randomized_world()
    playing = True
    while playing and player.alive:
        print_situation()
        command_success = False
        time_passes = False
        while not command_success:
            command_success = True
            command = input("What now? ")
            if len(command) == 0:
                continue
            command_words = command.split()
            if len(command_words) == 0:
                continue
            match command_words[0].lower():
                case "go":   #cannot handle multi-word directions
                    if len(command)>3:
                        okay = player.go_direction(command_words[1]) 
                        if okay is True:
                            time_passes = True
                        else:
                            print("You can't go that way.")
                            command_success = False
                    else:
                        print("You can't go that way.")
                        command_success = False
                case "wait":   
                        time_passes = True 
                case "pickup":  #can handle multi-word objects
                    target_name = command[7:] # everything after "pickup "
                    target = player.location.get_item_by_name(target_name)
                    if target != False:
                        player.pickup(target)
                    else:
                        print("No such item.")
                        command_success = False  
                case "drop":
                    target_name = command[5:] # everything after "drop "
                    target = player.get_item_by_name(target_name)
                    if target != False:
                        player.drop(target)
                        player.drop_equipped(target)
                    else:
                        print("No such item.")
                        command_success = False 
                case "inventory":
                    player.show_inventory()
                case "help":
                    show_help()
                case "exit":
                    playing = False
                case "attack":
                    target_name = command[7:]
                    target = player.location.get_monster_by_name(target_name)
                    if target != False:
                        player.attack_options(target)
                    else:
                        print("No such monster.")
                        command_success = False
                case "equip":
                    target_name = command[6:]
                    target = player.get_item_by_name(target_name)
                    check = player.check_weapon_equipped()
                    if target != False and isinstance(target, Weapon) and check is False:
                        player.equip_weapon(target)
                    elif target != False and isinstance(target, Weapon) and check is True:
                        print("You already have a weapon equipped")
                        command_success = False
                    elif target != False and isinstance(target, Armor):
                        player.equip_armor(target)
                    else:
                        print("No such item to equip")
                        command_success = False 
                case "unequip":
                    target_name = command[8:]
                    target = player.get_item_by_name_equipped(target_name)
                    if target != False:
                        print(target)
                        player.unequip(target)
                    else:
                        print("No such item to equip")
                        command_success = False        
                case "me":
                    print(player)
                case "inspect":
                    target_name = command[8:]
                    target_on_player = player.get_item_by_name(target_name)
                    target_in_location = player.location.get_item_by_name(target_name)
                    if target_on_player != False:
                        target_on_player.describe()
                    elif target_in_location != False:
                        target_in_location.describe()
                    else:
                        print("No such item to inspect")
                        command_success = False  
                case "heal":
                    if player.location == regenroom and regenroom.healing==True:
                        regenroom.player_regenerate(player)
                    else:
                        player.use_potion()
                case "sleep":
                    player.sleep()
                case "talkto":
                    target_name = command[7:]
                    target = player.location.get_npc_by_name(target_name)
                    if target != False:
                        if target.name == "Old man":
                            target.game_coin(player)
                        elif target.name == "Talking head":
                            target.choose_door(player)
                            target.die()
                        elif target.name == "Store clerk":
                            target.shop(player)
                        else: 
                            print("This npc doen't want to talk to you.")
                            command_success = False
                    else:
                        print("No such npc to talk to.")
                        command_success = False
                case "unlock":
                    if player.location == lockedroom:
                        key = player.get_item_by_name("key")
                        if key != False and isinstance(key, Key):
                            lockedroom.unlock_room()
                            player.remove_item(key)
                            Room.connect_rooms(lockedroom, "east", regenroom, "west")
                            player.location = regenroom
                        elif key == False and lockedroom.locked == True:
                            print("You don't have any keys")
                            command_success = False  
                        else:
                            print("\nYou already unlocked the door in this room. Press on.")
                            command_success = False 
                    elif player.location == lockedcoderoom:
                        lockedcoderoom.password_unlock()
                        if lockedcoderoom.opened == True and lockedcoderoom.locked == False and lockedcoderoom.box == True:
                            lockbox.put_in_room(lockedcoderoom)
                    else:
                        print("You are not in a room where there is something to unlock")
                        command_success = False
                case "open":
                    target_name = command[5:]
                    if target_name.lower() == lockbox.name and lockbox.loc == player.location or lockbox.loc == player:
                        if lockbox.locked == True:
                            lockbox.unlock()
                        else:
                            lockbox.menu_choice(player)
                    else:
                        print("Not a valid command")
                        command_success = False
                case "save":
                    savegame()
                case other:
                    print("Not a valid command")
                    command_success = False
        if time_passes == True:
            updater.update_all()

##############################################################################################
# def create_randomized_world():
#     num_of_rooms = 5
#     directions = ["east","west","north","south"]
#     dic_of_rooms = {1:regenroom,2:store,3:lockedroom,4:lockedcoderoom,5:startroom}
#     random_spawn_monster(startroom)
#     random_amount_of_rooms = randint(8,10) # <-- can change randint range for more variation
#     # Creates 3 to 5 more rooms in the game (other than the shop, regenroom, locked rooms, and intro room)
#     for room in len(6,random_amount_of_rooms):
#         room_number = randint(100, 999)
#         room_name = f"You are in room {room_number}"
#         num_of_rooms +=1
#         dic_of_rooms[room] = Room(room_name)
#         # randomly spawns up to two monsters of a random level in a room
#         random_spawn_monster(room_name)
#         random_spawn_monster(room_name)

#     #connects the rooms randomly
#     num = 1
#     while num != num_of_rooms:
#         random_directions = random.sample(directions, 2
#         works = Room.connect_rooms(dic_of_rooms.get(num), random_directions[0], dic_of_rooms.get(num+1), random_directions[1])
#         if works == True:
#             num +=1

#     # Room.connect_rooms(a, "east", b, "west")
#     # Puts items, npc, and player in random rooms
#     random_room = dic_of_rooms.get(randint(6,random_amount_of_rooms)) # put item/npcs in non-specialized rooms
#     old_man = Npc("Old man", random_room)
#     head = Npc("Talking head", random_room)
#     rock.put_in_room(startroom)
#     bplate.put_in_room(random_room)
#     key.put_in_room(random_room)
#     scroll.put_in_room(random_room)
#     player.location = startroom