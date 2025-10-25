import random

colors = ["vert", "camel", "rose", "jaune", "noir", "marron"]
combo_length = 4

secret_combo = random.choices(colors, k=combo_length)

print("La partie peut commencer !")
print(f"Les couleurs possibles sont : {', '.join(colors)}")
print(f"Propose une combinaison de {combo_length} couleur{'s' if combo_length > 1 else ''} (séparées par des espaces).")

turn_count = 0
max_turns = 10
history = []

while turn_count < max_turns:
    turn_count += 1
    print(f"\nTour {turn_count}/{max_turns}")
    print("Historique des essais :")
    for idx, (attempt, result, well_placed, badly_placed) in enumerate(history, 1):
        print(f"{idx}. {' '.join(attempt)} -> {result} ({well_placed} bien placée{'s' if well_placed>1 else ''}, {badly_placed} mal placée{'s' if badly_placed>1 else ''})")

    guess = input("Ta combinaison : ").strip().split()
    if len(guess) != combo_length:
        print(f"Il faut entrer exactement {combo_length} couleurs.")
        turn_count -= 1
        continue

    for color in guess:
        if color not in colors:
            print(f"Il faut choisir uniquement entre {colors}")
            turn_count -= 1
            break
    else:
        well_placed = 0
        badly_placed = 0
        result_symbols = ["_"] * combo_length
        secret_copy = secret_combo.copy()
        guess_copy = guess.copy()

        for i in range(combo_length):
            if guess[i] == secret_combo[i]:
                well_placed += 1
                result_symbols[i] = "*"
                secret_copy[i] = None
                guess_copy[i] = None

        for i in range(combo_length):
            if guess_copy[i] is not None and guess_copy[i] in secret_copy:
                badly_placed += 1
                result_symbols[i] = "°"
                secret_copy[secret_copy.index(guess_copy[i])] = None

        result = "".join(result_symbols)
        history.append((guess, result, well_placed, badly_placed))
        print(f"Résultat : {result}")
        print(f"({well_placed} bien placée{'s' if well_placed > 1 else ''}, {badly_placed} mal placée{'s' if badly_placed > 1 else ''})")

        if well_placed == combo_length:
            print("YOUPIIIII t'as réussi !!!")
            break
        elif badly_placed > 0 and well_placed < combo_length:
            print("Il y a des couleurs bien choisies mais mal placées !")

if well_placed != combo_length:
    print("\nTu as utilisé toutes tes tentatives.")
    print(f"La combinaison secrète était : {' '.join(secret_combo)}")
