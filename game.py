import pygame
from board import Board

class Game:
    def __init__(self):
        self.board = Board()
        self.current_player = "white"
        self.game_over = False

    def handle_click(self, position):
        ''' Manage click on the board '''
        if self.game_over:
            return
        
        x, y = position[0] // 75, position[1] // 75 # convert pixel to grid
        clicked_piece = self.board.get_piece((x, y))

        if self.board.selected_piece: # a piece is already selected
            if(x,y) in self.board.valid_moves: # we are trying to move the piece to valid position
                self.board.move_piece(self.board.selected_piece, (x,y))
                self.switch_turn()
                self.check_victory()
            self.board.selected_piece = None
            self.board.valid_moves = [] 

        elif clicked_piece and clicked_piece.color == self.current_player: # We just selected a piece, making sure the player selected his own pieces
            self.board.selected_piece = clicked_piece
            self.board.valid_moves = clicked_piece.get_moves(self.board)


    def switch_turn(self):
        if self.current_player == "white":
            self.current_player = "black"
        else:
            self.current_player = "white"
    
    def is_in_check(self, color):
        """ Return True if the 'color' king is checked """
        king = None

        # Trouver le roi du joueur actuel
        for row in range(8):
            for col in range(8):
                piece = self.board.grid[row][col]
                if piece and piece.__class__.__name__ == "King" and piece.color == color:
                    king = piece
                    break

        if not king:
            return False  # Impossible

        # Vérifier si une pièce adverse attaque le roi
        for row in self.board.grid:
            for piece in row:
                if piece and piece.color != color:
                    if king.position in piece.get_moves(self.board):
                        return True  # Le roi est attaqué

        return False  # Le roi est en sécurité

        
    def is_checkmate(self, color):
        """ Return True if the player 'color' is checkmated """
        print("cheching checkmate")
        if not self.is_in_check(color):
            return False  # No check, No mat
               
        king = None
        attackers = []  # List of opponent pieces that are checking the king

        # Found the king of the current_player
        for row in range(8):
            for col in range(8):
                piece = self.board.grid[row][col]
                if piece and piece.__class__.__name__ == "King" and piece.color == color:
                    king = piece
                elif piece and piece.color != color and king.position in piece.get_moves(self.board):
                    attackers.append(piece)  # Add the piece to attackers list

        if not king:
            return False  # Impossible

        # 1️⃣ Verify if the king can escape
        original_position = king.position

        for move in king.get_moves(self.board):
            target_piece = self.board.get_piece(move)
            self.board.move_piece(king, move) # Test the move

            if not self.is_in_check(color):  # if the king is no more checked
                self.board.move_piece(king, original_position)  # Restore the king position
                self.board.grid[move[1]][move[0]] = target_piece # Restore the eaten piece
                return False
        self.board.move_piece(king, original_position)  # Restore the state
        self.board.grid[move[1]][move[0]] = target_piece # Restore the eaten piece

        # The King can not escape
        if len(attackers) > 1:
            return True  # It's a checkmate
        
        # 2️⃣ Verify if a piece can eat the attacker
        attacker = attackers[0]
        for row in range(8):
            for col in range(8):
                piece = self.board.grid[row][col]
                if piece and piece.color == color:
                    if attacker.position in piece.get_moves(self.board): 
                        return False
        
        # 3️⃣ Verify if a piece can parry the attack
        if attacker.__class__.__name__ == "Knight":
            return True # Can not parry a Kinght attack

        x1, y1 = king.position
        x2, y2 = attacker.position
        path = [] 

        dx = (x2 - x1) // max(1, abs(x2 - x1))  # 0 if same row, else 1
        dy = (y2 - y1) // max(1, abs(y2 - y1))  # 0 if same col, else 1

        nx, ny = x1 + dx, y1 + dy
        while (nx, ny) != (x2, y2):
            path.append((nx, ny))
            nx += dx
            ny += dy

        for row in range(8):
            for col in range(8):
                piece = self.board.grid[row][col]
                if piece and piece.color == color:
                    for move in piece.get_moves(self.board):
                        if move in path:
                            return False
                        
        return True  # The king is checkmat

    def check_victory(self):
        if self.is_checkmate("white"):
            print("Victoire des Noirs par échec et mat !")
            self.game_over = True
            return
        elif self.is_checkmate("black"):
            print("Victoire des Blancs par échec et mat !")
            self.game_over = True
            return

# TODO: if the piece is nailed
# TODO: en passant
# TODO: illegal moves (for king)
# TODO; Castle