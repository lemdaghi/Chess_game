import random

class AIPlayer:
    def __init__(self, board, color):
        self.board = board
        self.color = color

    def get_best_move(self):
        """Retourne un mouvement légal aléatoire pour l'IA."""
        all_moves = self.get_all_legal_moves()
        if not all_moves:
            return None  # (Stalemate or Checkmate)
        
        return random.choice(all_moves)

    def get_all_legal_moves(self):
        """Retourne une liste de tous les mouvements légaux pour l'IA."""
        legal_moves = []
        for row in self.board.grid:
            for piece in row:
                if piece and piece.color == self.color:
                    for move in piece.get_moves(self.board):
                        if self.board.check_legal_move(piece, move):
                            legal_moves.append((piece, move))
        return legal_moves
