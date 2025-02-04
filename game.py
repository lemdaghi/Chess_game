import pygame
from board import Board
from chess_rules import ChessRules

class Game:
    def __init__(self):
        self.board = Board()
        self.current_player = "white"
        self.game_over = False
        self.move_history = []

    def handle_click(self, position):
        ''' Manage click on the board '''
        if self.game_over:
            print("game over")
            return
        
        x, y = position[0] // 75, position[1] // 75 # convert pixel to grid
        clicked_piece = self.board.get_piece((x, y))

        if self.board.selected_piece: # a piece is already selected
            if(x,y) in self.board.valid_moves: # we are trying to move the piece to valid position
                old_position = self.board.selected_piece.position
                legal_move = self.board.move_piece(self.board.selected_piece, (x,y))
                if legal_move:
                    move_description = f"{self.board.selected_piece.symbol} {self.board.pos_to_chess_notation(old_position)} → {self.board.pos_to_chess_notation((x, y))}"
                    self.move_history.append(move_description)
                    print(move_description)
                    self.switch_turn()
                    self.check_victory()
                else:
                    print("🚫 Mouvement illégal !")
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

    def get_move_history(self):
        """Retourne l'historique des coups joués."""
        return self.move_history


    def check_victory(self):
        """Vérifie si la partie est terminée par échec et mat."""
        if ChessRules.is_checkmate(self.board, "white"):
            print("🏆 Victoire des Noirs par échec et mat !")
            self.game_over = True
        elif ChessRules.is_checkmate(self.board, "black"):
            print("🏆 Victoire des Blancs par échec et mat !")
            self.game_over = True
        
        if ChessRules.is_stalemate(self.board, self.current_player):
            print("⚖️ Partie nulle par PAT !")
            self.game_over = True
            return

        if ChessRules.is_insufficient_material(self.board):
            print("⚖️ Partie nulle par manque de matériel !")
            self.game_over = True
            return
# TODO: Pawn transformation