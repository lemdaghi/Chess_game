import pygame
from pieces import Pawn, Rook, Bishop, Knight, Queen, King  
import copy  

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]  
        self.selected_piece = None 
        self.valid_moves = [] 
        self.last_move = None # save last move
        self.position_history = {}

        # Pawns
        for col in range(8):
            self.grid[6][col] = Pawn("white", (col, 6), f"assets/pawn_white.png")
            self.grid[1][col] = Pawn("black", (col, 1), f"assets/pawn_black.png")

        # Rooks
        self.grid[7][0] = Rook("white", (0, 7), f"assets/rook_white.png")
        self.grid[7][7] = Rook("white", (7, 7), f"assets/rook_white.png")
        self.grid[0][7] = Rook("black", (7, 0), f"assets/rook_black.png")
        self.grid[0][0] = Rook("black", (0, 0), f"assets/rook_black.png")

        # Knights
        self.grid[7][6] = Knight("white", (6, 7), f"assets/knight_white.png")
        self.grid[7][1] = Knight("white", (1, 7), f"assets/knight_white.png")
        self.grid[0][1] = Knight("black", (1, 0), f"assets/knight_black.png")
        self.grid[0][6] = Knight("black", (6, 0), f"assets/knight_black.png")

        # Bishops
        self.grid[7][5] = Bishop("white", (5, 7), f"assets/bishop_white.png")
        self.grid[7][2] = Bishop("white", (2, 7), f"assets/bishop_white.png")
        self.grid[0][2] = Bishop("black", (2, 0), f"assets/bishop_black.png")
        self.grid[0][5] = Bishop("black", (5, 0), f"assets/bishop_black.png")

        # Queens
        self.grid[7][3] = Queen("white", (3, 7), f"assets/queen_white.png")
        self.grid[0][3] = Queen("black", (3, 0), f"assets/queen_black.png")

        # Kings
        self.grid[7][4] = King("white", (4, 7), f"assets/king_white.png")
        self.grid[0][4] = King("black", (4, 0), f"assets/king_black.png")

    def draw(self, screen):
        SQUARE_SIZE = 75
        WHITE = (238, 238, 210)
        BLACK = (118, 150, 86)

        for row in range(8):
            for col in range(8):
                color = WHITE if (row + col) % 2 == 0 else BLACK
                pygame.draw.rect(screen, color, 
                                (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

        for row in range(8):
             for col in range(8):
                piece = self.grid[row][col]
                if piece:
                    piece.draw(screen)

    def get_piece(self, position):
        x, y = position
        return self.grid[y][x]

    def move_piece(self, piece, new_position):
        from chess_rules import ChessRules  

        old_position = piece.position
        x, y = old_position
        new_x, new_y = new_position

        captured_piece = self.grid[new_y][new_x]  

        if captured_piece and isinstance(captured_piece, King) and piece.color != captured_piece.color:
            print(f"🚨 Mouvement illégal de {piece.color} {piece.__class__.__name__}: Un Roi ne peut pas être capturé !")
            return False

        # ✅ Vérification du Roque
        if isinstance(piece, King) and abs(new_x - x) == 2:
            print("♔ King Castle Verification...")

            # Vérifier que le Roi n'est pas en échec avant le Roque
            if ChessRules.is_in_check(self, piece.color):
                print("🚫 Roque interdit : le Roi est en échec !")
                return False  

            # Déterminer le type de Roque et la position de la Tour
            if new_x == 6:  # Petit Roque (côté Roi)
                print("petit roque")
                rook_x, rook_new_x = 7, 5
                path = [(5, y), (6, y)]  # Cases traversées par le Roi
            elif new_x == 2:  # Grand Roque (côté Dame)
                print("grand roque")
                rook_x, rook_new_x = 0, 3
                path = [(3, y), (2, y)]  # Cases traversées par le Roi
            else:
                return False  # Sécurité : ce n'est pas un Roque

            # Vérifier que les cases du chemin sont vides
            if any(self.get_piece(pos) is not None for pos in path):
                print("🚫 Roque interdit : une pièce bloque le chemin !")
                return False  

            # **Vérifier si le Roi traverse une case attaquée**
            for pos in path:
                if ChessRules.is_in_check(self, piece.color, pos):
                    print(f"🚫 Roque interdit : le Roi passe par une case attaquée {pos} !")
                    return False  

            # Vérifier que la Tour est bien en place et n'a pas bougé
            rook = self.grid[y][rook_x]
            if not rook or not isinstance(rook, Rook) or not rook.first_move:
                print("🚫 Roque interdit : la Tour a déjà bougé ou est absente !")
                return False

            # ✅ Déplacer d'abord le Roi
            self.grid[y][x] = None  
            self.grid[y][new_x] = piece  
            piece.position = (new_x, y)  

            # ✅ Ensuite déplacer la Tour
            self.grid[y][rook_x] = None  
            self.grid[y][rook_new_x] = rook  
            rook.position = (rook_new_x, y)  

            # Marquer que le Roi et la Tour ont bougé
            piece.first_move = False  
            rook.first_move = False  

            print("✅ Roque effectué avec succès !")
            return True  
        
        # ✅ Vérifier si un Pion atteint la dernière rangée pour la promotion
        if isinstance(piece, Pawn) and (new_y == 0 or new_y == 7):
            print(f"♟️ {piece.color} Pawn atteint la dernière ligne ({new_y}) : Promotion requise !")

            # 👉 Choix automatique en Dame (pour l'instant)
            promoted_piece = self.promote_pawn(piece)
            self.grid[new_y][new_x] = promoted_piece  # Remplace le Pion par la Reine
            piece = promoted_piece  # ✅ Mise à jour de la référence mémoire pour éviter tout bug
            print(f"🎉 {piece.color} Pawn promu en {piece.symbol} !")
        
        # ✅ Capture "En Passant"
        if isinstance(piece, Pawn) and self.last_move:
            last_piece, (old_x, old_y), (last_new_x, last_new_y) = self.last_move

            if isinstance(last_piece, Pawn) and last_piece.color != piece.color:
                if abs(old_y - last_new_y) == 2 and old_x == last_new_x:  # Double-pas adverse
                    direction = (1 if piece.color == "white" else -1)
                    if (new_x, new_y) == (last_new_x, y - direction) and y == last_new_y:
                        print(f"♟️ Capture 'En Passant' de {last_piece.symbol} en {last_new_x}, {last_new_y}")
                        self.grid[last_new_y][last_new_x] = None  # ✅ SUPPRIME le pion adverse capturé
                        captured_piece = last_piece  # ✅ Marque la pièce comme capturée pour l'historique

        # ✅ Vérification classique du mouvement normal (hors Roque)
        self.grid[y][x] = None  # On enlève la pièce de sa position actuelle
        self.grid[new_y][new_x] = piece  # On la place sur la nouvelle case
        piece.position = (new_x, new_y)  # Mise à jour temporaire de la position

        # ✅ Vérification : Opposition des Rois
        if isinstance(piece, King) and self.is_king_opposition(piece):
            print(f"🚫 Mouvement illégal ! {piece.color} King ne peut pas s'opposer directement au Roi adverse !")

            # ✅ Restaurer l'état initial
            self.grid[new_y][new_x] = captured_piece  # Remettre la pièce capturée si besoin
            self.grid[y][x] = piece  # Remettre le Roi à sa position initiale
            piece.position = old_position  # Restauration de la position initiale

            return False  # 🚫 Mouvement interdit car il crée une opposition des Rois

        # ✅ Vérifier si le Roi est en échec après ce mouvement (SAUF si c'est un Roi)
        if not isinstance(piece, King) and ChessRules.is_in_check(self, piece.color):
            print(f"🚫 Mouvement illégal ! {piece.symbol} ({piece.__class__.__name__}) est cloué et ne peut pas bouger !")

            # ✅ Annuler le mouvement (restaurer l'état initial)
            self.grid[new_y][new_x] = captured_piece  # Remet la pièce capturée (si existante)
            self.grid[y][x] = piece  # Remet la pièce à sa position initiale
            piece.position = old_position  # Restauration de la position initiale
            
            return False  # 🚫 Mouvement interdit car il expose le Roi

        piece.first_move = False  

        # ✅ Sauvegarde le dernier coup joué
        self.last_move = (piece, old_position, new_position)

        return True

    def is_king_opposition(self, king):
        """Vérifie si un autre Roi est adjacent à la position actuelle du Roi."""
        x, y = king.position
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                piece = self.get_piece((nx, ny))
                if piece and isinstance(piece, King) and piece.color != king.color:
                    print(f"🚫 Mouvement illégal : Opposition des Rois détectée en {king.position} !")
                    return True  # ✅ Il y a un autre Roi adjacent → Opposition illégale

        return False  # ✅ Aucun Roi adjacent → Mouvement possible
    
    def promote_pawn(self, piece):
        """Permet au joueur de choisir en quoi promouvoir le Pion."""
        choices = {
            "Q": Queen(piece.color, piece.position, f"assets/queen_{piece.color}.png"),
            "R": Rook(piece.color, piece.position, f"assets/rook_{piece.color}.png"),
            "B": Bishop(piece.color, piece.position, f"assets/bishop_{piece.color}.png"),
            "N": Knight(piece.color, piece.position, f"assets/knight_{piece.color}.png"),
        }
        
        while True:
            choice = input("♟️ Promotion ! Choisissez (Q)Queen, (R)Rook, (B)Bishop, (N)Knight: ").upper()
            if choice in choices:
                return choices[choice]
            print("❌ Choix invalide, réessayez.")

    def check_legal_move(self, piece, new_position):
        """Retourne True si le mouvement est légal, sinon False."""
        from chess_rules import ChessRules  

        old_position = piece.position
        x, y = old_position
        new_x, new_y = new_position
        captured_piece = self.grid[new_y][new_x]  # ✅ On sauvegarde la pièce éventuellement capturée

        # ✅ Simuler le déplacement
        self.grid[y][x] = None  
        self.grid[new_y][new_x] = piece  
        piece.position = (new_x, new_y)  

        # 🔍 Vérification Opposition des Rois
        if isinstance(piece, King) and self.is_king_opposition(piece):
            print(f"🚫 Mouvement illégal ! {piece.color} King ne peut pas s'opposer directement au Roi adverse !")

            # ✅ Restaurer l'état initial
            self.grid[new_y][new_x] = captured_piece
            self.grid[y][x] = piece  
            piece.position = old_position  

            return False  # 🚫 Mouvement interdit !

        # 🔍 Vérification d'un échec sur son propre roi
        if ChessRules.is_in_check(self, piece.color):

            # ✅ Restauration de l'état
            self.grid[new_y][new_x] = captured_piece  
            self.grid[y][x] = piece  
            piece.position = old_position  

            return False  # 🚫 Mouvement interdit !

        # ✅ Rétablir la position après la simulation
        self.grid[new_y][new_x] = captured_piece  
        self.grid[y][x] = piece  
        piece.position = old_position  

        return True  # ✅ Mouvement autorisé !

    def record_position(self):
        """Enregistre la position actuelle de l'échiquier."""
        position_key = tuple((piece.__class__.__name__, piece.color, piece.position) for row in self.grid for piece in row if piece)
        if position_key in self.position_history:
            self.position_history[position_key] += 1
        else:
            self.position_history[position_key] = 1

    def is_triple_repetition(self):
        """Retourne True si la même position est apparue trois fois."""
        for count in self.position_history.values():
            if count >= 3:
                print("⚖️ Match nul par Triple Répétition !")
                return True
        return False

    def pos_to_chess_notation(self, position):
        """Convert position (x, y) to ('a1', 'h8')."""
        files = "abcdefgh"
        return f"{files[position[0]]}{8 - position[1]}"  # Ex: (4,6) → "e2"
    
    def copy(self):
        """Retourne une copie du plateau sans copier les images pygame."""
        new_board = Board()
        for y in range(8):
            for x in range(8):
                piece = self.grid[y][x]
                if piece:
                    # ✅ Crée une nouvelle instance de la pièce avec son `image_path`
                    new_piece = piece.__class__(piece.color, piece.position, piece.image_path)
                    new_piece.first_move = piece.first_move  # ✅ Garde l'info du premier mouvement
                    new_board.grid[y][x] = new_piece
        return new_board
