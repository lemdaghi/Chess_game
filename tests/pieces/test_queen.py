import unittest
from .utils import empty_board, place, moves_set, Q, P

class TestQueen(unittest.TestCase):

    def setUp(self):
        """Creates a fresh game state before each test."""
        self.board = empty_board()
    

    def test_queen_full_rays_on_empty_board(self):
        """From the center, queen must list all orthogonal + diagonal squares."""
        board = self.board
        queen = place(board, Q, "white", 3, 3)  # d5
        moves = moves_set(queen, board)

        expected = set()
        # Orthogonals
        expected.update((x, 3) for x in range(8) if x != 3)  # rank
        expected.update((3, y) for y in range(8) if y != 3)  # file
        # Diagonals
        for i in range(1, 8):
            if 3+i < 8 and 3+i < 8: expected.add((3+i, 3+i))      
            if 3-i >= 0 and 3-i >= 0: expected.add((3-i, 3-i))     
            if 3+i < 8 and 3-i >= 0: expected.add((3+i, 3-i))      
            if 3-i >= 0 and 3+i < 8: expected.add((3-i, 3+i))      

        self.assertEqual(moves, expected)

        self.assertNotIn((5, 4), moves)    # knight-like
        self.assertNotIn((4, 5), moves)    # knight-like
        self.assertNotIn((3, 3), moves)    # cannot stay
    

    def test_queen_blocked_by_allies(self):
        board = self.board
        queen = place(board, Q, "white", 3, 3)

        # Orthogonal blockers
        place(board, P, "white", 3, 1) 
        place(board, P, "white", 5, 3) 
        place(board, P, "white", 3, 5) 
        place(board, P, "white", 1, 3) 

        # Diagonal blockers
        place(board, P, "white", 5, 5)  
        place(board, P, "white", 1, 1)  
        place(board, P, "white", 5, 1)  
        place(board, P, "white", 1, 5)  

        moves = moves_set(queen, board)
        expected = {
            # orthogonal: one before each blocker
            (3, 2), (4, 3), (3, 4), (2, 3),
            # diagonal: one before each blocker
            (4, 4), (2, 2), (4, 2), (2, 4),
        }
        self.assertEqual(moves, expected)


    def test_queen_stops_on_capture(self):
        queen = place(self.board, Q, "white", 3, 4)  # d4
        place(self.board, P, "black", 6, 4)  # g4 (target)
        moves = moves_set(queen, self.board)
        self.assertIn((6, 4), moves)  # capture
        self.assertNotIn((7, 4), moves)  # can't go further

if __name__ == "__main__":
    unittest.main()
