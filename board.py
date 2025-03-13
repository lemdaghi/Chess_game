import pygame
from pieces import Pawn, Rook, Bishop, Knight, Queen, King  
import copy  

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]  
        self.selected_piece = None 
        self.valid_moves = [] 
        self.last_move = None # save last move
        self.position_history = {}

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
        GREEN = (0, 255, 0)

        # Draw Board
        for row in range(8):
            for col in range(8):
                color = WHITE if (row + col) % 2 == 0 else BLACK
                pygame.draw.rect(screen, color, 
                                (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

        # Draw Pieces
        for row in range(8):
             for col in range(8):
                piece = self.grid[row][col]
                if piece:
                    piece.draw(screen)

        # Draw Points on valid cases to move on
        if self.selected_piece:
            for move in self.valid_moves:
                move_x, move_y = move
                center_x = move_x * SQUARE_SIZE + SQUARE_SIZE // 2
                center_y = move_y * SQUARE_SIZE + SQUARE_SIZE // 2
                pygame.draw.circle(screen, GREEN, (center_x, center_y), 10)

    def get_piece(self, position):
        x, y = position
        return self.grid[y][x]

    def move_piece(self, piece, new_position):
        from chess_rules import ChessRules  

        old_position = piece.position
        x, y = old_position
        new_x, new_y = new_position

        captured_piece = self.grid[new_y][new_x]  

        if captured_piece and isinstance(captured_piece, King) and piece.color != captured_piece.color:
            print(f"🚨 Illegal move of {piece.color} {piece.__class__.__name__}: a king can not be captured !")
            return False

        # Castle Verification
        if isinstance(piece, King) and abs(new_x - x) == 2:
            print("♔ King Castle Verification...")
            
            # Verify the king didn't move yet
            if not piece.first_move:
                return False

            # Verify if the king is not checked
            if ChessRules.is_in_check(self, piece.color):
                print("🚫 Illegal Castle : the king is checked !")
                return False  

            # Define Castle type
            if new_x == 6:  # Kingside
                print("Small Castling")
                rook_x, rook_new_x = 7, 5
                path = [(5, y), (6, y)]  # Squares crossed by the king
            elif new_x == 2:  # Queenside
                print("Big Castling")
                rook_x, rook_new_x = 0, 3
                path = [(3, y), (2, y)]  # Squares crossed by the king
            else:
                return False  # Not a castle

            # Verify the tour was not moved
            rook = self.get_piece((rook_x, y))
            if not rook.first_move:
                return False
            
            rook = self.grid[y][rook_x]
            if not rook or not isinstance(rook, Rook) or not rook.first_move:
                print("🚫 Illegal Castle : the Rook already moved !")
                return False
            
            # Verify cases in between are empty
            if any(self.get_piece(pos) is not None for pos in path):
                print("🚫 Illegal Castle : a piece is in the road !")
                return False  

            # Verify if the king pass by an attacked square
            for pos in path:
                if ChessRules.is_in_check(self, piece.color, pos):
                    print(f"🚫 Illegal Castle : king pass by an attacked square {pos} !")
                    return False  

            # First move the king
            self.grid[y][x] = None  
            self.grid[y][new_x] = piece  
            piece.position = (new_x, y)  

            # Move Rook
            self.grid[y][rook_x] = None  
            self.grid[y][rook_new_x] = rook  
            rook.position = (rook_new_x, y)  

            # Set King's and Rook's first move to False
            piece.first_move = False  
            rook.first_move = False  

            print("✅ Castle Successfully completed !")
            return True  
        
        # Verify pawn promotion
        if isinstance(piece, Pawn) and (new_y == 0 or new_y == 7):
            print(f"♟️ {piece.color} Pawn reached last row ({new_y}) : Promotion is required !")            
            promoted_piece = self.promote_pawn(piece) # Select the promoted piece
            self.grid[new_y][new_x] = promoted_piece  # Replace pawn by the promoted piece
            piece = promoted_piece  # Update the reference
            print(f"🎉 {piece.color} Pawn promoted to {piece.symbol} !")
        
        # "En Passant" Rule
        if isinstance(piece, Pawn) and self.last_move:
            last_piece, (old_x, old_y), (last_new_x, last_new_y) = self.last_move

            if isinstance(last_piece, Pawn) and last_piece.color != piece.color:
                if abs(old_y - last_new_y) == 2 and old_x == last_new_x: 
                    direction = (1 if piece.color == "white" else -1)
                    if (new_x, new_y) == (last_new_x, y - direction) and y == last_new_y:
                        print(f"♟️ Took 'En Passant' {last_piece.symbol} in {last_new_x}, {last_new_y}")
                        self.grid[last_new_y][last_new_x] = None 
                        captured_piece = last_piece

        # Verify a classic move if it is legal
        self.grid[y][x] = None  # Remove the piece from its position
        self.grid[new_y][new_x] = piece  # Replace it in the new square in the grid
        piece.position = (new_x, new_y)  # Update position

        # Verify King opposition
        if isinstance(piece, King) and self.is_king_opposition(piece):
            print(f"🚫 Illegal move ! {piece.color} Kings can not be next to each other !")

            # Restore initial setting
            self.grid[new_y][new_x] = captured_piece
            self.grid[y][x] = piece  # Replace king to its initial position in the grid
            piece.position = old_position  # Update position

            return False  # Illegal move: King opposition

        # Verify if a piece is pinned 
        if not isinstance(piece, King) and ChessRules.is_in_check(self, piece.color):
            print(f"🚫 Illegal move ! {piece.symbol} ({piece.__class__.__name__}) is pinned and can not move !")

            # ✅ Undo the move
            self.grid[new_y][new_x] = captured_piece  
            self.grid[y][x] = piece  
            piece.position = old_position 
            
            return False  # Illegal move: pinned piece

        piece.first_move = False  

        # Save last move played
        self.last_move = (piece, old_position, new_position)

        return True

    def is_king_opposition(self, king):
        """Verify if two kings are next to each other"""
        print("King opposition verification")
        x, y = king.position
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                piece = self.get_piece((nx, ny))
                if piece and isinstance(piece, King) and piece.color != king.color:
                    print(f"🚫 Illegal move : King opposition detected in {king.position} !")
                    return True  # King opposition

        return False  # No King opposition
    
    def promote_pawn(self, piece):
        """Allow user to choose the promoted piece"""
        choices = {
            "Q": Queen(piece.color, piece.position, f"assets/queen_{piece.color}.png"),
            "R": Rook(piece.color, piece.position, f"assets/rook_{piece.color}.png"),
            "B": Bishop(piece.color, piece.position, f"assets/bishop_{piece.color}.png"),
            "N": Knight(piece.color, piece.position, f"assets/knight_{piece.color}.png"),
        }
        
        while True:
            choice = input("♟️ Promotion ! Choose (Q)Queen, (R)Rook, (B)Bishop, (N)Knight: ").upper()
            if choice in choices:
                return choices[choice]
            print("❌ Invalid choice, retry.")

    def check_legal_move(self, piece, new_position):
        """Return true if the move is legal, else False."""
        from chess_rules import ChessRules  

        old_position = piece.position
        x, y = old_position
        new_x, new_y = new_position
        captured_piece = self.grid[new_y][new_x]  # Save the captured piece (if it exists)

        # Simulate the move
        self.grid[y][x] = None  
        self.grid[new_y][new_x] = piece  
        piece.position = (new_x, new_y)  

        # Verify king opposition
        if isinstance(piece, King) and self.is_king_opposition(piece):
            print(f"🚫 Illegal move ! {piece.color} Kings can not be next to each other !")

            # Restore initial state
            self.grid[new_y][new_x] = captured_piece
            self.grid[y][x] = piece  
            piece.position = old_position  

            return False  # Illegal move !

        # Verify King check
        if ChessRules.is_in_check(self, piece.color):

            # Restore initial state
            self.grid[new_y][new_x] = captured_piece  
            self.grid[y][x] = piece  
            piece.position = old_position  

            return False  # Illegal move !

        # Restore position after simulation
        self.grid[new_y][new_x] = captured_piece  
        self.grid[y][x] = piece  
        piece.position = old_position  

        return True  # Legal Move !

    def record_position(self):
        """Save current position of the grid"""
        position_key = tuple((piece.__class__.__name__, piece.color, piece.position) for row in self.grid for piece in row if piece)
        if position_key in self.position_history:
            self.position_history[position_key] += 1
        else:
            self.position_history[position_key] = 1

    def is_triple_repetition(self):
        """Return true if the same position was repeated 3 times"""
        for count in self.position_history.values():
            if count >= 3:
                print("⚖️ Draw by threefold !")
                return True
        return False

    def pos_to_chess_notation(self, position):
        """Convert position (x, y) to ('a1', 'h8')."""
        files = "abcdefgh"
        return f"{files[position[0]]}{8 - position[1]}"  # Ex: (4,6) → "e2"
    
    def copy(self):
        """Return a copy of the grid."""
        new_board = Board()
        new_board.grid = [[None for _ in range(8)] for _ in range(8)]

        for y in range(8):
            for x in range(8):
                piece = self.grid[y][x]
                if piece:
                    # Create a new instance of the piece with its image_path
                    new_piece = piece.__class__(piece.color, piece.position, piece.image_path)
                    new_piece.first_move = piece.first_move  # Save first move value
                    new_board.grid[y][x] = new_piece
        return new_board
