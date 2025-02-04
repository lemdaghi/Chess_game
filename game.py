import pygame
from board import Board
from chess_rules import ChessRules

class Game:
    def __init__(self):
        self.board = Board()
        self.current_player = "white"
        self.game_over = False
        self.move_history = []
        self.count_moves = 0

    def handle_click(self, position):
        if self.game_over:
            print("🚫 La partie est terminée.")
            return
        
        x, y = position[0] // 75, position[1] // 75
        clicked_piece = self.board.get_piece((x, y))

        if self.board.selected_piece:
            if (x, y) in self.board.valid_moves:
                old_position = self.board.selected_piece.position
                
                legal_move = self.board.move_piece(self.board.selected_piece, (x, y))

                if legal_move:
                    move_description = f"{self.board.selected_piece.symbol} {self.board.pos_to_chess_notation(old_position)} → {self.board.pos_to_chess_notation((x, y))}"
                    self.move_history.append(move_description)
                    print(move_description)

                    # ✅ Réinitialiser le compteur si un pion bouge ou si une capture est faite
                    if self.board.selected_piece.__class__.__name__ == "Pawn" or (clicked_piece is not None and clicked_piece.color != self.board.get_piece((x, y)).color):
                        print(f"you moved a {self.board.selected_piece.__class__.__name__}")
                        
                        destination = self.board.get_piece((x, y))
                        if destination:
                            print(f"to {destination.position}")
                        self.count_moves = 0
                    else:
                        self.count_moves += 1  # ✅ Incrémentation normale

                    print(f"⏳ 50 Moves Rule: {self.count_moves}/100")

                    self.board.record_position()  # ✅ Enregistrer la position après le coup
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
    
    def is_fifty_move_rule(self):
        """Retourne True si la règle des 50 coups s'applique."""
        if self.count_moves >= 100:  # ✅ 100 demi-coups = 50 coups complets
            print("⚖️ Match nul par la règle des 50 coups !")
            return True
        return False


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
        
        if self.board.is_triple_repetition():
            print("⚖️ Partie nulle par triple répétition !")
            self.game_over = True
            return
        
        if self.is_fifty_move_rule():
            print("⚖️ Partie nulle par la règle des 50 coups !")
            self.game_over = True

# TODO: Pawn transformation