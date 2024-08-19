import random

class Player:
    def __init__(self, name=""):
        self.name = name  # Player's name
        self.health = 100  # Player's initial health
        self.backpack = []  # Items the player is carrying
        self.location = (1, 1)  # Starting location

    def move(self, direction, max_x, max_y):
        x, y = self.location  # Get current location coordinates
        # Move the player based on direction, ensuring they don't go out of bounds
        if direction == "forward" and y < max_y:
            self.location = (x, y + 1)
        elif direction == "backward" and y > 1:
            self.location = (x, y - 1)
        elif direction == "left" and x > 1:
            self.location = (x - 1, y)
        elif direction == "right" and x < max_x:
            self.location = (x + 1, y)
        else:
            print("You can't move in that direction.")  # Notify player of invalid move
            return False
        return True

    def add_to_backpack(self, item):
        # Check if backpack can fit more items
        if len(self.backpack) >= 4:
            print("Backpack is full! Can't carry more items.")  # Notify player of full backpack
            return
        self.backpack.append(item)  # Add item to backpack

class Location:
    def __init__(self, x, y, description, items=None):
        self.coordinates = (x, y)  # Location coordinates
        self.description = description  # Description of the location
        self.items = items or []  # List of items in the location

    def __str__(self):
        return f"Location {self.coordinates}: {self.description}"  # String representation of location

class Scp:
    def __init__(self, name="", caution="", power=0, location=()):
        self.name = name # Name of SCP
        self.caution = caution # Caution details about SCP
        self.power = power # SCP's power level, reducing health by this amount
        self.location = location
    
    def move(self, max_x, max_y):
        # Generate new random coordinates within the bounds
        new_x = random.randint(1, max_x)
        new_y = random.randint(1, max_y)
        self.location = (new_x, new_y)  # Update SCP's location to the new random location
        return f"SCP has moved to {self.location}" 


def gameplay():
    name = input("Enter a character name: ")  # Get player's name
    player = Player(name)  # Create a new player object

    # Define locations with coordinates, descriptions, and items
    locations = {
        (1, 1): Location(1, 1, "Start", items=["Map Fragment"]),
        (1, 2): Location(1, 2, "Lab", items=["Energy Bar", "Toolbox"]),
        (1, 3): Location(1, 3, "SCP - 055's Room", items=["Weapon (Stun Gun)"]),
        (1, 4): Location(1, 4, "SCP Containment", items=["Security Keycard"]),
        (2, 1): Location(2, 1, "Control Room", items=["EMP Device"]),
        (2, 2): Location(2, 2, "Armory", items=["Weapon (Stun Gun)"]),
        (2, 3): Location(2, 3, "Infirmary", items=["Medkit"]),
        (3, 1): Location(3, 1, "Observation Deck"),
        (3, 2): Location(3, 2, "Power Core", items=["Toolbox"]),
        (3, 3): Location(3, 3, "Engineering"),
        (4, 1): Location(4, 1, "Mess Hall", items=["Water Bottle", "Canned Food"]),
        (4, 2): Location(4, 2, "Storage", items=["First-Aid Kit"]),
        (5, 1): Location(5, 1, "Escape Pods"),
        (5, 2): Location(5, 2, "Emergency Exit"),
    }

    # SCP initial random coordinates
    random_x = random.randint(1, 5)  # Choose a random x-coordinate within bounds
    random_y = random.randint(1, 4)  # Choose a random y-coordinate within bounds

    # Create SCP-1 with random coordinates
    scp1 = Scp(name="SCP-1", caution="Don't touch him", power=3, location=(random_x, random_y)) 

    max_x = max(location[0] for location in locations)  # Determine maximum x coordinate
    max_y = max(location[1] for location in locations)  # Determine maximum y coordinate

    print(f"Welcome to SCP HQ, {player.name}! Survive and find a way to escape.")
    print(" ")
    print(f"You are currently at {player.location}. {locations[player.location].description}. You found {locations[player.location].items}")

    scp_initial_location_desc = locations.get(scp1.location, Location(*scp1.location, "Dark")).description
    print(" ")
    print(f"SCP is initially in {scp_initial_location_desc}")

    while True:
        print(" ")
        action = input("Choose an action (1.move, 2.pick up item): ").lower() # Get player's action

        # SCP moves before each action
        scp_move_message = scp1.move(max_x, max_y)
        scp_location_desc = locations.get(scp1.location, Location(*scp1.location, "Unknown location")).description
        print(" ")
        print(scp_move_message)  # SCP move message
        print(" ")
        print(f"SCP is now in {scp_location_desc}")
        # Sorry if you're another developer—yeah, you might need to repair or update this because, well, I made it. 
        # But if you're a teacher, double sorry for the headache you're about to endure.
        # Some things might seem a bit... puzzling? Just head over to explanation.txt for more of my brilliant logic (or lack thereof).
        if action in ["1", "move"]:
            print(" ")
            direction = input("Choose where to move (forward, backward, left, right): ").lower()  # Get direction to move
            if player.move(direction, max_x, max_y):  # Move player and update location
                current_location = locations[player.location]
                scp_move_message = scp1.move(max_x, max_y)
                scp_location_desc = locations.get(scp1.location, Location(*scp1.location, "Unknown location")).description
                print(" ")
                print(scp_move_message)  # SCP move message
                print(" ")
                print(f"SCP is now in {scp_location_desc}")
                print(" ")
                print(f"You moved {direction}. New location: {current_location.coordinates}. {current_location.description}. You found {current_location.items}")
            elif player.location == (4, 2) or player.location == (4, 1):
                if player.backpack == ["Security Keycard"] and direction == "forward":
                    player.location = (5, 2)
            else:
                continue

        elif action in ["2", "pick up item"]:
            current_location = locations[player.location]  # Get current location
            if current_location.items:
                if len(current_location.items) == 1:
                    item = current_location.items[0]  # Pick the only item available
                    player.add_to_backpack(item)
                    print(" ")
                    print(f"Item added to your backpack: {item}")
                    current_location.items = []  # Clear items from the location after picking them up
                else:
                    print(" ")
                    print("Items in this location:")
                    for i, item in enumerate(current_location.items, 1):
                        print(" ")
                        print(f"{i}. {item}")
                    try:
                        choice = int(input("Which one to pick? "))  # Get user's choice
                        if 1 <= choice <= len(current_location.items):
                            item = current_location.items.pop(choice - 1)  # Remove item from the list
                            player.add_to_backpack(item)
                            print(" ")
                            print(f"Item added to your backpack: {item}")
                        else:
                            print(" ")
                            print("Invalid choice.")  # Handle invalid choice
                            continue
                    except ValueError:
                        print(" ")
                        print("Please enter a valid number.")  # Handle non-integer input
                        continue
                print(" ")
                print(f"Current backpack: {player.backpack}")
            else:
                print(" ")
                print("No items to pick up here.")  # No items in the location
        else:
            print(" ")
            print("Invalid action. Please choose 'move' or 'pick up item'.")  # Handle invalid action
        
        if player.location == scp1.location:
            print("Game Over!")
            break

        if player.location == (5, 2) or player.location == (5, 1):
            print(" ")
            print("Congratulations, you have found the Emergency Exit and won the game!")  # Player won the game
            break
gameplay()