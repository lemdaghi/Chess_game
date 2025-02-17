import pygame
from game import Game

def choose_time_control():
    print("\n🎯 Select a Time Control:")
    print("1️⃣ Bullet (1 min)")
    print("2️⃣ Blitz (5 min)")
    print("3️⃣ Rapid (10 min) [Default]")
    print("4️⃣ Classical (1 hour)")

    choice = input("👉 Enter a number (1-4): ")

    time_modes = {
        "1": "bullet",
        "2": "blitz",
        "3": "rapid",
        "4": "classical"
    }
    
    return time_modes.get(choice, "rapid")  # Default to Rapid

def get_player_mode():
    """Prompt the user to choose between playing with another player or AI."""
    print("Welcome to Chess!")
    print("Choose your mode:")
    print("1. Two Players")
    print("2. Play Against AI")
    
    choice = input("Enter 1 or 2: ").strip()
    if choice == "1":
        return "two_players"
    elif choice == "2":
        return "vs_ai"
    else:
        print("Invalid choice. Defaulting to Two Players mode.")
        return "two_players"

pygame.init()
WIDTH, HEIGHT = 600, 600
SQUARE_SIZE = WIDTH // 8
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")

player_mode = get_player_mode()
selected_time_control = choose_time_control()
game = Game(mode = player_mode, time_control = selected_time_control)
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            game.handle_click(pygame.mouse.get_pos())
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_u:  # "U" for Undo
                if player_mode == "vs_ai":
                    game.undo_move()
                game.undo_move()
            elif event.key == pygame.K_r:  # "R" for Restart
                game.restart_game()

    font = pygame.font.Font(None, 24)
    for index, move in enumerate(game.get_move_history()):
        text_surface = font.render(move, True, (255, 255, 255))
        screen.blit(text_surface, (10, 10 + index * 20))  # Displays history at top left

    screen.fill((0, 0, 0))  
    game.board.draw(screen)
    pygame.display.flip()

pygame.quit()
