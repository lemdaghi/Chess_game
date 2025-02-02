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
    
    # def is_in_check(self, color):
    #     """Retourne True si le Roi de 'color' est en échec."""
    #     king = None

    #     # Trouver le Roi
    #     for row in range(8):
    #         for col in range(8):
    #             piece = self.board.grid[row][col]  # ✅ On accède bien à `self.grid`
    #             if piece and piece.__class__.__name__ == "King" and piece.color == color:
    #                 king = piece
    #                 break

    #     if not king:
    #         print("🚨 ERREUR: Le Roi n'a pas été trouvé sur l'échiquier !")
    #         return False  # Évite le crash

    #     print(f"🔎 Vérification de l'échec contre {color.capitalize()} à {king.position}")

    #     # Vérifier si une pièce adverse attaque le Roi
    #     for row in self.board.grid:
    #         for piece in row:
    #             if piece and piece.color != color:
    #                 moves = piece.get_moves(self.board)  # ✅ Passe `self`, qui est bien `Board`
    #                 print(f"🔍 {piece.symbol} ({piece.__class__.__name__}) en {piece.position} peut attaquer {moves}")
    #                 if king.position in moves:
    #                     print(f"⚠️ {piece.symbol} ({piece.__class__.__name__}) attaque le Roi !")
    #                     return True  # Le Roi est attaqué

    #     return False  # Le Roi est en sécurité


        
    # def is_checkmate(self, color):
    #     """ Return True if the player 'color' is checkmated """
    #     if not self.is_in_check(color):
    #         return False  # No check, No mat
               
    #     king = None
    #     attackers = []  # List of opponent pieces that are checking the king

    #     # Found the king of the current_player
    #     for row in range(8):
    #         for col in range(8):
    #             piece = self.board.grid[row][col]
    #             if piece:
    #                 if piece.__class__.__name__ == "King" and piece.color == color:
    #                     king = piece
    #                 elif piece.color != color:
    #                     moves = piece.get_moves(self.board)
    #                     print(f"🔍 {piece.symbol} ({piece.__class__.__name__}) en {piece.position} a ces mouvements : {moves}")
    #                     if king and king.position in moves:
    #                         attackers.append(piece)
    #                         print(f"⚠️ {piece.symbol} attaque le Roi !")

    #     if not king:
    #         return False  # Impossible
        
    #     if not attackers:
    #         print("🚨 ERREUR: Aucun attaquant trouvé, mais `is_checkmate` a été appelé !")
    #         return False 
    #     print(f"👑 {color.capitalize()} est en échec par {len(attackers)} pièce(s) : {[p.symbol for p in attackers]}") 
        
    #     # 1️⃣ Verify if the king can escape
    #     original_position = king.position

    #     target_piece = None
    #     for move in king.get_moves(self.board):

    #         if self.board.get_piece(move):
    #             target_piece = self.board.get_piece(move)
    #         self.board.move_piece(king, move) # Test the move

    #         if not self.is_in_check(color):  # if the king is no more checked
    #             self.board.move_piece(king, original_position)  # Restore the king position
    #             if target_piece:
    #                 self.board.grid[move[1]][move[0]] = target_piece # Restore the eaten piece
    #             return False
    #     self.board.move_piece(king, original_position)  # Restore the state
    #     if target_piece:
    #         self.board.grid[move[1]][move[0]] = target_piece # Restore the eaten piece

    #     # The King can not escape
    #     if len(attackers) > 1:
    #         return True  # It's a checkmate
        
    #     # 2️⃣ Verify if a piece can eat the attacker
    #     attacker = attackers[0]
    #     for row in range(8):
    #         for col in range(8):
    #             piece = self.board.grid[row][col]
    #             if piece and piece.color == color:
    #                 if attacker.position in piece.get_moves(self.board): 
    #                     return False
        
    #     # 3️⃣ Verify if a piece can parry the attack
    #     if attacker.__class__.__name__ == "Knight":
    #         return True # Can not parry a Kinght attack

    #     x1, y1 = king.position
    #     x2, y2 = attacker.position
    #     path = [] 

    #     dx = (x2 - x1) // max(1, abs(x2 - x1))  # 0 if same row, else 1
    #     dy = (y2 - y1) // max(1, abs(y2 - y1))  # 0 if same col, else 1

    #     nx, ny = x1 + dx, y1 + dy
    #     while (nx, ny) != (x2, y2):
    #         path.append((nx, ny))
    #         nx += dx
    #         ny += dy

    #     for row in range(8):
    #         for col in range(8):
    #             piece = self.board.grid[row][col]
    #             if piece and piece.color == color:
    #                 for move in piece.get_moves(self.board):
    #                     if move in path:
    #                         return False
                        
    #     return True  # The king is checkmat

    # def check_victory(self):
    #     if self.is_in_check("white") and self.is_checkmate("white"):
    #         print("🏆 Victoire des Noirs par échec et mat !")
    #         self.game_over = True
    #     elif self.is_in_check("black") and self.is_checkmate("black"):
    #         print("🏆 Victoire des Blancs par échec et mat !")
    #         self.game_over = True

# TODO: if the piece is nailed
# TODO: en passant
# TODO: illegal moves (for king)
# TODO; Castle