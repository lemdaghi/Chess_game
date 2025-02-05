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
    
    return time_modes.get(choice, "rapid")  # Default to Blitz

pygame.init()
WIDTH, HEIGHT = 600, 600
SQUARE_SIZE = WIDTH // 8
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")

selected_time_control = choose_time_control()
game = Game(time_control=selected_time_control)
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            game.handle_click(pygame.mouse.get_pos())
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_u:  # "U" pour Undo
                game.undo_move()
            elif event.key == pygame.K_r:  # "R" pour Restart
                game.restart_game()

    font = pygame.font.Font(None, 24)
    for index, move in enumerate(game.get_move_history()):
        text_surface = font.render(move, True, (255, 255, 255))
        screen.blit(text_surface, (10, 10 + index * 20))  # Affiche l'historique en haut à gauche

    screen.fill((0, 0, 0))  
    game.board.draw(screen)
    pygame.display.flip()

pygame.quit()
