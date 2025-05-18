#Zork Game

import random
rooms = ["Light Blue", "White", "Orange", "Red", "Green"]
room_doors = {
    "Light Blue": {"east": "White", "south": "Orange"},
    "White": {"west": "Light Blue"},
    "Orange": {"north": "Light Blue", "south": "Red"},
    "Red": {"north": "Orange", "east": "Green"},
    "Green": {"west": "Red", "south": "Exit"} 
}

box_and_dragon_rooms = random.sample(rooms, 3)
gold_box_room = box_and_dragon_rooms[0]
silver_box_room = box_and_dragon_rooms[1]
dragon_room = box_and_dragon_rooms[2]
key_in = random.choice(["gold", "silver"])

current_room = "Light Blue"
have_key = False
exit_locked = True
dragon_helped = False
game_over = False

print("Welcome to the Adventure Game!")
print("Rooms: Light Blue, White, Orange, Red, Green.")

while True:
    print("You are in the", current_room, "room.")
    if current_room in room_doors:
        for direction in room_doors[current_room]:
            print("There is a door", direction, "to", room_doors[current_room][direction])
    if current_room == gold_box_room:
        print("There is a Gold box here.")
    if current_room == silver_box_room:
        print("There is a Silver box here.")
    if current_room == dragon_room and not dragon_helped:
        print("There is a dragon here.")
    if current_room == "Green":
        print("There is an EXIT to the South. It is", "locked." if exit_locked else "unlocked!")

    player = input("What do you want to do? ").strip().lower()

    if player.startswith("go "):
        direction = player[3:]
        if current_room in room_doors and direction in room_doors[current_room]:
            next_room = room_doors[current_room][direction]
            if next_room == "Exit":
                if exit_locked:
                    print("The EXIT is locked.")
                else:
                    print("You escaped! Bravo!")
                    break
            else:
                current_room = next_room
        else:
            print("You cannot go that way.")

    elif player == "unlock exit":
        if current_room == "Green":
            if have_key:
                exit_locked = False
                print("You unlocked the EXIT!")
            else:
                print("You don't have the key.")
        else:
            print("There is no exit here.")

    elif player == "open box":
        if current_room == gold_box_room:
            if key_in == "gold":
                have_key = True
                print("You got the key from the Gold box!")
            else:
                print("Wrong box! The Silver box locks forever. Game over.")
                game_over = True
        elif current_room == silver_box_room:
            if key_in == "silver":
                have_key = True
                print("You got the key from the Silver box!")
            else:
                print("Wrong box! The Gold box locks forever. Game over.")
                game_over = True
        else:
            print("There is no box here.")
        if game_over:
            break

    elif player == "where is the key" and current_room == dragon_room and not dragon_helped:
        print("Dragon: Answer my riddle and I will tell you where the key is.")
        answer = input("Dragon asks: What has to be broken before you can use it? ").strip().lower()
        if "egg" in answer:
            print(f"Dragon: Correct! The key is in the {key_in.capitalize()} box.")
            dragon_helped = True
        else:
            print("Dragon: Wrong! I won't help you anymore.")
            dragon_helped = True

    elif player == "exit":
        if current_room == "Green" and not exit_locked:
            print("You escape! Congratulations!")
            break
        else:
            print("You can't exit here.")
    else:
        print("I don't understand that command.")
