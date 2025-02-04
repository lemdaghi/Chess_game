class ChessRules:

    @staticmethod
    def is_in_check(board, color, position=None, ignore_castling=False):
        """Retourne True si le Roi de 'color' est en échec, sauf si on ignore la vérification pour le Roque."""
        king_pos = None
        
        if position:
            king_pos = position
        else:
            for row in board.grid:
                for piece in row:
                    if piece and piece.__class__.__name__ == "King" and piece.color == color:
                        king_pos = piece.position
                        break

        if not king_pos:
            print('No King')
            return False
          
        x, y = king_pos

        # ✅ Simulation temporaire en enlevant la pièce à cet endroit
        temp_piece = board.get_piece(king_pos)
        board.grid[y][x] = None 
        
        # Vérifier toutes les pièces adverses
        in_check = False
        for row in board.grid:
            for piece in row:
                if piece and piece.color != color and piece.__class__.__name__ != "King":
                    # ✅ Vérification spéciale pour les Pions
                    if piece.__class__.__name__ == "Pawn":
                        direction = -1 if piece.color == "white" else 1  # Blancs montent, Noirs descendent
                        for dx in [-1, 1]:  # Attaque en diagonale
                            px, py = piece.position
                            if (px + dx, py + direction) == (x, y):  # Le Roi est sur une case attaquée
                                in_check = True
                                break
                    elif king_pos in piece.get_moves(board, simulate=True):
                        in_check = True
                        break  
                    
        # ✅ Restauration de la pièce d'origine
        board.grid[y][x] = temp_piece
        return in_check  

    @staticmethod
    def is_checkmate(board, color):
        """Retourne True si le joueur 'color' est échec et mat."""
        if not ChessRules.is_in_check(board, color):
            return False  # Pas en échec, donc pas de mat.

        king = None
        for row in board.grid:
            for piece in row:
                if piece and piece.__class__.__name__ == "King" and piece.color == color:
                    king = piece

        if king is None:
            print("🚨 ERREUR: Impossible de trouver le Roi !")
            return False  

        print(f"⚠️ {color} King est en échec")
        # 1️⃣ Vérifier si le Roi peut s’échapper
        original_position = king.position  # ✅ Sauvegarde la position initiale du Roi
        for move in king.get_moves(board):  # ✅ Teste chaque déplacement possible

            target_piece = board.get_piece(move)  # ✅ On sauvegarde ce qu'il y a à la destination
            board.grid[original_position[1]][original_position[0]] = None  # ✅ On enlève le Roi temporairement
            board.grid[move[1]][move[0]] = king  # ✅ On place le Roi à la nouvelle position
            king.position = move  # ✅ On met à jour la position du Roi

            print(f"Testing move: King moves to {move}")

            if not ChessRules.is_in_check(board, color):  
                print(f"King escapes check by moving to {move}")
                # ✅ Si le Roi peut se déplacer sans être en échec, on restaure l'état et on retourne False
                board.grid[move[1]][move[0]] = target_piece  # ✅ On remet la pièce capturée si besoin
                board.grid[original_position[1]][original_position[0]] = king  # ✅ On remet le Roi à sa position
                king.position = original_position  # ✅ On rétablit la vraie position du Roi
                return False  # ✅ Ce n'est PAS un échec et mat

            # ✅ Restauration de l’état initial après chaque test
            board.grid[move[1]][move[0]] = target_piece  # ✅ On remet la pièce mangée (si existante)
            board.grid[original_position[1]][original_position[0]] = king  # ✅ On remet le Roi à sa position
            king.position = original_position  # ✅ On restaure la vraie position du Roi

        print(f"{color.capitalize()} King is checked and has no escape!")

        # 2️⃣ Vérifier si une autre pièce peut intercepter l’attaque ou capturer l’attaquant
        attackers = []
        for row in board.grid:
            for piece in row:
                if piece and piece.color != color:
                    if king.position in piece.get_moves(board, simulate=True):  
                        attackers.append(piece)

        if len(attackers) > 1:
            return True  # ✅ Si plusieurs attaquants menacent le Roi, il n'y a aucun moyen de se défendre → ÉCHEC ET MAT.

        attacker = attackers[0]  # ✅ S'il n'y a qu'un seul attaquant, on teste si on peut le capturer ou le bloquer

        # 3️⃣ Vérifier si une pièce alliée peut capturer l’attaquant
        for row in board.grid:
            for piece in row:
                if piece and piece.color == color:
                    if attacker.position in piece.get_moves(board, simulate=True):  
                        return False  # ✅ Si une pièce peut capturer l'attaquant, ce n'est PAS un mat

        # 4️⃣ Vérifier si on peut interposer une pièce entre l'attaquant et le Roi
        if attacker.__class__.__name__ != "Knight":  # ✅ Les Cavaliers ne peuvent pas être bloqués
            print(f"attacker is {attacker.__class__.__name__}")
            x1, y1 = king.position
            x2, y2 = attacker.position
            path = []  

            dx = (x2 - x1) // max(1, abs(x2 - x1))  
            dy = (y2 - y1) // max(1, abs(y2 - y1))  

            nx, ny = x1 + dx, y1 + dy
            while (nx, ny) != (x2, y2):
                path.append((nx, ny))
                nx += dx
                ny += dy

            for row in board.grid:
                for piece in row:
                    if piece and piece.color == color:
                        for move in piece.get_moves(board, simulate=True):  
                            if move in path:
                                return False  # ✅ Une pièce peut bloquer l'attaque

        return True  # ✅ Si rien ne peut sauver le Roi, alors ÉCHEC ET MAT.

    @staticmethod
    def is_stalemate(board, color):
        """Vérifie si le joueur `color` est en situation de PAT."""
        if ChessRules.is_in_check(board, color):
            return False  # ✅ S'il est en échec, ce n'est pas un PAT

        # 🔎 Parcourir toutes les pièces du joueur
        for row in board.grid:
            for piece in row:
                if piece and piece.color == color:
                    valid_moves = piece.get_moves(board)  # Récupérer les mouvements légaux
                    
                    for move in valid_moves[:]:  # ✅ On utilise une copie pour éviter les modifications directes
                        if board.check_legal_move(piece, move):  
                            return False  # ✅ Il y a encore au moins un coup légal → Pas de PAT
                    
        print("⚖️ Match nul par PAT ! Aucun coup légal possible.")
        return True  # ✅ Aucun coup légal → C'est un PAT !