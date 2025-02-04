import pygame
from board import Board
from chess_rules import ChessRules

class Game:
    def __init__(self):
        self.board = Board()
        self.current_player = "white"
        self.game_over = False
        self.move_history = []
        self.history = []
        self.count_moves = 0

    def handle_click(self, position):
        if self.game_over:
            print("🚫 La partie est terminée.")
            self.propose_rematch()
            return
        
        x, y = position[0] // 75, position[1] // 75
        clicked_piece = self.board.get_piece((x, y))

        if self.board.selected_piece:
            if (x, y) in self.board.valid_moves:
                old_position = self.board.selected_piece.position
                self.history.append((self.board.copy(), self.count_moves)) # save board before moving
                self.print_board(self.board)

                legal_move = self.board.move_piece(self.board.selected_piece, (x, y))

                if legal_move:
                    move_description = f"{self.board.selected_piece.symbol} {self.board.pos_to_chess_notation(old_position)} → {self.board.pos_to_chess_notation((x, y))}"
                    self.move_history.append(move_description)
                    print(move_description)

                    print("🔍 État après coup :")
                    self.print_board(self.board)

                    # ✅ Réinitialiser le compteur si un pion bouge ou si une capture est faite
                    if self.board.selected_piece.__class__.__name__ == "Pawn" or (clicked_piece is not None and clicked_piece.color != self.board.get_piece((x, y)).color):
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
            self.board.valid_moves = [move for move in clicked_piece.get_moves(self.board) if self.board.check_legal_move(clicked_piece, move)]

    def switch_turn(self):
        if self.current_player == "white":
            self.current_player = "black"
        else:
            self.current_player = "white"

    def print_board(self, board):
        """Affiche l'échiquier dans le terminal pour debug."""
        print("\n   a b c d e f g h")
        print("  -----------------")
        for y in range(8):
            row_str = f"{8 - y} | "
            for x in range(8):
                piece = board.grid[y][x]
                row_str += piece.symbol if piece else "·"
                row_str += " "
            print(row_str + f"| {8 - y}")
        print("  -----------------")
        print("   a b c d e f g h\n")

    def get_move_history(self):
        """Retourne l'historique des coups joués."""
        return self.move_history

    def undo_move(self):
        if self.history:
            print("📜 Dernier état enregistré avant annulation :")
            self.print_board(self.history[-1][0])

            last_board, last_count_moves = self.history.pop()  # ✅ Restaure l'état du plateau avant le dernier coup

            self.board.grid = last_board.grid
            self.current_player = "white" if self.current_player == "black" else "black"
            self.count_moves = last_count_moves
            
            print(f"⏳ 50 Moves Rule after undo : {self.count_moves}/100")

            # ✅ Supprimer le dernier état de position_history pour éviter les erreurs de répétition
            if isinstance(self.board.position_history, dict) and self.board.position_history:
                last_key = list(self.board.position_history.keys())[-1]  # Récupère la dernière clé (Python Version >= 3.7, les dictionnaires conservent l'ordre d'ajout)
                print(f"🗑 Suppression de la dernière position enregistrée : {last_key}")
                self.board.position_history.pop(last_key)

            # ✅ DEBUG : Afficher l'état du plateau après annulation
            print("🔙 État de la grille après annulation :")
            self.print_board(self.board)

            if self.move_history:
                self.move_history.pop()
            print("🔄 Annulation : Le dernier coup a été annulé.")
        else:
            print("🚫 Aucun coup à annuler.")

    def restart_game(self):
        self.board = Board()  # ✅ Réinitialise l'échiquier
        self.current_player = "white"
        self.game_over = False
        self.move_history = []
        self.history = []  # ✅ Efface l'historique
        self.count_moves = 0
        print("🔄 La partie a été redémarrée.")

    def propose_rematch(self):
        """Propose a rematch and reset the game if accepted."""
        response = input("🔄 Do you want a rematch? (yes/no): ").strip().lower()
        if response == "yes":
            self.restart_game()
        else:
            print("🎉 Game over! Thanks for playing!")


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
            return
        elif ChessRules.is_checkmate(self.board, "black"):
            print("🏆 Victoire des Blancs par échec et mat !")
            self.game_over = True
            return
        
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
            return

        