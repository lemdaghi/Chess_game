import pygame
from game import Game

pygame.init()
WIDTH, HEIGHT = 600, 600
SQUARE_SIZE = WIDTH // 8
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")

game = Game()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            game.handle_click(pygame.mouse.get_pos())

    font = pygame.font.Font(None, 24)
    for index, move in enumerate(game.get_move_history()):
        text_surface = font.render(move, True, (255, 255, 255))
        screen.blit(text_surface, (10, 10 + index * 20))  # Affiche l'historique en haut à gauche

    screen.fill((0, 0, 0))  
    game.board.draw(screen)
    pygame.display.flip()

pygame.quit()
