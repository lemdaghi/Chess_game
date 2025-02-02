import pygame
from game import Game
import os
print(os.listdir("assets/"))

pygame.init()
WIDTH, HEIGHT = 600, 600
SQUARE_SIZE = WIDTH // 8
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")

WHITE = (238, 238, 210)
BLACK = (118, 150, 86)

def draw_board():
    """Dessine un échiquier correctement alterné."""
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else BLACK  
            pygame.draw.rect(screen, color, 
                             (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            
game = Game()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            game.handle_click(pygame.mouse.get_pos())

    screen.fill((0, 0, 0))  # Fond noir
    game.board.draw(screen)

    # draw_board()
    pygame.display.flip()

pygame.quit()



# # Initialisation
# pygame.init()
# WIDTH, HEIGHT = 600, 600
# SQUARE_SIZE = WIDTH // 8
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Jeu d'échecs")

# # Couleurs
# WHITE = (238, 238, 210)
# BLACK = (118, 150, 86)

# # Fonction pour dessiner l’échiquier
# def draw_board():
#     for row in range(8):
#         for col in range(8):
#             color = WHITE if (row + col) % 2 == 0 else BLACK
#             pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# # Boucle principale
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     draw_board()
#     pygame.display.flip()

# pygame.quit()
