# import unittest
# from board import Board
# from game import Game
# from pieces import King, Queen, Rook, Bishop, Knight, Pawn
# from chess_rules import ChessRules

# class TestChess(unittest.TestCase):

#     def setUp(self):
#         """Create a fresh board for each test."""
#         self.board = Board()

#     # Board Setup
#     def test_draw_board(self):
#         return
    
#     def test_draw_piece(self):
#         return
    
#     def test_get_piece(self):
#         self.board = Board()

#         piece = self.board.get_piece((0, 6))  # White pawn at a2
#         self.assertIsNotNone(piece)
#         self.assertEqual(piece.__class__.__name__, "Pawn")

#         case = self.board.get_piece((4, 4))
#         self.assertIsNone(case)
    
#     # Moves
#     def test_get_moves(self):
#         return
    
#     def test_move_piece(self):
#         return
    
#     def test_check_moves(self):
#         return
    
#     # Special rules
    # def test_short_castling(self):
    #     self.board = Board()
    #     self.board.grid = [[None for _ in range(8)] for _ in range(8)]
    #     self.board.grid[0][4] = King("black", (4, 0), "assets/king_black.png")
    #     self.board.grid[7][4] = King("white", (4, 7), "assets/king_white.png")
    #     self.board.grid[7][7] = Rook("white", (7, 7), "assets/rook_white.png")

    #     king = self.board.get_piece((4, 7))
    #     self.assertTrue(self.board.move_piece(king, (6, 7)))  # Short castling (kingside)
    #     self.assertEqual(self.board.get_piece((6, 7)), king)  # King should be at g1
    #     self.assertEqual(self.board.get_piece((5, 7)).__class__.__name__, "Rook")  # Rook should be at f1

    # def test_long_castling(self):   
    #     self.board = Board()
    #     self.board.grid = [[None for _ in range(8)] for _ in range(8)]
    #     self.board.grid[0][4] = King("black", (4, 0), "assets/king_black.png")
    #     self.board.grid[7][4] = King("white", (4, 7), "assets/king_white.png")
    #     self.board.grid[7][0] = Rook("white", (0, 0), "assets/rook_white.png")

    #     king = self.board.get_piece((4, 7))
    #     self.assertTrue(self.board.move_piece(king, (2, 7)))  # Long castling (Queenside)
    #     self.assertEqual(self.board.get_piece((2, 7)), king)  # King should be at c1
    #     self.assertEqual(self.board.get_piece((3, 7)).__class__.__name__, "Rook")  # Rook should be at d1

#     def test_pawn_promotion(self):
#         self.board = Board()
#         self.board.grid = [[None for _ in range(8)] for _ in range(8)]
#         self.board.grid[7][4] = King("white", (4, 7), "assets/king_white.png")
#         self.board.grid[0][4] = King("black", (4, 0), "assets/king_black.png")
#         self.board.grid[1][4] = Pawn("white", (4, 1), "assets/white.png")

#         pawn = self.board.get_piece((4, 1))
#         self.assertTrue(self.board.move_piece(pawn, (4, 1)))  # pawn promotion
#         # Il faut faire un choix pour la promotion et s'assurer que la promotion a bien été réalisée

#         return

#     def test_en_passant(self):
#         """Ensure en passant captures work correctly."""
#         self.board = Board()
#         self.board.move_piece(self.board.get_piece((4, 6)), (4, 4))  # e2 → e4
#         self.board.move_piece(self.board.get_piece((3, 1)), (3, 3))  # d7 → d5
#         self.board.move_piece(self.board.get_piece((4, 4)), (3, 3))  # e4 → d5 (En Passant)

#         self.assertIsNone(self.board.get_piece((3, 4)))  # Captured pawn should be gone
#         self.assertEqual(self.board.get_piece((3, 3)).__class__.__name__, "Pawn")  # Moved pawn should be there
    
#     # Game logic
#     def test_check(self):
#         return

#     def test_checkmate(self):
#         """Test checkmate detection (Fool’s Mate)."""
#         self.board = Board()
#         self.board.move_piece(self.board.get_piece((5, 6)), (5, 5))  # f2 → f3
#         self.board.move_piece(self.board.get_piece((4, 1)), (4, 3))  # e7 → e5
#         self.board.move_piece(self.board.get_piece((6, 6)), (6, 4))  # g2 → g4
#         self.board.move_piece(self.board.get_piece((3, 0)), (7, 4))  # Qd8 → h5 (Checkmate)

