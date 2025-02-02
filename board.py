import pygame
from pieces import Piece, Pawn, Rook  # Import de la classe mère

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]  # Empty grid
        self.selected_piece = None 
        self.valid_moves = [] # valid cases to move in

        # Pawns
        for col in range(8):
            self.grid[1][col] = Pawn("white", (col, 1), f"assets/pawn_white.png")
            self.grid[6][col] = Pawn("black", (col, 6), f"assets/pawn_black.png")

        # Rooks
        self.grid[0][7] = Rook("white", (7, 0), f"assets/rook_white.png")
        self.grid[0][0] = Rook("white", (0, 0), f"assets/rook_white.png")
        self.grid[7][0] = Rook("black", (0, 7), f"assets/rook_black.png")
        self.grid[7][7] = Rook("black", (7, 7), f"assets/rook_black.png")

        # Knight
        self.grid[0][6] = Rook("white", (6, 0), f"assets/knight_white.png")
        self.grid[0][1] = Rook("white", (1, 0), f"assets/knight_white.png")
        self.grid[7][1] = Rook("black", (1, 7), f"assets/knight_black.png")
        self.grid[7][6] = Rook("black", (6, 7), f"assets/knight_black.png")

        # Bishops
        self.grid[0][5] = Rook("white", (5, 0), f"assets/bishop_white.png")
        self.grid[0][2] = Rook("white", (2, 0), f"assets/bishop_white.png")
        self.grid[7][2] = Rook("black", (2, 7), f"assets/bishop_black.png")
        self.grid[7][5] = Rook("black", (5, 7), f"assets/bishop_black.png")

        # Queens
        self.grid[0][4] = Rook("white", (4, 0), f"assets/queen_white.png")
        self.grid[7][4] = Rook("black", (4, 7), f"assets/queen_black.png")

        # Kings
        self.grid[0][3] = Rook("white", (3, 0), f"assets/king_white.png")
        self.grid[7][3] = Rook("black", (3, 7), f"assets/king_black.png")
   

    def draw(self, screen):
        ''' Draw the board and pieces '''
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
                    piece.draw(screen) # Draw the piece on the case

    def get_piece(self, position):
        ''' Return a piece from its position '''
        x, y = position
        return self.grid[y][x]
    
    def move_piece(self, piece, new_position):
        ''' Move a piece on the board '''
        x, y = piece.position
        new_x, new_y = new_position
        self.grid[y][x] = None # Delete the piece from the old position in the grid
        self.grid[new_y][new_x] = piece # Put the piece on the new position in the grid
        piece.move(new_position) # Move the piece

    
