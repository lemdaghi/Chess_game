import unittest
from .utils import empty_board, place, moves_set, R, P

class TestRook(unittest.TestCase):

    def setUp(self):
        """Creates a fresh game state before each test."""
        self.board = empty_board()

    
    def test_rook_full_rays_on_empty_board(self):
        """On an empty board, rook should list all squares along rank and file."""
        rook = place(self.board, R, "white", 3, 3)  # d5 (x=3,y=3)
        moves = moves_set(rook, self.board)

        expected = set()
        
        expected.update((col, 3) for col in range(8) if col != 3)
        
        expected.update((3, row) for row in range(8) if row != 3)

        self.assertEqual(moves, expected)
        
        self.assertNotIn((4, 4), moves)  # no diagonal
        self.assertNotIn((3, 3), moves)  # cannot stay in place


    def test_rook_blocked_by_own_piece(self):
        """Test rook movement blocked by own piece."""
        board = self.board
        rook = place(board, R, "white", 3, 3)

        place(board, P, "white", 3, 1)  # up blocker
        place(board, P, "white", 5, 3)  # right blocker
        place(board, P, "white", 3, 5)  # down blocker
        place(board, P, "white", 1, 3)  # left blocker

        moves = moves_set(rook, board)
        expected = {(3, 2), (4, 3), (3, 4), (2, 3)}
        self.assertEqual(moves, expected)


    def test_rook_capture_opponent(self): 
        """Test rook capturing an opponent's piece."""
        board = self.board
        rook = place(board, R, "white", 3, 3)

        place(board, P, "black", 3, 1)  # up enemy
        place(board, P, "black", 6, 3)  # right enemy

        moves = moves_set(rook, board)

        # Up ray
        self.assertIn((3, 2), moves)   # before enemy
        self.assertIn((3, 1), moves)   # capture
        self.assertNotIn((3, 0), moves)  # beyond enemy -> forbidden

        # Right ray
        self.assertIn((4, 3), moves)
        self.assertIn((5, 3), moves)
        self.assertIn((6, 3), moves)   # capture
        self.assertNotIn((7, 3), moves)  # beyond enemy


    def test_rook_moves_on_ranks_and_files_until_block(self):
        rook = place(self.board, R, "white", 0, 7)   # a1
        # Blockers: ally in a3 (0,5) and ennemy in a5 (0,3)
        place(self.board, P, "white", 0, 5)  # a3 (block)
        place(self.board, P, "black", 0, 3)  # a5 (capturable, and stop)
        moves = moves_set(rook, self.board)

        for col in range(1, 8):  # b1..h1
            self.assertIn((col, 7), moves)

        self.assertIn((0, 6), moves)
        self.assertNotIn((0, 5), moves)

        self.board.grid[5][0] = None
        moves2 = moves_set(rook, self.board)
        self.assertIn((0, 6), moves2)
        self.assertIn((0, 5), moves2)
        self.assertIn((0, 4), moves2)
        self.assertIn((0, 3), moves2)   # capture
        self.assertNotIn((0, 2), moves2)  # can't go further


# Run the tests
if __name__ == '__main__':
    unittest.main()
