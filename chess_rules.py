import pygame

class ChessRules:
    @staticmethod
    def is_in_check(board, color):
        """Retourne True si le Roi de 'color' est en échec."""
        king = None

        # Trouver le Roi
        for row in board.grid:
            for piece in row:
                if piece and piece.__class__.__name__ == "King" and piece.color == color:
                    king = piece
                    break

        if not king:
            print("🚨 ERREUR: Le Roi n'a pas été trouvé sur l'échiquier !")
            return False  # Évite le crash

        # Vérifier si une pièce adverse attaque le Roi
        for row in board.grid:
            for piece in row:
                if piece and piece.color != color:
                    moves = piece.get_moves(board)  # ✅ Appelle uniquement Board, pas Game
                    if king.position in moves:
                        return True  # Le Roi est attaqué

        return False  # Le Roi est en sécurité

    @staticmethod
    def is_checkmate(board, color):
        """Retourne True si le joueur 'color' est échec et mat."""
        if not ChessRules.is_in_check(board, color):
            return False  # Pas en échec, pas de mat

        king = None
        attackers = []

        # Trouver le Roi et les attaquants
        for row in board.grid:
            for piece in row:
                if piece and piece.__class__.__name__ == "King" and piece.color == color:
                    king = piece
                elif piece and piece.color != color:
                    moves = piece.get_moves(board)
                    if king and king.position in moves:
                        attackers.append(piece)

        if not king:
            print("🚨 ERREUR: Le Roi n'a pas été trouvé sur l'échiquier !")
            return False

        if not attackers:
            print("🚨 ERREUR: Aucun attaquant trouvé alors que le Roi est en échec !")
            return False

        # 1️⃣ Le Roi peut-il s'échapper ?
        for move in king.get_moves(board):
            temp_piece = board.get_piece(move)  # Sauvegarde
            board.move_piece(king, move)  # Teste le mouvement
            if not ChessRules.is_in_check(board, color):  # Vérifie si le Roi est en sécurité
                board.move_piece(king, king.position)  # Restaure la position du Roi
                board.grid[move[1]][move[0]] = temp_piece  # Restaure la pièce mangée
                return False  # Pas échec et mat
            board.move_piece(king, king.position)
            board.grid[move[1]][move[0]] = temp_piece

        return True  # Si aucun mouvement ne sort le Roi de l'échec → échec et mat
