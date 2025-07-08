import random
import time

elements = [
    {"name": "Hydrogen", "symbol": "H", "atomic": 1, "power": 2},
    {"name": "Helium", "symbol": "He", "atomic": 2, "power": 1, "effect": "shield"},
    {"name": "Carbon", "symbol": "C", "atomic": 6, "power": 5},
    {"name": "Oxygen", "symbol": "O", "atomic": 8, "power": 6},
    {"name": "Iron", "symbol": "Fe", "atomic": 26, "power": 10},
    {"name": "Uranium", "symbol": "U", "atomic": 92, "power": 15},
    {"name": "Gold", "symbol": "Au", "atomic": 79, "power": 12},
    {"name": "Nitrogen", "symbol": "N", "atomic": 7, "power": 4}
]

player_score = 0
ai_score = 0
rounds = 5

print("🔬 Welcome to ELEMENTAL DICE! Beat the AI with atomic power.\n")


def roll_element():
    return random.choice(elements)


for round_num in range(1, rounds + 1):
    print(f"\n🎲 Round {round_num}!")
    input("Press Enter to roll your element...")

    player_elem = roll_element()
    ai_elem = roll_element()

    print(f"\n🧪 You got: {player_elem['name']} ({player_elem['symbol']}) with power {player_elem['power']}")
    print(f"🤖 AI got: {ai_elem['name']} ({ai_elem['symbol']}) with power {ai_elem['power']}")

    player_power = player_elem["power"]
    ai_power = ai_elem["power"]

    if player_elem.get("effect") == "shield":
        print("🛡️ Your Helium gives you a shield! +1 power")
        player_power += 1
    if ai_elem.get("effect") == "shield":
        print("🤖 AI's Helium gives it a shield! +1 power")
        ai_power += 1

    if player_power > ai_power:
        print("✅ You win this round!")
        player_score += 1
    elif ai_power > player_power:
        print("❌ AI wins this round!")
        ai_score += 1
    else:
        print("⚖️ It's a tie!")

    time.sleep(1)

# Final result
print("\n🏁 GAME OVER")
print(f"🔢 Final Score: You {player_score} - AI {ai_score}")
if player_score > ai_score:
    print("🎉 YOU WIN THE GAME!")
elif ai_score > player_score:
    print("😓 AI WINS THIS TIME!")
else:
    print("🤝 It's a DRAW!")

print("\nThanks for playing Elemental Dice! Play again to learn more elements!")
