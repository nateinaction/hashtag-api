import unittest
import app


class ApiTestCase(unittest.TestCase):
    def test_is_valid_request(self):
        # Not a dict
        json_obj = 123
        self.assertFalse(app.is_valid_request(json_obj))

        # Request does not contain board key
        json_obj = {
            'hello': None
        }
        self.assertFalse(app.is_valid_request(json_obj))

        # Should pass
        json_obj = {
            'board': None
        }
        self.assertTrue(app.is_valid_request(json_obj))

    def test_is_list_with_3_elements(self):
        # Not a list
        a_list = 'abc'
        self.assertFalse(app.is_list_with_3_elements(a_list))

        # None
        a_list = None
        self.assertFalse(app.is_list_with_3_elements(a_list))

        # Empty array
        a_list = []
        self.assertFalse(app.is_list_with_3_elements(a_list))

        # Too few elements
        a_list = [1]
        self.assertFalse(app.is_list_with_3_elements(a_list))

        # Too many elements
        a_list = [1, 2, 3, 4]
        self.assertFalse(app.is_list_with_3_elements(a_list))

        # Should pass
        a_list = [1, 2, 3]
        self.assertTrue(app.is_list_with_3_elements(a_list))

    def test_are_rows_valid(self):
        # Row is not a list
        board = ['123', [None, None, None], [None, None, None]]
        self.assertFalse(app.are_rows_valid(board))

        # Too few tokens in a row
        board = [[None, None], [None, None, None], [None, None, None]]
        self.assertFalse(app.are_rows_valid(board))

        # Too many tokens in a row
        board = [[None, None, None, None], [None, None, None], [None, None, None]]
        self.assertFalse(app.are_rows_valid(board))

        # Should pass
        board = [[None, None, None], [None, None, None], [None, None, None]]
        self.assertTrue(app.are_rows_valid(board))

    def test_are_tokens_valid(self):
        # Unrecognized character
        board = [[1, None, None], [None, None, None], [None, None, None]]
        self.assertFalse(app.are_tokens_valid(board))

        # Should pass
        board = [['x', None, None], [None, 'o', None], [None, None, 'x']]
        self.assertTrue(app.are_tokens_valid(board))

    def test_is_game_fair(self):
        # Too many 'x' plays
        board = [['x', 'x', None], [None, None, None], [None, None, None]]
        self.assertFalse(app.is_game_fair(board))

        # Too many 'o' plays
        board = [['x', 'o', 'o'], [None, None, None], [None, None, None]]
        self.assertFalse(app.is_game_fair(board))

        # Should pass
        board = [['x', None, None], [None, 'o', None], [None, None, 'x']]
        self.assertTrue(app.is_game_fair(board))


if __name__ == '__main__':
    unittest.main()
