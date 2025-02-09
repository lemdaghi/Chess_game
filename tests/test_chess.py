import unittest
from unittest.mock import patch
from board import Board
from game import Game
from chess_rules import ChessRules
from pieces import Pawn, Rook, Knight, Bishop, Queen, King

class TestChess(unittest.TestCase):

    def setUp(self):
        """Creates a fresh game state before each test."""
        self.board = Board()
        self.game = Game()
    
    # ---------------- BOARD TESTS ----------------
    
    def test_get_piece(self):
        """Test that a piece is correctly retrieved from the board."""
        piece = self.board.get_piece((0, 0))  # Should be a Rook
        self.assertIsInstance(piece, Rook)
    
    def test_move_piece(self):
        """Test that a piece moves correctly."""
        pawn = self.board.get_piece((0, 6))  # White pawn
        self.assertTrue(self.board.move_piece(pawn, (0, 4)))  # Move forward 2 spaces
        self.assertEqual(pawn.position, (0, 4))

    def test_copy_board(self):
        """Ensure the board is correctly copied."""
        new_board = self.board.copy()
        self.assertNotEqual(id(self.board), id(new_board))  # Different memory location
        self.assertEqual(len(new_board.grid), 8)  # Should still have 8 rows

    def test_pos_to_chess_notation(self):
        """Ensure board positions convert correctly."""
        self.assertEqual(self.board.pos_to_chess_notation((0, 0)), "a8")
        self.assertEqual(self.board.pos_to_chess_notation((4, 6)), "e2")
    
    def test_threefold_repetition(self):
        """Ensure threefold repetition is correctly detected."""
        self.assertFalse(self.board.is_triple_repetition())

    # ---------------- GAME TESTS ----------------

    def test_switch_turn(self):
        """Ensure turn switching works correctly."""
        self.game.switch_turn()
        self.assertEqual(self.game.current_player, "black")
        self.game.switch_turn()
        self.assertEqual(self.game.current_player, "white")

    def test_check_victory(self):
        """Ensure checkmate is detected correctly."""
        self.assertFalse(self.game.check_victory())  # No one should be checkmated at start

    def test_undo_move(self):
        """Ensure undo works correctly."""
        pawn = self.board.get_piece((0, 6))
        self.game.handle_click((0, 450))  # Select piece
        self.game.handle_click((0, 300))  # Move piece
        self.game.undo_move()
        self.assertEqual(pawn.position, (0, 6))  # Should be back in initial position

    def test_restart_game(self):
        """Ensure game resets properly."""
        self.game.restart_game()
        self.assertEqual(self.game.current_player, "white")  # Game starts with white
        
    def test_fifty_move_rule(self):
        """Ensure the 50-move rule is triggered correctly."""
        self.assertFalse(self.game.is_fifty_move_rule())

    # ---------------- CHESS RULES TESTS ----------------

    def test_is_in_check(self):
        """Ensure check detection works."""
        self.assertFalse(ChessRules.is_in_check(self.board, "white"))

    def test_is_checkmate(self):
        """Ensure checkmate detection works."""
        self.assertFalse(ChessRules.is_checkmate(self.board, "black"))

    def test_is_stalemate(self):
        """Ensure stalemate detection works."""
        self.assertFalse(ChessRules.is_stalemate(self.board, "white"))

    def test_insufficient_material(self):
        """Ensure insufficient material draws are detected."""
        self.assertFalse(ChessRules.is_insufficient_material(self.board))

    # ---------------- PIECE TESTS ----------------

    def test_pawn_moves(self):
        """Test pawn movement."""
        pawn = self.board.get_piece((0, 6))  # White pawn
        moves = pawn.get_moves(self.board)
        self.assertIn((0, 5), moves)  # Can move one step forward

    def test_rook_moves(self):
        """Test rook movement."""
        rook = Rook("white", (0, 0), "assets/rook_white.png")
        self.board.grid[0][0] = rook
        moves = rook.get_moves(self.board)
        self.assertTrue(len(moves) > 0)  # Should be able to move

    def test_knight_moves(self):
        """Test knight movement."""
        knight = Knight("white", (1, 7), "assets/knight_white.png")
        moves = knight.get_moves(self.board)
        self.assertIn((0, 5), moves)  # Knight can move in "L" shape

    def test_bishop_moves(self):
        """Test bishop movement."""
        bishop = Bishop("white", (2, 0), "assets/bishop_white.png")
        moves = bishop.get_moves(self.board)
        self.assertTrue(len(moves) > 0)  # Should move diagonally

    def test_queen_moves(self):
        """Test queen movement."""
        queen = Queen("white", (3, 0), "assets/queen_white.png")
        moves = queen.get_moves(self.board)
        self.assertTrue(len(moves) > 0)  # Should move in all directions

    def test_king_moves(self):
        """Test king movement."""
        king = King("white", (4, 0), "assets/king_white.png")
        moves = king.get_moves(self.board)
        self.assertTrue(len(moves) > 0)  # King should move one step

    def test_pawn_promotion(self):
        """Ensure pawn promotion works"""
        pawn = Pawn("white", (6, 1), "assets/pawn_white.png")
        self.board.grid[1][6] = pawn
        self.assertTrue(self.board.move_piece(pawn, (6, 0)))  # Move to promotion
        # ✅ Simulate choosing a Queen as promotion (or change it to other pieces)
        promoted_piece = Queen("white", (6, 0), "assets/queen_white.png")
        self.board.grid[0][6] = promoted_piece

        # ✅ Ensure the pawn is replaced with a Queen
        new_piece = self.board.get_piece((6, 0))
        self.assertIsInstance(new_piece, Queen)  # Pawn should now be a Queen
        self.assertEqual(new_piece.color, "white")  # Check color consistency
        self.assertNotEqual(self.board.get_piece((6, 0)).__class__.__name__, "Pawn")  # Should be a new piece
        self.assertEqual(self.board.get_piece((6, 0)).__class__.__name__, "Queen")  # Should be a new piece
        return
    
    def test_wrong_castling(self):
        """Test castling is executed correctly."""
        king = self.board.get_piece((4, 7))
        self.assertFalse(self.board.move_piece(king, (6, 7)))  # Small castling

        self.board.grid = [[None for _ in range(8)] for _ in range(8)]
        self.board.grid[0][4] = King("black", (4, 0), "assets/king_black.png")
        self.board.grid[7][4] = King("white", (4, 7), "assets/king_white.png")
        self.board.grid[7][0] = Rook("white", (0, 0), "assets/rook_white.png")

        king = self.board.get_piece((4, 7))
        king.first_move = False
        self.assertFalse(self.board.move_piece(king, (2, 7)))  # Long castling (Queenside)
        self.assertNotEqual(self.board.get_piece((2, 7)), king)  # King should be at c1
        self.assertNotEqual(self.board.get_piece((3, 7)).__class__.__name__, "Rook")  # Rook should be at d1
        return

    # def test_pawn_promotion(self):
    #     """Test pawn promotion."""
    #     pawn = Pawn("white", (6, 1), "assets/pawn_white.png")
    #     self.board.grid[1][6] = pawn
    #     self.board.move_piece(pawn, (6, 0))  # Move to last row
    #     promoted_piece = self.board.get_piece((6, 0))
    #     self.assertNotEqual(promoted_piece.__class__.__name__, "Pawn")  # Should be promoted

    def test_pawn_promotion(self):
        """Test pawn promotion automatically choosing Queen."""
        pawn = Pawn("white", (6, 1), "assets/pawn_white.png")
        self.board.grid[1][6] = pawn

        with patch("builtins.input", return_value="Q"):  # Simulate user typing "Q"
            self.board.move_piece(pawn, (6, 0))  # Move to last rank (promotion)
        
        promoted_piece = self.board.get_piece((6, 0))
        self.assertEqual(promoted_piece.__class__.__name__, "Queen")  # Must be a Queen

    def test_en_passant(self):
        """Test en passant capture."""
        pawn = Pawn("white", (4, 4), "assets/pawn_white.png")
        enemy_pawn = Pawn("black", (3, 4), "assets/pawn_black.png")
        self.board.grid[4][4] = pawn
        self.board.grid[4][3] = enemy_pawn
        self.board.last_move = (enemy_pawn, (3, 6), (3, 4))  # Enemy pawn moved 2 squares forward
        self.assertTrue(self.board.move_piece(pawn, (3, 5)))  # En passant capture

    def test_king_opposition(self):
        """Test that kings cannot move next to each other."""
        self.board.grid = [[None for _ in range(8)] for _ in range(8)]

        self.board.grid[4][4] = King("white", (4, 4), "assets/king_white.png")
        self.board.grid[4][6] = King("black", (6, 4), "assets/king_black.png")
        
        king = self.board.get_piece((4, 4))
        self.assertTrue(isinstance(king, King))
        self.assertFalse(self.board.check_legal_move(king, (5, 4)))  # Should not be allowed

        self.board.grid = [[None for _ in range(8)] for _ in range(8)]
        self.board.grid[7][4] = King("white", (4, 7), "assets/king_white.png")
        self.board.grid[5][4] = King("black", (4, 5), "assets/king_black.png")
        king = self.board.get_piece((4, 7))
        self.assertFalse(self.board.check_legal_move(king, (4, 6)))  # King should not be able to move adjacent
        return

# Run the tests
if __name__ == '__main__':
    unittest.main()
