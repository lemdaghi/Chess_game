import unittest
from unittest.mock import patch
from board import Board
from game import Game
from chess_rules import ChessRules
from pieces import Pawn, Rook, Knight, Bishop, Queen, King

class TestBoardSetup(unittest.TestCase):

    def setUp(self):
        """Creates a fresh game state before each test."""
        self.board = Board()
        self.game = Game()
    
    def test_grid_dimensions(self):
        self.assertEqual(len(self.board.grid), 8)
        self.assertTrue(all(len(row) == 8 for row in self.board.grid))

    def test_selected_defaults(self):
        self.assertIsNone(self.board.selected_piece)
        self.assertIsNone(self.board.last_move)
        self.assertIsInstance(self.board.position_history, dict)
        self.assertEqual(self.board.valid_moves, [])

    def test_initial_piece_placement(self):
        """Test that pieces are in their correct starting positions."""
        # Check pawns
        for row in range(8):
            self.assertIsInstance(self.board.get_piece((row, 1)), Pawn)
            self.assertEqual(self.board.get_piece((row, 1)).color, "black")
            self.assertIsInstance(self.board.get_piece((row, 1)), Pawn)
            self.assertEqual(self.board.get_piece((row, 1)).color, "white")
        # Check rooks
        self.assertIsInstance(self.board.get_piece((0, 0)), Rook)  # a8
        self.assertEqual(self.board.get_piece((0, 0)).color, "black")
        self.assertIsInstance(self.board.get_piece((7, 0)), Rook)  # h8
        self.assertEqual(self.board.get_piece((7, 0)).color, "black")
        self.assertIsInstance(self.board.get_piece((0, 7)), Rook)  # a1
        self.assertEqual(self.board.get_piece((0, 7)).color, "white")
        self.assertIsInstance(self.board.get_piece((7, 7)), Rook)  # h1
        self.assertEqual(self.board.get_piece((7, 7)).color, "white")
        # Check knights
        self.assertIsInstance(self.board.get_piece((1, 0)), Knight)  # b8
        self.assertEqual(self.board.get_piece((1, 0)).color, "black")
        self.assertIsInstance(self.board.get_piece((6, 0)), Knight)  # g8
        self.assertEqual(self.board.get_piece((6, 0)).color, "black")
        self.assertIsInstance(self.board.get_piece((1, 7)), Knight)  # b1
        self.assertEqual(self.board.get_piece((1, 7)).color, "white")
        self.assertIsInstance(self.board.get_piece((6, 7)), Knight)  # g1
        self.assertEqual(self.board.get_piece((6, 7)).color, "white")
        # Check bishops
        self.assertIsInstance(self.board.get_piece((2, 0)), Bishop)  # c8
        self.assertEqual(self.board.get_piece((2, 0)).color, "black")
        self.assertIsInstance(self.board.get_piece((5, 0)), Bishop)  # f8
        self.assertEqual(self.board.get_piece((5, 0)).color, "black")
        self.assertIsInstance(self.board.get_piece((2, 7)), Bishop)  # c1
        self.assertEqual(self.board.get_piece((2, 7)).color, "white")
        self.assertIsInstance(self.board.get_piece((5, 7)), Bishop)  # f1
        self.assertEqual(self.board.get_piece((5, 7)).color, "white")
        # Check queens
        self.assertIsInstance(self.board.get_piece((3, 0)), Queen)  # d8
        self.assertEqual(self.board.get_piece((3, 0)).color, "black")
        self.assertIsInstance(self.board.get_piece((3, 7)), Queen)  # d1
        self.assertEqual(self.board.get_piece((3, 7)).color, "white")
        # Check kings
        self.assertIsInstance(self.board.get_piece((4, 0)), King)  # e8
        self.assertEqual(self.board.get_piece((4, 0)).color, "black")
        self.assertIsInstance(self.board.get_piece((4, 7)), King)  # e1
        self.assertEqual(self.board.get_piece((4, 7)).color, "white")

    def test_piece_position_fields_match_grid_coordinates(self):
        # Each piece must have piece.position == (x,y) it's case coordinates
        for y in range(8):
            for x in range(8):
                piece = self.board.grid[y][x]
                if piece:
                    self.assertEqual(
                        piece.position, (x, y),
                        f"piece.position does not match {piece.__class__.__name__} at {(x,y)}"
                    )

    def test_get_piece(self):
        """Test that a piece is correctly retrieved from the board."""
        piece = self.board.get_piece((0, 0))  # a8
        self.assertIsInstance(piece, Rook)
        self.assertEqual(piece.color, "black")
        piece2 = self.board.get_piece((4, 6))  # e2
        self.assertIsInstance(piece2, Pawn)
        self.assertEqual(piece2.color, "white")

    def test_get_piece_out_of_bounds_raises(self):
        with self.assertRaises(IndexError):
            _ = self.board.get_piece((8, 0))
        with self.assertRaises(IndexError):
            _ = self.board.get_piece((0, 8))
        with self.assertRaises(IndexError):
            _ = self.board.get_piece((-1, 0))

    def test_pos_to_chess_notation(self):
        """Ensure board positions convert correctly."""
        self.assertEqual(self.board.pos_to_chess_notation((0, 0)), "a8")
        self.assertEqual(self.board.pos_to_chess_notation((7, 0)), "h8")
        self.assertEqual(self.board.pos_to_chess_notation((0, 7)), "a1")
        self.assertEqual(self.board.pos_to_chess_notation((7, 7)), "h1")
        self.assertEqual(self.board.pos_to_chess_notation((4, 6)), "e2")
        self.assertEqual(self.board.pos_to_chess_notation((3, 0)), "d8")

    def test_copy_board(self):
        """Ensure the board is correctly copied."""
        new_board = self.board.copy()
        self.assertIsNot(self.board, new_board)  # Different memory location
        self.assertEqual(len(new_board.grid), 8)

        # Objects in the grid should be different instances but same types
        orig_pawn = self.board.get_piece((0, 6))
        copy_pawn = new_board.get_piece((0, 6))
        self.assertIsInstance(copy_pawn, Pawn)
        self.assertIsNot(orig_pawn, copy_pawn)

        # Modifying the original should not affect the copy
        self.board.grid[6][0] = None
        self.assertIsNotNone(copy_pawn)
        self.assertIsInstance(new_board.get_piece((0, 6)), Pawn)

    def test_modifying_copy_does_not_affect_original(self):
        new_board = self.board.copy()

        # Remove a piece in the copy board should not remove it in the original
        self.assertIsInstance(self.board.get_piece((0, 6)), Pawn)  # a2 original
        self.assertIsInstance(new_board.get_piece((0, 6)), Pawn)   # a2 copy
        new_board.grid[6][0] = None                                # remove pawn in a2 (copy)
        self.assertIsNotNone(self.board.get_piece((0, 6)))         # original unchanged
        self.assertIsNone(new_board.get_piece((0, 6)))             # removed in copy

    def test_record_position(self):
        """Test that positions are recorded correctly."""
        self.board.record_position()
        self.board.record_position()
        self.board.record_position()
        self.assertTrue(self.board.is_triple_repetition())

# Run the tests
if __name__ == '__main__':
    unittest.main()
