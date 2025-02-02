import pygame
from pieces import Pawn, Rook, Bishop, Knight, Queen, King  
import copy  

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]  
        self.selected_piece = None 
        self.valid_moves = [] 

        # Pawns
        for col in range(8):
            self.grid[6][col] = Pawn("white", (col, 6), f"assets/pawn_white.png")
            self.grid[1][col] = Pawn("black", (col, 1), f"assets/pawn_black.png")

        # Rooks
        self.grid[7][0] = Rook("white", (0, 7), f"assets/rook_white.png")
        self.grid[7][7] = Rook("white", (7, 7), f"assets/rook_white.png")
        self.grid[0][7] = Rook("black", (7, 0), f"assets/rook_black.png")
        self.grid[0][0] = Rook("black", (0, 0), f"assets/rook_black.png")

        # Knights
        self.grid[7][6] = Knight("white", (6, 7), f"assets/knight_white.png")
        self.grid[7][1] = Knight("white", (1, 7), f"assets/knight_white.png")
        self.grid[0][1] = Knight("black", (1, 0), f"assets/knight_black.png")
        self.grid[0][6] = Knight("black", (6, 0), f"assets/knight_black.png")

        # Bishops
        self.grid[7][5] = Bishop("white", (5, 7), f"assets/bishop_white.png")
        self.grid[7][2] = Bishop("white", (2, 7), f"assets/bishop_white.png")
        self.grid[0][2] = Bishop("black", (2, 0), f"assets/bishop_black.png")
        self.grid[0][5] = Bishop("black", (5, 0), f"assets/bishop_black.png")

        # Queens
        self.grid[7][3] = Queen("white", (3, 7), f"assets/queen_white.png")
        self.grid[0][3] = Queen("black", (3, 0), f"assets/queen_black.png")

        # Kings
        self.grid[7][4] = King("white", (4, 7), f"assets/king_white.png")
        self.grid[0][4] = King("black", (4, 0), f"assets/king_black.png")

    def draw(self, screen):
        SQUARE_SIZE = 75
        WHITE = (238, 238, 210)
        BLACK = (118, 150, 86)

        for row in range(8):
            for col in range(8):
                color = WHITE if (row + col) % 2 == 0 else BLACK
                pygame.draw.rect(screen, color, 
                                (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

        for row in range(8):
             for col in range(8):
                piece = self.grid[row][col]
                if piece:
                    piece.draw(screen)

    def get_piece(self, position):
        x, y = position
        return self.grid[y][x]
    
    def move_piece(self, piece, new_position):
        old_position = piece.position
        x, y = old_position
        new_x, new_y = new_position

        captured_piece = self.grid[new_y][new_x] 
         
        if captured_piece and isinstance(captured_piece, King) and piece.color != captured_piece.color:
            print(f"🚨 Mouvement illégal de {piece.color} {piece.__class__.__name__}: Un Roi ne peut pas être capturé !")
            return False
            
        self.grid[y][x] = None  
        self.grid[new_y][new_x] = piece  
        piece.position = (new_x, new_y)  
        piece.first_move = False  

        return True

    def pos_to_chess_notation(self, position):
        """Convert position (x, y) to ('a1', 'h8')."""
        files = "abcdefgh"
        return f"{files[position[0]]}{8 - position[1]}"  # Ex: (4,6) → "e2"
    
    def copy(self):
        """Retourne une copie du plateau sans copier les images pygame."""
        new_board = Board()
        for y in range(8):
            for x in range(8):
                piece = self.grid[y][x]
                if piece:
                    # ✅ Crée une nouvelle instance de la pièce avec son `image_path`
                    new_piece = piece.__class__(piece.color, piece.position, piece.image_path)
                    new_piece.first_move = piece.first_move  # ✅ Garde l'info du premier mouvement
                    new_board.grid[y][x] = new_piece
        return new_board
