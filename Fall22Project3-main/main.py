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

# TODO
# Randomize map: auto-spawning monsters (randomize monsters stats), put npcs in random rooms. 
# store
# locked room and make it so regeneration isn't madatory

player = Player()

def gameplay_menu():
    choice = int(input("Do you want to play the game?\n[1]Play\n[2]Quit\n"))
    command_success = False
    match choice:
        case 1:
            clear()
            print("...loading...")
            time.sleep(1)
            print("...booting up game...")
            time.sleep(1)
            command_success = True
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

# def create_randomized_world():
#     num_of_rooms = 2
#     directions = ["east", "north", "west", "south"]
#     store = Store()
#     regen_room = Room("You are in the regeneration room")
#     dic_of_rooms = {1:regen_room,2:store}
#     random_amount_of_rooms = randint(5,7) # <-- can change randint range for more variation
#     # Creates 3 to 5 more rooms in the game
#     for room in len(3,random_amount_of_rooms):
#         room_number = randint(100, 999)
#         room_name = f"You are in room {room_number}"
#         num_of_rooms +=1
#         dic_of_rooms[room] = Room(room_name)
#     # Connects the rooms in a random pattern

#     for num in num_of_rooms:
#         random_directions = random.sample(directions, 2)
#         Room.connect_rooms(num, random_directions[0], random_directions[1])

def create_world():
    a = Room("You are in the blue room")
    b = Room("You are in the gray room")
    c = Room("You are in the gold room")
    d = Room("You are in the black room")
    e = Room("You are in the red room")
    store = Store()
    Room.connect_rooms(a, "east", b, "west")
    Room.connect_rooms(c, "east", d, "west")
    Room.connect_rooms(a, "north", c, "south")
    Room.connect_rooms(b, "north", d, "south")
    Room.connect_rooms(store, "north", b, "south")
    Room.connect_rooms(e, "north", store, "south")

    old_man = Npc("Old man", c)
    head = Npc("Talking head", c)

    rock = Rock()
    bplate = BrestPlate()
    rock.put_in_room(a)
    bplate.put_in_room(b)
    player.location = a
    monster = spawn_monster(a,1) #attack, defense, max_health, room, level
    monster_lvl2 = spawn_monster(a,2)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_situation():
    clear()
    print(player.location.desc)
    print()
    if player.location.has_monsters():
        print("This room contains the following monsters:")
        for m in player.location.monsters:
            print(m.name)
        print()
    if player.location.has_npcs():
        print("This room contains the following npcs:")
        for m in player.location.npcs:
            print(m.name)
        print()
    if player.location.has_items():
        print("This room contains the following items:")
        for i in player.location.items:
            print(i.name)
        print()
    print("You can go in the following directions:")
    for e in player.location.exit_names():
        print(e)
    print()

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
    print("quit -- quits the game")
    print()
    input("Press enter to continue...")


if __name__ == "__main__":
    #gameplay_menu()
    create_world()
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
                    if target != False and isinstance(target, Weapon):
                        player.equip_weapon(target)
                    elif target != False and isinstance(target, Armor):
                        player.equip_armor(target)
                    else:
                        print("No such item to equip")
                        command_success = False 
                case "unequip":
                    target_name = command[8:]
                    target = player.get_item_by_name(target_name)
                    if target != False:
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
                    player.use_potion()
                case "sleep":
                    player.sleep()
                case "talk_to":
                    target_name = command[8:]
                    target = player.location.get_npc_by_name(target_name)
                    if target != False:
                        if target.name == "Old man":
                            target.game_coin(player)
                        elif target.name == "Talking head":
                            target.choose_door(player)
                            target.die()
                        else: 
                            print("This npc doen't want to talk to you.")
                            command_success = False
                    else:
                        print("No such npc to talk to.")
                        command_success = False
                case other:
                    print("Not a valid command")
                    command_success = False
        if time_passes == True:
            updater.update_all()

