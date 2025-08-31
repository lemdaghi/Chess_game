from board import Board
from pieces import Pawn, Rook, Knight, Bishop, Queen, King

def img_path(piece_cls, color):
    name = piece_cls.__name__.lower()
    return f"assets/{name}_{color}.png"  # ex: assets/rook_white.png

def empty_board():
    board = Board()
    board.grid = [[None for _ in range(8)] for _ in range(8)]
    board.last_move = None
    return board

def place(board, piece_cls, color, x, y):
    piece = piece_cls(color, (x, y), img_path(piece_cls, color))
    board.grid[y][x] = piece
    return piece

def moves_set(piece, board):
    return set(piece.get_moves(board))

# Aliases
P = Pawn; R = Rook; N = Knight; B = Bishop; Q = Queen; K = King
