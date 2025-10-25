import pygame  # type: ignore
import random
import sys

colors = ["vert", "camel", "rose", "jaune", "noir", "marron"]
color_rgb = {
    "vert": (144, 238, 144),
    "camel": (193, 154, 107),
    "rose": (255, 182, 193),
    "jaune": (255, 255, 153),
    "noir": (40, 40, 40),
    "marron": (139, 69, 19)
}
combo_length = 4
max_turns = 10
screen_width = 700
screen_height = 950

pygame.init()
pygame.display.set_caption("THE GREAT CHOICE")
screen = pygame.display.set_mode((screen_width, screen_height))
font = pygame.font.SysFont("arialrounded", 32)
big_font = pygame.font.SysFont("arialrounded", 56)
small_font = pygame.font.SysFont("arialrounded", 22)

WHITE = (255, 255, 255)
PINK = (255, 210, 220)
PEACH = (255, 230, 200)
BROWN = (90, 60, 50)
GREY = (180, 180, 180)
GREEN = (120, 200, 120)
ORANGE = (255, 190, 100)
PANEL = (248, 244, 241)

background = pygame.image.load("panda_wallpaper.png")
background = pygame.transform.scale(background, (screen_width, screen_height))


def draw_button(text, rect, color_bg, color_text):
    pygame.draw.rect(screen, color_bg, rect, border_radius=20)
    label = font.render(text, True, color_text)
    screen.blit(label, (rect.x + (rect.width - label.get_width()) // 2,
                        rect.y + (rect.height - label.get_height()) // 2))


def wrap_lines(text, font_obj, max_width):
    words = text.split(" ")
    lines = []
    cur = ""
    for w in words:
        test = (cur + " " + w).strip()
        if font_obj.size(test)[0] <= max_width:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def show_end_screen(message, submessage="", color=GREEN):
    while True:
        screen.blit(background, (0, 0))
        lines = wrap_lines(message, big_font, screen_width - 80)
        y = screen_height // 2 - (len(lines) * big_font.get_height()) // 2 - 60
        for ln in lines:
            label = big_font.render(ln, True, color)
            screen.blit(label, (screen_width // 2 - label.get_width() // 2, y))
            y += big_font.get_height() + 4
        if submessage:
            sub_lines = wrap_lines(submessage, font, screen_width - 80)
            y += 10
            for ln in sub_lines:
                lab = font.render(ln, True, BROWN)
                screen.blit(lab, (screen_width // 2 - lab.get_width() // 2, y))
                y += font.get_height() + 2
        replay_btn = pygame.Rect(screen_width // 2 - 230, y + 60, 200, 70)
        quit_btn = pygame.Rect(screen_width // 2 + 30, y + 60, 200, 70)
        draw_button("REJOUER", replay_btn, PINK, BROWN)
        draw_button("QUITTER", quit_btn, (255, 170, 170), BROWN)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if replay_btn.collidepoint(event.pos):
                    return "replay"
                if quit_btn.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()


def show_menu():
    while True:
        screen.blit(background, (0, 0))
        title = font.render("T'ES BEAU TOI AUJOURD'HUI !", True, PINK)
        screen.blit(title, (screen_width // 2 - title.get_width() // 2, 300))
        play_btn = pygame.Rect(screen_width // 2 - 100, 600, 200, 80)
        draw_button("JOUER", play_btn, PINK, BROWN)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_btn.collidepoint(event.pos):
                    return


def play_game():
    secret_combo = random.choices(colors, k=combo_length)
    attempts = []
    feedback = []
    current_guess = [None] * combo_length
    selected_index = None
    turn_count = 0
    tip_message = ""
    game_over = False
    victory = False

    # fond kawaii
    background = pygame.image.load("panda_wallpaper.png")
    background = pygame.transform.scale(background, (screen_width, screen_height))

    # couleurs
    color_buttons = []
    palette_y = screen_height - 140
    spacing = screen_width // (len(colors) + 1)
    for i, c in enumerate(colors):
        rect = pygame.Rect(spacing * (i + 1) - 35, palette_y, 70, 70)
        color_buttons.append((rect, c))

    # emplacements pour les bulles 
    def current_slot_center(i):
        start_x = (screen_width - (combo_length * 90 - 20)) // 2
        y = screen_height // 2 + 100
        return (start_x + i * 90, y)

    while not game_over:
        screen.blit(background, (0, 0))

        # titre 
        title = font.render(f"TENTATIVE {turn_count + 1}/{max_turns}", True, (255, 210, 220))
        screen.blit(title, (screen_width // 2 - title.get_width() // 2, 40))

        # affichage des tentatives précédentes
        y_offset = screen_height // 2 - 250
        for i, attempt in enumerate(attempts[-5:]):  # max 5 dernières
            row_x = (screen_width - (combo_length * 90 - 20)) // 2
            for j, c in enumerate(attempt):
                # dessin de la bulle
                pygame.draw.circle(screen, color_rgb[c], (row_x + j * 90, y_offset), 25)

                # affichage du texte de state
                status = feedback[i][j]
                if status:
                    text = "Validée" if status == "bien" else "À déplacer"
                    color = GREEN if status == "bien" else ORANGE
                    label = small_font.render(text, True, color)
                    label_x = (row_x + j * 90) - (label.get_width() // 2)
                    label_y = y_offset + 35
                    screen.blit(label, (label_x, label_y))

            y_offset += 70  # espace entre les ligne 

        for i, c in enumerate(current_guess):
            center = current_slot_center(i)
            if c:
                pygame.draw.circle(screen, color_rgb[c], center, 35)
            else:
                pygame.draw.circle(screen, GREY, center, 35, 2)
            if selected_index == i:
                pygame.draw.circle(screen, (255, 150, 180), center, 40, 3)

        for rect, c in color_buttons:
            pygame.draw.circle(screen, color_rgb[c], rect.center, 35)
            pygame.draw.circle(screen, GREY, rect.center, 35, 2)

        if tip_message:
            tip = small_font.render(tip_message, True, (100, 80, 80))
            screen.blit(tip, (screen_width // 2 - tip.get_width() // 2, screen_height - 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos

                for i in range(combo_length):
                    cx, cy = current_slot_center(i)
                    dist = ((pos[0] - cx) ** 2 + (pos[1] - cy) ** 2) ** 0.5
                    if dist < 35:
                        selected_index = i if selected_index != i else None

                for rect, c in color_buttons:
                    if rect.collidepoint(pos):
                        if selected_index is not None:
                            current_guess[selected_index] = c
                            selected_index = None
                        else:
                            for i in range(combo_length):
                                if current_guess[i] is None:
                                    current_guess[i] = c
                                    break

                if None not in current_guess:
                    well_placed = 0
                    badly_placed = 0
                    statuses = [""] * combo_length
                    secret_copy = secret_combo.copy()
                    guess_copy = current_guess.copy()
                    tip_message = ""

                    for i in range(combo_length):
                        if guess_copy[i] == secret_copy[i]:
                            well_placed += 1
                            statuses[i] = "bien"
                            secret_copy[i] = None
                            guess_copy[i] = None

                    for i in range(combo_length):
                        if guess_copy[i] is not None and guess_copy[i] in secret_copy:
                            badly_placed += 1
                            statuses[i] = "mal"
                            secret_copy[secret_copy.index(guess_copy[i])] = None

                    attempts.append(current_guess.copy())
                    feedback.append(statuses)
                    turn_count += 1
                    current_guess = [None] * combo_length
                    selected_index = None

                    if well_placed == combo_length:
                        victory = True
                        game_over = True
                    elif turn_count >= max_turns:
                        victory = False
                        game_over = True

    # fin du jeu
    if victory:
        return show_end_screen("YOUPIIIII t'as réussi !!!", color=GREEN)
    else:
        solution = " ".join(secret_combo)
        return show_end_screen("Dommage, c'est perdu !", f"La combinaison était : [{solution}]", color=PINK)

if __name__ == "__main__":
    while True:
        show_menu()
        result = play_game()
        if result == "replay":
            continue
        else:
            pygame.quit()
            sys.exit()
