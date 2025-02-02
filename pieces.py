import pygame
import os
print(os.listdir("assets/"))
base_path = os.path.dirname(os.path.abspath(__file__))  

class Piece :
    def __init__(self, color, position, image_path):
        full_path = os.path.join(base_path, image_path)

        self.color = color # BLACK / WHITE
        self.position = position # (x,y)
        try:
            self.image = pygame.image.load(full_path)  # Load the image
            self.image = pygame.transform.scale(self.image, (60, 60)) # adjust the size
        except pygame.error as e:
            print(f"❌ Erreur lors du chargement de l'image {image_path}: {e}")
        self.first_move = True # for pawn and castle

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

    def get_moves(self, board):
        moves = []
        x, y = self.position
        direction = -1 if self.color == "white" else 1 # WHITE goes up, BLACK goes down

        # Move forward one square
        if 0 <= y + direction < 8 and board.grid[y + direction][x] is None: # if we are not moving over the board, and there is no piece there
            moves.append((x, y + direction))
            if self.first_move and 0 <= y + 2 * direction < 8 and board.grid[y + 2 * direction][x] is None:
                moves.append((x, y + 2 * direction))

        # Diagonal Eating
        for dx in [-1, 1]:
            if 0 <= x + dx < 8 and 0 <= y + direction < 8:
                target = board.grid[y + direction][x + dx]
                if target and target.color != self.color: # if there is an opponent piece in the front immediate diagonal cases 
                    moves.append((x + dx, y + direction))
        return moves

class Rook(Piece):
    def __init__(self, color, position, image_path):
        super().__init__(color, position, image_path)

    def get_moves(self, board):
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
                    # Case 3: Own piece in the new position, IMPOSSIBLE MOVE
                    else:
                        break
                else: # we've gone over the edge
                    break
        return moves
    
class Knight(Piece):
    def __init__(self, color, position, image_path):
        super().__init__(color, position, image_path)

    def get_moves(self, board):
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

    def get_moves(self, board):
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
                    # Case 3: Own piece in the new position, IMPOSSIBLE MOVE
                    else:
                        break
                else: # we've gone over the edge
                    break
        return moves
    
class Queen(Piece):
    def __init__(self, color, position, image_path):
        super().__init__(color, position, image_path)

    def get_moves(self, board):
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
                    # Case 3: Own piece in the new position, IMPOSSIBLE MOVE
                    else:
                        break
                else: # we've gone over the edge
                    break
        return moves
    
class King(Piece):
    def __init__(self, color, position, image_path):
        super().__init__(color, position, image_path)

    def get_moves(self, board):
        moves = []
        x, y = self.position
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)] # all directions
        
        for dx, dy in directions:
            nx, ny = x, y

            nx += dx
            ny += dy

            if 0 <= nx < 8 and 0 <= ny < 8:
                # Case 1: no piece in the new position
                if board.grid[ny][nx] is None:
                    moves.append((nx, ny))
                # Case 2: Opponent piece is in the new position
                elif board.grid[ny][nx].color != self.color:
                    moves.append((nx, ny))
        return moves
    