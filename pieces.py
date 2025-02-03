import pygame
import os
print(os.listdir("assets/"))
base_path = os.path.dirname(os.path.abspath(__file__))  

class Piece :
    def __init__(self, color, position, image_path):
        self.color = color  
        self.position = position  
        self.image_path = image_path  # ✅ Sauvegarde du chemin de l’image
        self.first_move = True  

        # Chargement de l'image
        try:
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (60, 60))
        except pygame.error as e:
            print(f"❌ Erreur lors du chargement de l'image {image_path}: {e}")

        # Symboles des pièces
        piece_symbols = {
            "Pawn": "♙" if color == "white" else "♟",
            "Rook": "♖" if color == "white" else "♜",
            "Knight": "♘" if color == "white" else "♞",
            "Bishop": "♗" if color == "white" else "♝",
            "Queen": "♕" if color == "white" else "♛",
            "King": "♔" if color == "white" else "♚",
        }
        self.symbol = piece_symbols[self.__class__.__name__]

    def get_moves(self, board):
        ''' Return a list of possible moves '''
          # To overide in sub-classes
        return []
    
    def move(self, new_position):
        ''' Move the piece to the new position '''
        self.position = new_position
        self.first_move = False
    
    def draw(self, screen):
        ''' Draw the piece on the board '''
        x, y = self.position
        screen.blit(self.image, (x * 75 + 7, y * 75 + 7))

class Pawn(Piece):
    def __init(self, color, position, image_path):
        super().__init__(color, position, image_path)

    def get_moves(self, board, simulate=False):
        moves = []
        
        x, y = self.position
        direction = -1 if self.color == "white" else 1 # WHITE goes up, BLACK goes down

        ## Moving
        # Move forward one square
        if 0 <= y + direction < 8 and board.grid[y + direction][x] is None: # if we are not moving over the board, and there is no piece there
            moves.append((x, y + direction))
            # Move forward two squares (from the initial line)
            if self.first_move and 0 <= y + 2 * direction < 8 and board.grid[y + 2 * direction][x] is None:
                moves.append((x, y + 2 * direction))

        ## Eating
        # Diagonal Eating
        for dx in [-1, 1]:
            if 0 <= x + dx < 8 and 0 <= y + direction < 8:
                target = board.grid[y + direction][x + dx]
                if target and target.color != self.color: # if there is an opponent piece in the front immediate diagonal cases 
                    moves.append((x + dx, y + direction))

        # En Passant
        if board.last_move:  # Vérifie s'il y a eu un dernier mouvement
            last_piece, (old_x, old_y), (new_x, new_y) = board.last_move

            # Vérifie si le dernier coup était un double-pas d'un pion adverse
            if isinstance(last_piece, Pawn) and last_piece.color != self.color:
                if abs(old_y - new_y) == 2 and new_y == y and abs(new_x - x) == 1:  # ✅ Correction de la condition
                    moves.append((new_x, y + direction))  # ✅ En passant se fait sur la même colonne

        return moves

class Rook(Piece):
    def __init__(self, color, position, image_path):
        super().__init__(color, position, image_path)

    def get_moves(self, board, simulate=False):


        moves = []
        x, y = self.position

        
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] # UP, DOWN, LEFT, RIGHT
        
        for dx, dy in directions:
            nx, ny = x, y
            while(1):
                nx += dx
                ny += dy

                if 0 <= nx < 8 and 0 <= ny < 8:
                    # Case 1: no piece in the new position
                    if board.grid[ny][nx] is None:
                        moves.append((nx, ny))
                    # Case 2: Opponent piece is in the new position
                    elif board.grid[ny][nx].color != self.color:
                        moves.append((nx, ny))
                        break
                    # Case 3: Own piece in the new position, IMPOSSIBLE MOVE
                    else:
                        break
                else: # we've gone over the edge
                    break
        return moves
    
class Knight(Piece):
    def __init__(self, color, position, image_path):
        super().__init__(color, position, image_path)

    def get_moves(self, board, simulate=False):
        moves = []
        
        x, y = self.position
        directions = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8: # assert we stay on the board
                piece = board.grid[ny][nx]
                if piece is None or piece.color != self.color: 
                    moves.append((nx, ny))

        return moves

    