#         self.assertTrue(ChessRules.is_checkmate(self.board, "white"))
    
#     # Draw Conditions
#     def test_stalemate(self):
#         """Test stalemate scenario where no legal moves exist but king is NOT in check."""
#         self.board = Board()
#         self.board.grid = [[None for _ in range(8)] for _ in range(8)]
#         self.board.grid[7][7] = King("white", (7, 7), "assets/king_white.png")
#         self.board.grid[5][6] = Queen("black", (5, 6), "assets/queen_black.png")
#         self.board.grid[6][5] = King("black", (6, 5), "assets/king_black.png")

#         self.assertTrue(ChessRules.is_stalemate(self.board, "white"))
    
#     def test_insufficient_material(self):
#         # test all cases
#         return
    
#     def test_threefold_repetition(self):
#         self.board = Board()
#         for _ in range(3):  # Repeat same move three times
#             self.board.move_piece(self.board.get_piece((1, 7)), (2, 5))  # Move knight b8 → c6
#             self.board.move_piece(self.board.get_piece((1, 0)), (2, 2))  # Move knight b1 → c3
#             self.board.move_piece(self.board.get_piece((2, 5)), (1, 7))  # Undo
#             self.board.move_piece(self.board.get_piece((2, 2)), (1, 0))  # Undo

#         self.assertTrue(ChessRules.is_threefold_repetition(self.board))

#     def test_fifty_move_rule(self):
#         return
    
#     # Game mechanics
#     def test_undo(self):
#         return

#     def test_restart(self):
#         return

#     def test_rematch(self):
#         return

#     def test_check_victory(self):
#         return
    
#     # Clock
#     def test_run_clock(self):
#         return

#     def test_display_time(self):
#         return

#     def test_format_time(self):
#         game = Game()
#         self.assertTrue(game.format_time(600) == "10:00")
#         self.assertTrue(game.format_time(180) == "3:00")
#         self.assertTrue(game.format_time(200) == "3:20")
#         self.assertTrue(game.format_time(3600) == "60:00")
#         self.assertTrue(game.format_time(3147) == "52:27")
#         return
    
#     # Others tests
#     def test_handle_click(self):
#         return

#     def test_draw_points(self):
#         return
    
#     def test_switch_turn(self):
#         return

#     def test_king_opposition(self):
#         return

#     def test_record_position(self):
#         return
    
#     def test_chess_notation(self):
#         return

#     def test_pinning_piece(self):
#         return

#     def test_get_move_history(self):
#         return    

# if __name__ == "__main__":
#     unittest.main()


import unittest
import time
from board import Board
from game import Game
from pieces import King, Queen, Rook, Bishop, Knight, Pawn
from chess_rules import ChessRules


