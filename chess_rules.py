class ChessRules:
    # @staticmethod
    # def is_pinned(board, piece):
    #     """Retourne True si la pièce est clouée et ne peut pas bouger librement."""
    #     print(f"Verifying if {piece.color} {piece.__class__.__name__} is pinned")
    #     if piece.__class__.__name__ == "King":  
    #         return False  # ✅ Le Roi ne peut jamais être "cloué"

    #     king = None
    #     for row in board.grid:
    #         for p in row:
    #             if p and p.__class__.__name__ == "King" and p.color == piece.color:
    #                 king = p
    #                 break

    #     if not king:
    #         print(f"🚨 ERREUR: Impossible de trouver le Roi de {piece.color} !")
    #         return False  

    #     x1, y1 = piece.position
    #     x2, y2 = king.position

    #     # ✅ Vérifier si la pièce et le Roi sont alignés (même ligne, colonne ou diagonale)
    #     if x1 == x2 or y1 == y2 or abs(x1 - x2) == abs(y1 - y2):
    #         direction_x = (x2 - x1) // max(1, abs(x2 - x1)) if x1 != x2 else 0
    #         direction_y = (y2 - y1) // max(1, abs(y2 - y1)) if y1 != y2 else 0

    #         # ✅ Vérifier s'il y a exactement UNE pièce entre la pièce testée et le Roi
    #         path = []
    #         nx, ny = x1 + direction_x, y1 + direction_y
    #         while (nx, ny) != (x2, y2):
    #             path.append((nx, ny))
    #             nx += direction_x
    #             ny += direction_y
    #         print("je suis la")
    #         pieces_between = [board.get_piece(pos) for pos in path if board.get_piece(pos)]
    #         if len(pieces_between) != 0:
    #             print(f"il y a pas qu'une seule piece entre {piece.color} {piece.__class__.__name__} et le roi {king.color}")
    #             return False  # ✅ Il y a d'autres pièces entre la pièce et le Roi, donc pas cloué

    #         print(f"il y a exactement une piece entre {piece.color} {piece.__class__.__name__} et le roi {king.color} ")
    #         # ✅ Vérifier si un attaquant est aligné et menace directement le Roi après la pièce
    #         nx, ny = x2 + direction_x, y2 + direction_y
    #         while 0 <= nx < 8 and 0 <= ny < 8:
    #             attacker = board.get_piece((nx, ny))
    #             if attacker and attacker.color != piece.color and attacker.__class__.__name__ in ["Rook", "Bishop", "Queen"]:
    #                 print(f"⚠️ {piece.symbol} ({piece.__class__.__name__}) est cloué par {attacker.symbol} en {attacker.position} !")
    #                 return True  # ✅ La pièce est clouée car un attaquant l'aligne avec le Roi
    #             elif attacker:
    #                 break  # ✅ Une autre pièce bloque la ligne d'attaque

    #             nx += direction_x
    #             ny += direction_y

    #     return False  # ✅ Pas de clouage

    
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
        print(f"🔎 Vérification de l'échec pour {color} en {position if position else king_pos}")

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
                                print(f"⚠️ {color} King est en échec par {piece.symbol} en {piece.position} via attaque en diagonale")
                                in_check = True
                                break
                    elif king_pos in piece.get_moves(board, simulate=True):
                        print(f"⚠️ {color} est en échec en {king_pos} par {piece.color} {piece.__class__.__name__} en {piece.position}")
                        in_check = True
                        break  
                    
        # ✅ Restauration de la pièce d'origine
        board.grid[y][x] = temp_piece
        return in_check  


    # @staticmethod
    # def is_in_check(board, color, position=None):
    #     """Retourne True si le Roi de 'color' est en échec."""
    #     king = None
    #     if position:
    #         x, y = position
    #     else:
    #         for row in board.grid:
    #             for piece in row:
    #                 if piece and piece.__class__.__name__ == "King" and piece.color == color:
    #                     king = piece
    #                     break
                
    #     if not king:
    #         return False  
    #     print(f"{king.color} King is in {king.position}")
    #     for row in board.grid:
    #         for piece in row:
    #             if piece and piece.color != color and piece.__class__.__name__ != "King":
    #                 if king.position in piece.get_moves(board, simulate=True):
    #                     print(f"{king.color} King is checked by {piece.color} {piece.__class__.__name__} in {piece.position}")
    #                     return True  

    #     return False  

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

