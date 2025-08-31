import unittest
from unittest.mock import patch
from .utils import empty_board, place, moves_set, P


class TestPawn(unittest.TestCase):

    def setUp(self):
        """Creates a fresh game state before each test."""
        self.board = empty_board()

    
    def test_white_pawn_forward_one_and_two(self):
        pawn = place(self.board, P, "white", 0, 6)  # a2
        moves = moves_set(pawn, self.board)
        self.assertIn((0, 5), moves)  # a3
        self.assertIn((0, 4), moves)  # a4 (double step)


    def test_black_pawn_forward_one_and_two(self):
        pawn = place(self.board, P, "black", 7, 1)  # h7
        moves = moves_set(pawn, self.board)
        self.assertIn((7, 2), moves)  # h6
        self.assertIn((7, 3), moves)  # h5 (double step)


    def test_pawn_blocked_by_piece_ahead(self):
        """Cannot move forward if the square immediately in front is occupied."""
        pawn = place(self.board, P, "white", 4, 6)  # e2
        place(self.board, P, "white", 4, 5)  # e3 ally
        moves = moves_set(pawn, self.board)
        self.assertNotIn((4, 5), moves)
        self.assertNotIn((4, 4), moves)

    
    def test_pawn_blocked_by_piece_two_ahead(self):
        """May step one if free; cannot use double step if the second square is occupied."""
        pawn = place(self.board, P, "white", 4, 6)  # e2
        place(self.board, P, "white", 4, 4)  # e4 ally
        moves = moves_set(pawn, self.board)
        self.assertIn((4, 5), moves)
        self.assertNotIn((4, 4), moves)

    
    def test_pawn_diagonal_captures(self):
        pawn = place(self.board, P, "white", 4, 4)  # e4
        place(self.board, P, "black", 3, 3)  # d3
        place(self.board, P, "black", 5, 3)  # f3
        moves = moves_set(pawn, self.board)
        self.assertIn((3, 3), moves)  # e4xd3
        self.assertIn((5, 3), moves)  # e4xf3


    def test_pawn_no_capture_own_piece(self):
        pawn = place(self.board, P, "white", 4, 4)  # e4
        place(self.board, P, "white", 3, 3)  # d3 ally
        place(self.board, P, "white", 5, 3)  # f3 ally
        moves = moves_set(pawn, self.board)
        self.assertNotIn((3, 3), moves)
        self.assertNotIn((5, 3), moves)


    def test_white_pawn_no_double_after_first_move(self):
        board = self.board
        pawn = place(board, P, "white", 4, 6)  # e2

        moves_before = moves_set(pawn, board)
        self.assertIn((4, 4), moves_before)  # e4
        self.assertIn((4, 5), moves_before)  # e3

        with patch("chess_rules.ChessRules.is_in_check", return_value=False):
            ok = board.move_piece(pawn, (4, 5))  # e3
        self.assertTrue(ok)

        moves_after = moves_set(pawn, board)
        self.assertIn((4, 4), moves_after)      # e4 
        self.assertNotIn((4, 3), moves_after)   # e5 not allowed


    def test_black_pawn_no_double_after_first_move(self):
        board = self.board
        pawn = place(board, P, "black", 3, 1)  # d7

        moves_before = moves_set(pawn, board)
        self.assertIn((3, 2), moves_before)  # d6
        self.assertIn((3, 3), moves_before)  # d5

        with patch("chess_rules.ChessRules.is_in_check", return_value=False):
            ok = board.move_piece(pawn, (3, 2))  # d6
        self.assertTrue(ok)

        moves_after = moves_set(pawn, board)
        self.assertIn((3, 3), moves_after)      # d5
        self.assertNotIn((3, 4), moves_after)   # d4 not allowed


# Run the tests
if __name__ == '__main__':
    unittest.main()
