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
        if not self.is_in_check(color):
            return False  # No check, No mat
               
        king = None

        # Found the king of the current_player
        for row in range(8):
            for col in range(8):
                piece = self.board.grid[row][col]
                if piece and piece.__class__.__name__ == "King" and piece.color == color:
                    king = piece
                    break

        if not king:
            return False  # Impossible

        # Verify if the king can escape
        for move in king.get_moves(self.board):
            temp_board = self.board  # Save temporarily
            self.board.move_piece(king, move)  # Test the move
            if not self.is_in_check(color):  # if the king is no more checked
                self.board = temp_board  # Restore the state
                return False
        self.board = temp_board  # Restore the state
        
        # TO DO: Add the case where another piece can protect him by eating the piece or by interception
        return True  # The king is checkmat

    def check_victory(self):
        if self.is_checkmate("white"):
            print("Victoire des Noirs par échec et mat !")
            self.game_over = True
        elif self.is_checkmate("black"):
            print("Victoire des Blancs par échec et mat !")
            self.game_over = True
