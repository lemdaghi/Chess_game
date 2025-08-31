import unittest
from unittest.mock import patch
from .utils import empty_board, place, moves_set, K, R

class TestKing(unittest.TestCase):

    def setUp(self):
        """Creates a fresh game state before each test."""
        self.board = empty_board()


    def test_king_opposition(self):
        """Test that kings cannot move next to each other."""
        board = self.board
        board.grid = [[None for _ in range(8)] for _ in range(8)]

        white = place(board, K, "white", 4, 4)  # e4
        black = place(board, K, "black", 6, 4)  # g4 (adjacent squares around f4)
        self.assertFalse(board.check_legal_move(white, (5, 4)))  # f4 should be illegal

        board.grid = [[None for _ in range(8)] for _ in range(8)]
        white = place(board, K, "white", 4, 7)  # e1
        black = place(board, K, "black", 4, 5)  # e3
        self.assertFalse(board.check_legal_move(white, (4, 6)))  # e2 should be illegal

    
    def test_king_one_square_moves_inside_board(self):
        king = place(self.board, K, "white", 4, 4)  # e4
        with patch("chess_rules.ChessRules.is_in_check", return_value=False):
            moves = moves_set(king, self.board)
        expected = {
            (3,3),(4,3),(5,3),
            (3,4),      (5,4),
            (3,5),(4,5),(5,5)
        }
        self.assertTrue(expected.issubset(moves))


    def test_king_does_not_include_attacked_square(self):
        king = place(self.board, K, "white", 4, 7)  # e1
        place(self.board, R, "black", 4, 0)  # e8 (rook control all col e)
       
        moves = moves_set(king, self.board)
        self.assertNotIn((4, 6), moves)  # e2 (4,6)
        

# Run the tests
if __name__ == '__main__':
    unittest.main()
