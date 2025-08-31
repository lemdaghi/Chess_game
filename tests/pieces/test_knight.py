import unittest
from .utils import empty_board, place, moves_set, N, P

class TestKnight(unittest.TestCase):

    def setUp(self):
        """Creates a fresh game state before each test."""
        self.board = empty_board()

    
    def test_knight_full_set_from_center(self):
        """From a center square, the knight must list exactly 8 legal L-moves."""
        k = place(self.board, N, "white", 3, 3)  # d5
        moves = moves_set(k, self.board)
        expected = {
            (5, 4), (5, 2), (1, 4), (1, 2),
            (4, 5), (4, 1), (2, 5), (2, 1),
        }
        self.assertEqual(moves, expected)
        self.assertNotIn((3, 3), moves)  # cannot stay in place

        # no straight or diagonal moves
        self.assertNotIn((3, 4), moves)
        self.assertNotIn((4, 4), moves)


    def test_knight_leaps_over_pieces(self):
        knight = place(self.board, N, "white", 1, 7)  # b1

        place(self.board, P, "white", 0, 6)  # a2
        place(self.board, P, "white", 1, 6)  # b2
        place(self.board, P, "white", 2, 6)  # c2
        moves = moves_set(knight, self.board)

        # Possible moves from b1 : a3 (0,5) et c3 (2,5), d2 (3,6)
        self.assertIn((0, 5), moves)  # a3
        self.assertIn((2, 5), moves)  # c3
        self.assertIn((3, 6), moves)  # d2


    def test_knight_cannot_land_on_own_piece(self):
        knight = place(self.board, N, "white", 3, 3)  # d5
        place(self.board, P, "white", 4, 5)  # e3 (ally position)
        moves = moves_set(knight, self.board)
        self.assertNotIn((4, 5), moves)

    
    def test_knight_can_capture_enemy_on_landing_square(self):
        """Enemy on a landing square is capturable."""
        k = place(self.board, N, "white", 3, 3)  # d5
        place(self.board, P, "black", 4, 5)      # e3 (enemy)
        moves = moves_set(k, self.board)
        self.assertIn((4, 5), moves)


# Run the tests
if __name__ == '__main__':
    unittest.main()
