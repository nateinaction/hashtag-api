import unittest
import hashtag


class TestMe(unittest.TestCase):
    def test_find_winner(self):
        self.assertEqual(None, hashtag.find_winner([[None, None, None]]))
        self.assertEqual(None, hashtag.find_winner([['x', None, 'x']]))
        self.assertEqual(None, hashtag.find_winner([['y', 'y', 'y']]))
        self.assertEqual(None, hashtag.find_winner([['x', None, 'x', 'x', 'x']]))
        self.assertEqual(None, hashtag.find_winner([['x', 'x']]))
        self.assertEqual(None, hashtag.find_winner([['x', 'x', 'o']]))
        self.assertEqual('x', hashtag.find_winner([['x', 'x', 'x']]))
        self.assertEqual('o', hashtag.find_winner([['o', 'o', 'o']]))
        self.assertEqual('x', hashtag.find_winner([['x', None, 'x', 'x']]))
        self.assertEqual('x', hashtag.find_winner([['x', 'x', 'x'], ['x', 'x', 'o']]))
        self.assertEqual('x', hashtag.find_winner([[None, None, None], ['x', 'x', 'x']]))

    def test_collate_possible_win_groups(self):
        input_board = [
            ['1', '2', '3'],
            ['4', '5', '6'],
            ['7', '8', '9'],
        ]
        expect = [
            ['1', '2', '3'],
            ['4', '5', '6'],
            ['7', '8', '9'],
            ['1', '4', '7'],
            ['2', '5', '8'],
            ['3', '6', '9'],
            ['1', '5', '9'],
            ['3', '5', '7'],
        ]
        self.assertEqual(expect, hashtag.collate_possible_win_groups(input_board))

    def test_get_current_turn(self):
        self.assertEqual('x', hashtag.get_current_turn([[None, None, None], [None, None, None], [None, None, None]]))
        self.assertEqual('o', hashtag.get_current_turn([['x', None, None], [None, None, None], [None, None, None]]))
        self.assertEqual('x', hashtag.get_current_turn([['x', 'o', None], [None, None, None], [None, None, None]]))
        self.assertEqual('x', hashtag.get_current_turn([['x', 'x', None], [None, None, None], [None, None, None]]))
        self.assertEqual(None, hashtag.get_current_turn([['x', 'x', 'x']]))

    def test_maximize_moves(self):
        available_moves = [
            hashtag.Move(row=0, col=1, score=-16),
            hashtag.Move(row=1, col=2, score=6),
            hashtag.Move(row=2, col=1, score=-1),
            hashtag.Move(row=2, col=2, score=1),
            hashtag.Move(row=2, col=2, score=6),
        ]
        expected_sorted_moves = hashtag.SortedMoves(
            score=6,
            moves=[
                hashtag.Move(row=1, col=2, score=6),
                hashtag.Move(row=2, col=2, score=6),
            ]
        )
        self.assertEqual(expected_sorted_moves, hashtag.maximize_moves(available_moves))
        available_moves = [hashtag.Move(row=2, col=0, score=-2)]
        expected_sorted_moves = hashtag.SortedMoves(
            score=-2,
            moves=[hashtag.Move(row=2, col=0, score=-2)]
        )
        self.assertEqual(expected_sorted_moves, hashtag.maximize_moves(available_moves))

    def test_minimize_moves(self):
        available_moves = [
            hashtag.Move(row=0, col=1, score=-16),
            hashtag.Move(row=1, col=2, score=6),
            hashtag.Move(row=2, col=1, score=-1),
            hashtag.Move(row=2, col=2, score=1),
            hashtag.Move(row=2, col=2, score=6),
        ]
        expected_sorted_moves = hashtag.SortedMoves(
            score=-16,
            moves=[
                hashtag.Move(row=0, col=1, score=-16),
            ]
        )
        self.assertEqual(expected_sorted_moves, hashtag.minimize_moves(available_moves))
        available_moves = [hashtag.Move(row=2, col=0, score=-2)]
        expected_sorted_moves = hashtag.SortedMoves(
            score=-2,
            moves=[hashtag.Move(row=2, col=0, score=-2)]
        )
        self.assertEqual(expected_sorted_moves, hashtag.minimize_moves(available_moves))

    def test_select_sorted_move(self):
        seed = 0
        sorted_moves = hashtag.SortedMoves(
            score=6,
            moves=[
                hashtag.Move(row=1, col=2, score=6),
                hashtag.Move(row=2, col=2, score=6),
            ],
        )
        expect = hashtag.Move(row=2, col=2, score=6)
        self.assertEqual(expect, hashtag.select_sorted_move(sorted_moves, seed))
        sorted_moves = hashtag.SortedMoves(
            score=-2,
            moves=[
                hashtag.Move(row=2, col=0, score=-2),
            ],
        )
        expect = hashtag.Move(row=2, col=0, score=-2)
        self.assertEqual(expect, hashtag.select_sorted_move(sorted_moves, seed))

    def test_rank_available_moves(self):
        # 'x' should play on 1, 1 even though 'o' is in winning pos.
        board = [
            ['o', None, 'x'],
            ['x', None, 'x'],
            [None, 'o', 'o'],
        ]
        expect = [
            hashtag.Move(row=0, col=1, score=-11),
            hashtag.Move(row=1, col=1, score=10),
            hashtag.Move(row=2, col=0, score=7),
        ]
        self.assertEqual(expect, hashtag.rank_available_moves(board, 'o'))

        # 'o' should play on 1, 1 to prevent 'x from winning
        board = [
            ['o', None, 'x'],
            ['x', None, 'x'],
            ['x', 'o', 'o'],
        ]
        expect = [hashtag.Move(row=0, col=1, score=-11), hashtag.Move(row=1, col=1, score=10)]
        self.assertEqual(expect, hashtag.rank_available_moves(board))

        # 'x' should play on 0, 1 to tie game
        board = [
            ['o', None, 'x'],
            ['x', 'o', 'x'],
            ['x', 'o', 'o'],
        ]
        expect = [hashtag.Move(row=0, col=1, score=-10)]
        self.assertEqual(expect, hashtag.rank_available_moves(board, 'o'))

        # No moves available should return empty array
        board = [
            ['o', 'x', 'x'],
            ['x', 'o', 'x'],
            ['x', 'o', 'o'],
        ]
        expect = []
        self.assertEqual(expect, hashtag.rank_available_moves(board))

    def test_select_next_move(self):
        # 'x' should play on 1, 1 even though 'o' is in winning pos.
        board = [
            ['o', None, 'x'],
            ['x', None, 'x'],
            [None, 'o', 'o'],
        ]
        human_player = 'o'
        seed = 0
        expect = hashtag.Move(row=1, col=1, score=10)
        self.assertEqual(expect, hashtag.select_next_move(board, seed))

        # 'o' should play on 1, 1 to prevent 'x from winning
        board = [
            ['o', None, 'x'],
            ['x', None, 'x'],
            ['x', 'o', 'o'],
        ]
        human_player = 'x'
        seed = 0
        expect = hashtag.Move(row=1, col=1, score=10)
        self.assertEqual(expect, hashtag.select_next_move(board, seed))

        # 'x' should play on 0, 1 to tie game
        board = [
            ['o', None, 'x'],
            ['x', 'o', 'x'],
            ['x', 'o', 'o'],
        ]
        human_player = 'o'
        seed = 0
        expect = hashtag.Move(row=0, col=1, score=-10)
        self.assertEqual(expect, hashtag.select_next_move(board, seed))

        # No moves available should return empty array
        board = [
            ['o', 'x', 'x'],
            ['x', 'o', 'x'],
            ['x', 'o', 'o'],
        ]
        expect = None
        self.assertEqual(expect, hashtag.select_next_move(board))

        # Should pick corner
        board = [[None, None, None], [None, None, None], [None, None, None]]
        human_player = 'o'
        seed = 0
        expect = hashtag.Move(row=2, col=2, score=0)
        self.assertEqual(expect, hashtag.select_next_move(board, seed))
        board = [[None, None, None], [None, 'x', None], [None, None, None]]
        human_player = 'x'
        seed = 0
        expect = hashtag.Move(row=2, col=2, score=0)
        self.assertEqual(expect, hashtag.select_next_move(board, seed))
        board = [[None, 'x', None], [None, None, None], [None, None, None]]
        human_player = 'x'
        seed = 0
        expect = hashtag.Move(row=2, col=2, score=0)
        self.assertEqual(expect, hashtag.select_next_move(board, seed))

        # Should pick center
        board = [['x', None, None], [None, None, None], [None, None, None]]
        human_player = 'x'
        seed = 0
        expect = hashtag.Move(row=1, col=1, score=0)
        self.assertEqual(expect, hashtag.select_next_move(board, seed))


if __name__ == '__main__':
    unittest.main()
