import unittest
import app


class ApiTestCase(unittest.TestCase):
    def test_is_valid_board(self):
        # Not an array
        board = 'abc'
        self.assertFalse(app.is_valid_board(board))

        # None
        board = None
        self.assertFalse(app.is_valid_board(board))

        # Too few rows
        board = [[None, None, None]]
        self.assertFalse(app.is_valid_board(board))

        # Too many rows
        board = [[None, None, None], [None, None, None], [None, None, None], [None, None, None]]
        self.assertFalse(app.is_valid_board(board))

        # Unrecognized character
        board = [['y', None, None], [None, None, None], [None, None, None]]
        self.assertFalse(app.is_valid_board(board))

        # Too many 'x' plays
        board = [['x', 'x', None], [None, None, None], [None, None, None]]
        self.assertFalse(app.is_valid_board(board))

        # Should pass
        board = [['x', None, None], [None, 'o', None], [None, None, 'o']]
        self.assertTrue(app.is_valid_board(board))

    def test_is_valid_player(self):
        # None
        token = None
        self.assertFalse(app.is_valid_player(token))

        # Unrecognized character
        token = 'y'
        self.assertFalse(app.is_valid_player(token))

        # Not a string
        token = [1, 2, 3]
        self.assertFalse(app.is_valid_player(token))

        # Should pass
        token = 'x'
        self.assertTrue(app.is_valid_player(token))
        token = 'o'
        self.assertTrue(app.is_valid_player(token))


if __name__ == '__main__':
    unittest.main()
