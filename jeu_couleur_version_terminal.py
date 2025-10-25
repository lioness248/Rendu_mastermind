import random

colors = ["vert", "camel", "rose", "jaune", "noir", "marron"]
combo_length = 4
max_turns = 10


def generate_secret(colors, combo_length):
    return random.choices(colors, k=combo_length)


def get_guess(combo_length, colors):
    while True:
        guess = input("Ta combinaison : ").strip().split()
        if len(guess) != combo_length:
            print(f"Il faut entrer exactement {combo_length} couleurs.")
            continue
        if any(color not in colors for color in guess):
            print(f"Il faut choisir uniquement entre {colors}")
            continue
        return guess


def check_guess(guess, secret):
    well_placed = 0
    badly_placed = 0
    result_symbols = ["_"] * len(secret)
    secret_copy = secret.copy()
    guess_copy = guess.copy()

    for i in range(len(secret)):
        if guess[i] == secret[i]:
            well_placed += 1
            result_symbols[i] = "*"
            secret_copy[i] = None
            guess_copy[i] = None

    for i in range(len(secret)):
        if guess_copy[i] is not None and guess_copy[i] in secret_copy:
            badly_placed += 1
            result_symbols[i] = "°"
            secret_copy[secret_copy.index(guess_copy[i])] = None

    return "".join(result_symbols), well_placed, badly_placed


def print_history(history):
    if not history:
        return
    print("Historique des essais :")
    for idx, (attempt, result, well_placed, badly_placed) in enumerate(history, 1):
        print(f"{idx}. {' '.join(attempt)} -> {result} "
              f"({well_placed} bien placée{'s' if well_placed>1 else ''}, "
              f"{badly_placed} mal placée{'s' if badly_placed>1 else ''})")


def play_game():
    secret_combo = generate_secret(colors, combo_length)
    print("La partie peut commencer !")
    print(f"Les couleurs possibles sont : {', '.join(colors)}")
    print(f"Propose une combinaison de {combo_length} couleur{'s' if combo_length > 1 else ''} (séparées par des espaces).")

    turn_count = 0
    history = []

    while turn_count < max_turns:
        turn_count += 1
        print(f"\nTour {turn_count}/{max_turns}")
        print_history(history)
        guess = get_guess(combo_length, colors)
        result, well_placed, badly_placed = check_guess(guess, secret_combo)

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


if __name__ == "__main__":
    play_game()