class Bishop(Piece):
    def __init__(self, color, position, image_path):
        super().__init__(color, position, image_path)

    def get_moves(self, board, simulate=False):

        moves = []
        x, y = self.position
        
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)] # Diagonals
        
        for dx, dy in directions:
            nx, ny = x, y
            while(1):
                nx += dx
                ny += dy

                if 0 <= nx < 8 and 0 <= ny < 8:
                    # Case 1: no piece in the new position
                    if board.grid[ny][nx] is None:
                        moves.append((nx, ny))
                    # Case 2: Opponent piece is in the new position
                    elif board.grid[ny][nx].color != self.color:
                        moves.append((nx, ny))
                        break
                    # Case 3: Own piece in the new position, IMPOSSIBLE MOVE
                    else:
                        break
                else: # we've gone over the edge
                    break
        return moves
    
class Queen(Piece):
    def __init__(self, color, position, image_path):
        super().__init__(color, position, image_path)

    def get_moves(self, board, simulate=False):
        from chess_rules import ChessRules  

        moves = []
        x, y = self.position
    
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)] # all directions
        
        for dx, dy in directions:
            nx, ny = x, y
            while(1):
                nx += dx
                ny += dy

                if 0 <= nx < 8 and 0 <= ny < 8:
                    # Case 1: no piece in the new position
                    if board.grid[ny][nx] is None:
                        moves.append((nx, ny))
                    # Case 2: Opponent piece is in the new position
                    elif board.grid[ny][nx].color != self.color:
                        moves.append((nx, ny))
                        break
                    # Case 3: Own piece in the new position, IMPOSSIBLE MOVE
                    else:
                        break
                else: # we've gone over the edge
                    break
        return moves
    
class King(Piece):
    def __init__(self, color, position, image_path):
        super().__init__(color, position, image_path)

    def get_moves(self, board, simulate = True):
        """Retourne les mouvements possibles du Roi en excluant les cases attaquées."""
        moves = []
        
    
        old_position = self.position
        x, y = old_position
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]  # Toutes les directions

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                target_piece = board.get_piece((nx, ny))  # ✅ On sauvegarde la pièce existante

                if target_piece is None or target_piece.color != self.color:
                    # ✅ Déplacement temporaire du Roi
                    board.grid[y][x] = None  # Retire le Roi temporairement
                    board.grid[ny][nx] = self  # Met le Roi sur la nouvelle case
                    self.position = (nx, ny)  # Met à jour la position temporaire

                    from chess_rules import ChessRules  # ✅ Import pour éviter les dépendances circulaires
                    if not ChessRules.is_in_check(board, self.color):  
                        moves.append((nx, ny))  # ✅ Ajoute la case si elle est sûre

                    # ✅ Restauration complète de l'état initial
                    board.grid[ny][nx] = target_piece  # Remet la pièce d'origine si elle existait
                    board.grid[y][x] = self  # Remet le Roi à sa place initiale
                    self.position = old_position  # ✅ On restaure la position du Roi

        # Verify Castle
        if self.first_move and not ChessRules.is_in_check(board, self.color):
            # Grand roque
            if all(board.get_piece((i, y)) is None for i in range(1, 4)): # aucune piece entre le roi et la tour
                rook = board.get_piece((0, y)) # Queen side / left side
                if rook and isinstance(rook, Rook) and rook.first_move:
                    if not any(ChessRules.is_in_check(board, self.color, (i, y)) for i in range(2, 5)):
                        moves.append((2, y))

            # Petit roque
            if all(board.get_piece((i, y)) is None for i in range(5, 7)): # aucune piece entre le roi et la tour
                rook = board.get_piece((7, y)) # Queen side / left side
                if rook and isinstance(rook, Rook) and rook.first_move:
                    if not any(ChessRules.is_in_check(board, self.color) for i in range(5, 7)):
                        moves.append((6, y))
        return moves