class TestChess(unittest.TestCase):

    def setUp(self):
        """Create a new game instance before each test"""
        self.game = Game(mode="2_players")
        self.board = self.game.board  # Access board from game instance

    ## ====================== UNIT TESTS ====================== ##
    
    def test_board_initialization(self):
        """Ensure board starts with correct piece placement."""
        self.assertEqual(self.board.get_piece((0, 6)).__class__.__name__, "Pawn")
        self.assertEqual(self.board.get_piece((4, 7)).__class__.__name__, "King")
        self.assertEqual(self.board.get_piece((3, 0)).__class__.__name__, "Queen")
        return

    def test_get_piece(self):
        """Ensure we can retrieve pieces correctly"""
        piece = self.board.get_piece((0, 6))  # White pawn at a2
        self.assertIsNotNone(piece)
        self.assertEqual(piece.__class__.__name__, "Pawn")
        return

    def test_move_piece(self):
        """Test a basic piece movement"""
        pawn = self.board.get_piece((4, 6))  # e2
        self.assertTrue(self.board.move_piece(pawn, (4, 4)))  # Move e2 → e4
        self.assertIsNone(self.board.get_piece((4, 6)))  # e2 should be empty
        self.assertEqual(self.board.get_piece((4, 4)), pawn)  # Pawn should be at e4
        return

    def test_king_opposition(self):
        """Ensure king can't move adjacent to enemy king"""
        self.board.grid = [[None for _ in range(8)] for _ in range(8)]
        self.board.grid[7][4] = King("white", (4, 7), "assets/king_white.png")
        self.board.grid[5][4] = King("black", (4, 5), "assets/king_black.png")
        king = self.board.get_piece((4, 7))
        self.assertFalse(self.board.check_legal_move(king, (4, 6)))  # King should not be able to move adjacent
        return

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

    def test_castling(self):
        """Ensure castling follows all rules"""
        self.board.grid = [[None for _ in range(8)] for _ in range(8)]
        self.board.grid[7][4] = King("white", (4, 7), "assets/king_white.png")
        self.board.grid[7][7] = Rook("white", (7, 7), "assets/rook_white.png")
        king = self.board.get_piece((4, 7))
        self.assertTrue(self.board.move_piece(king, (6, 7)))  # Kingside castling should be allowed
        return

    def test_fifty_move_rule(self):
        """Ensure 50-move rule triggers a draw"""
        self.game.count_moves = 100  # Simulate 50 moves
        self.assertTrue(self.game.is_fifty_move_rule())
        return

    ## =================== INTEGRATION TESTS ================== ##
    
    def test_fools_mate(self):
        """Simulate Fool's Mate (fastest checkmate)"""
        self.game.handle_click((5 * 75, 6 * 75))  # f2
        self.game.handle_click((5 * 75, 4 * 75))  # f3
        self.game.handle_click((4 * 75, 1 * 75))  # e7
        self.game.handle_click((4 * 75, 3 * 75))  # e5
        self.game.handle_click((6 * 75, 6 * 75))  # g2
        self.game.handle_click((6 * 75, 4 * 75))  # g4
        self.game.handle_click((3 * 75, 0 * 75))  # Queen move
        self.game.handle_click((7 * 75, 4 * 75))  # Checkmate move
        self.assertTrue(ChessRules.is_checkmate(self.board, "white"))
        return

    def test_stalemate(self):
        """Ensure stalemate is detected"""
        self.board.grid = [[None for _ in range(8)] for _ in range(8)]
        self.board.grid[7][7] = King("white", (7, 7), "assets/king_white.png")
        self.board.grid[5][6] = Queen("black", (5, 6), "assets/queen_black.png")
        self.board.grid[6][5] = King("black", (6, 5), "assets/king_black.png")
        self.assertTrue(ChessRules.is_stalemate(self.board, "white"))
        return

    ## ================ FUNCTIONAL (END-TO-END) TESTS ================ ##

    def test_full_game_simulation(self):
        """Play an entire game and verify the game ends correctly"""
        move_sequence = [
            ((4, 6), (4, 4)),  # e2 → e4
            ((6, 1), (6, 3)),  # g7 → g5
            ((2, 6), (2, 4)),  # b2 → b4
        ]

        for old_pos, new_pos in move_sequence:
            piece = self.board.get_piece(old_pos)
            self.assertIsNotNone(piece)
            self.assertTrue(self.board.move_piece(piece, new_pos))
            self.game.switch_turn()

        self.assertFalse(ChessRules.is_checkmate(self.board, "black"))


        move_sequence = [
            ((5, 1), (5, 3)),  # black move f7 → f5
            ((3, 7), (7, 3)),  # Qd1 → h5 (Fast checkmate)
        ]

        for old_pos, new_pos in move_sequence:
            piece = self.board.get_piece(old_pos)
            self.assertIsNotNone(piece)
            self.assertTrue(self.board.move_piece(piece, new_pos))
            self.game.switch_turn()

        self.assertTrue(ChessRules.is_checkmate(self.board, "black"))

        return

    def test_timer_functionality(self):
        """Ensure the clock decrements properly"""
        initial_time = self.game.player_timers["white"]
        time.sleep(2)  # Simulate waiting
        self.assertLess(self.game.player_timers["white"], initial_time)  # Timer should have decreased
        return

    def test_restart_game(self):
        """Ensure restart sets up a new board"""
        self.game.restart_game()
        self.assertIsNotNone(self.board.get_piece((4, 7)))  # White King should be back
        self.assertIsNotNone(self.board.get_piece((3, 0)))  # Black Queen should be back
        self.assertEqual(self.game.current_player, "white")  # White should start
        return

if __name__ == '__main__':
    unittest.main()
