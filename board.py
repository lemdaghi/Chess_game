import pygame
from pieces import Piece, Pawn, Rook, Bishop, Knight, Queen, King  # Import de la classe mère

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]  # Empty grid
        self.selected_piece = None 
        self.valid_moves = [] # valid cases to move in

        # Pawns
        for col in range(8):
            self.grid[6][col] = Pawn("white", (col, 6), f"assets/pawn_white.png")
            self.grid[1][col] = Pawn("black", (col, 1), f"assets/pawn_black.png")

        # Rooks
        self.grid[7][0] = Rook("white", (0, 7), f"assets/rook_white.png")
        self.grid[7][7] = Rook("white", (7, 7), f"assets/rook_white.png")
        self.grid[0][7] = Rook("black", (7, 0), f"assets/rook_black.png")
        self.grid[0][0] = Rook("black", (0, 0), f"assets/rook_black.png")

        # Knight
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
        
    def pos_to_chess_notation(self, position):
        """Convert position (x, y) to ('a1', 'h8')."""
        files = "abcdefgh"
        return f"{files[position[0]]}{8 - position[1]}"  # Ex: (4,6) → "e2"
    
    def move_piece(self, piece, new_position):
        ''' Move a piece on the board '''
        old_position = piece.position
        x, y = old_position
        new_x, new_y = new_position
        
        captured_piece = self.grid[new_y][new_x]  # Verify if a piece is captured
        if captured_piece and captured_piece.__class__.__name__ == "King":
            print("🚨 Illegal move : King can not be captured !")
            return False
            
        self.grid[y][x] = None # Delete the piece from the old position in the grid
        self.grid[new_y][new_x] = piece # Put the piece on the new position in the grid
        piece.move(new_position) # Move the piece
        piece.first_move = False # disable first_move

        move_description = f"{piece.symbol} {self.pos_to_chess_notation(old_position)} → {self.pos_to_chess_notation(new_position)}"
        if captured_piece:
            move_description += f" (capture {captured_piece.symbol})"
        self.game.move_history.append(move_description)  # Add history description
        print(move_description) 
        
        return True
    
