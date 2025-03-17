import random

class AIPlayer:
    def __init__(self, board, color):
        self.board = board
        self.color = color

    def get_random_move(self):
        """Retourne un mouvement légal aléatoire pour l'IA."""
        all_moves = self.get_all_legal_moves()
        if not all_moves:
            return None  # (Stalemate or Checkmate)
        
        return random.choice(all_moves)
    
    def get_best_move(self):
        legal_moves = []
        for row in self.board.grid:
            for piece in row:
                if piece and piece.color == self.color:
                    for move in piece.get_moves(self.board):
                        legal_moves.append((piece, move))

        if not legal_moves:
            return None 

        # sort moves depending on the captured piece's value
        def evaluate_move(move):
            piece, new_position = move
            target_piece = self.board.get_piece(new_position)
            piece_values = {"King": 0, "Queen": 9, "Rook": 5, "Bishop": 3, "Knight": 3, "Pawn": 1}
            return piece_values.get(target_piece.__class__.__name__, 0) if target_piece else 0

        legal_moves.sort(key=evaluate_move, reverse=True)  # sort from best to worst
        return legal_moves[0]  # Choose the best move

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
