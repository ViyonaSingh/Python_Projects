import random
import os

width, height = 10, 6
player_x, player_y = 0, 0
num_planets = 6

facts = [
    "Jupiter is so big it could fit all the other planets inside it!",
    "Your DNA is 60% similar to a banana.",
    "Neutron stars are so dense, a teaspoon weighs 6 billion tons!",
    "Octopuses have three hearts and blue blood.",
    "Light from the Sun takes 8 minutes to reach Earth.",
    "The speed of light is 299,792 km per second!",
    "You can’t burp in space without exploding a bit.",
    "There’s a planet made of diamonds (55 Can-cri e)!"
]

# Generate random planets
planets = {(random.randint(0, width-1), random.randint(0, height-1)) for _ in range(num_planets)}


def display_map():
    os.system('cls' if os.name == 'nt' else 'clear')
    for y in range(height):
        row = ''
        for x in range(width):
            if (x, y) == (player_x, player_y):
                row += '🚀'
            elif (x, y) in planets:
                row += '* '
            else:
                row += '. '
        print(row)
    print("\nMove: w = up, s = down, a = left, d = right. q = quit")


def explore():
    global player_x, player_y
    while True:
        display_map()
        move = input(">> ").lower()

        if move == 'q':
            print("Thanks for exploring! See you among the stars. 🌌")
            break

        if move == 'w' and player_y > 0:
            player_y -= 1
        elif move == 's' and player_y < height - 1:
            player_y += 1
        elif move == 'a' and player_x > 0:
            player_x -= 1
        elif move == 'd' and player_x < width - 1:
            player_x += 1

        if (player_x, player_y) in planets:
            fact = random.choice(facts)
            print("\n🌍 You landed on a planet!")
            print(f"📚 Fun fact: {fact}")
            input("\nPress Enter to continue...")
            planets.remove((player_x, player_y))


explore()
