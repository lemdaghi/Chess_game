import unittest
from .utils import empty_board, place, moves_set, B, P


class TestBishop(unittest.TestCase):

    def setUp(self):
        """Creates a fresh game state before each test."""
        self.board = empty_board()

    def test_bishop_full_diagonals_on_empty_board(self):
        """From the center, bishop must list all diagonal squares and nothing else."""
        board = place(self.board, B, "white", 3, 3)  # d5
        moves = moves_set(board, self.board)

        expected = set()
        # right top (+1,-1): (4,2),(5,1),(6,0)
        expected.update([(4, 2), (5, 1), (6, 0)])
        # left top (-1,-1): (2,2),(1,1),(0,0)
        expected.update([(2, 2), (1, 1), (0, 0)])
        # right bottom (+1,+1): (4,4),(5,5),(6,6),(7,7)
        expected.update([(4, 4), (5, 5), (6, 6), (7, 7)])
        # left bottom (-1,+1): (2,4),(1,5),(0,6)
        expected.update([(2, 4), (1, 5), (0, 6)])

        self.assertEqual(moves, expected)
       
        self.assertNotIn((3, 4), moves)
        self.assertNotIn((4, 3), moves)
        self.assertNotIn((3, 3), moves)

    
    def test_bishop_diagonals_and_block(self):
        board = place(self.board, B, "white", 2, 7)  # c1
       
        place(self.board, P, "white", 3, 6)  # d2 (diagonal blocked by ally)
        place(self.board, P, "black", 1, 6)  # b2 (capturable piece)
        moves = moves_set(board, self.board)
        self.assertIn((1, 6), moves)   # c1xb2
        self.assertNotIn((0, 5), moves)  # can not go beyond the capturable piece
        self.assertNotIn((4, 5), moves)  # c1->d2 blocked by ally
        
        self.assertNotIn((-1, 4), moves) # not on the board


    def test_bishop_captures_enemy_and_stops(self):
        board = self.board
        bishop = place(board, B, "white", 3, 3)   # d5
        place(board, P, "black", 6, 6)         # g2
        place(board, P, "black", 1, 5)         # b3

        moves = moves_set(bishop, board)

        # left bottom ray: includes (4,4),(5,5),(6,6) but not (7,7)
        self.assertIn((4, 4), moves)
        self.assertIn((5, 5), moves)
        self.assertIn((6, 6), moves)
        self.assertNotIn((7, 7), moves)

        # right bottom ray: includes (2,4),(1,5) but not (0,6)
        self.assertIn((2, 4), moves)
        self.assertIn((1, 5), moves)
        self.assertNotIn((0, 6), moves)

        # top is unobstructed (edge to edge)
        self.assertIn((4, 2), moves)
        self.assertIn((5, 1), moves)
        self.assertIn((6, 0), moves)
        self.assertIn((2, 2), moves)
        self.assertIn((1, 1), moves)
        self.assertIn((0, 0), moves)

# Run the tests
if __name__ == '__main__':
    unittest.main()
