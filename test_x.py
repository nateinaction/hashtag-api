import unittest
import x


class TestMe(unittest.TestCase):
    def test_who_won(self):
        self.assertEqual(x.find_winner([[None, None, None]]), None)
        self.assertEqual(x.find_winner([['x', None, 'x']]), None)
        self.assertEqual(x.find_winner([['y', 'y', 'y']]), None)
        self.assertEqual(x.find_winner([['x', None, 'x', 'x', 'x']]), None)
        self.assertEqual(x.find_winner([['x', 'x']]), None)
        self.assertEqual(x.find_winner([['x', 'x', 'o']]), None)
        self.assertEqual(x.find_winner([['x', 'x', 'x']]), 'x')
        self.assertEqual(x.find_winner([['o', 'o', 'o']]), 'o')
        self.assertEqual(x.find_winner([['x', None, 'x', 'x']]), 'x')
        self.assertEqual(x.find_winner([['x', 'x', 'x'], ['x', 'x', 'o']]), 'x')
        self.assertEqual(x.find_winner([[None, None, None], ['x', 'x', 'x']]), 'x')

    def test_possible_wins(self):
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
        self.assertEqual(expect, x.collate_possible_win_groups(input_board))

    def test_who_goes_next(self):
        self.assertEqual('x', x.who_goes_next(None))
        self.assertEqual('x', x.who_goes_next('o'))
        self.assertEqual('o', x.who_goes_next('x'))
        self.assertEqual('x', x.who_goes_next(123))

    def test_who_goes_next2(self):
        self.assertEqual('x', x.who_goes_next2([[None, None, None], [None, None, None], [None, None, None]]))
        self.assertEqual('o', x.who_goes_next2([['x', None, None], [None, None, None], [None, None, None]]))
        self.assertEqual('x', x.who_goes_next2([['x', 'o', None], [None, None, None], [None, None, None]]))
        self.assertEqual('x', x.who_goes_next2([['x', 'x', None], [None, None, None], [None, None, None]]))
        self.assertEqual(None, x.who_goes_next2([['x', 'x', 'x']]))

    def test_find_best_moves(self):
        available_moves = [
            x.Move(row=0, col=1, score=-16),
            x.Move(row=1, col=2, score=6),
            x.Move(row=2, col=1, score=-1),
            x.Move(row=2, col=2, score=1),
            x.Move(row=2, col=2, score=6),
        ]
        expected_best_moves = x.BestMoves(
            score=6,
            moves=[
                x.Move(row=1, col=2, score=6),
                x.Move(row=2, col=2, score=6),
            ]
        )
        self.assertEqual(expected_best_moves, x.find_best_moves(available_moves))
        available_moves = [x.Move(row=2, col=0, score=-2)]
        expected_best_moves = x.BestMoves(
            score=-2,
            moves=[x.Move(row=2, col=0, score=-2)]
        )
        self.assertEqual(expected_best_moves, x.find_best_moves(available_moves))

    def test_select_best_move(self):
        seed = 0
        best_moves = x.BestMoves(
            score=6,
            moves=[
                x.Move(row=1, col=2, score=6),
                x.Move(row=2, col=2, score=6),
            ],
        )
        expect = x.Move(row=2, col=2, score=6)
        self.assertEqual(expect, x.select_best_move(best_moves, seed))
        best_moves = x.BestMoves(
            score=-2,
            moves=[
                x.Move(row=2, col=0, score=-2),
            ],
        )
        expect = x.Move(row=2, col=0, score=-2)
        self.assertEqual(expect, x.select_best_move(best_moves, seed))

    def test_rank_available_moves(self):
        test_board = [
            ['x', 'o', 'x'],
            ['o', 'x', 'o'],
            ['o', 'x', None],
        ]
        self.assertEqual([x.Move(row=2, col=2, score=0)], x.rank_available_moves(test_board),
                         "No win scenario should return None")
        test_board = [
            ['o', 'x', 'o'],
            ['x', None, 'x'],
            ['o', 'x', 'o'],
        ]
        self.assertEqual([x.Move(row=1, col=1, score=-10)], x.rank_available_moves(test_board))
        test_board = [
            [None, 'x', 'x'],
            ['x', None, 'x'],
            ['x', 'x', None],
        ]
        self.assertEqual([x.Move(row=0, col=0, score=10), x.Move(row=1, col=1, score=10), x.Move(row=2, col=2, score=10)], x.rank_available_moves(test_board, 'o'))
        test_board = [
            ['o', None, 'x'],
            ['x', None, 'x'],
            [None, 'o', 'o'],
        ]
        expect = [
            x.Move(row=0, col=1, score=9),
            x.Move(row=1, col=1, score=-10),
            x.Move(row=2, col=0, score=-2),
        ]
        self.assertEqual(expect, x.rank_available_moves(test_board))
        test_board = [
            ['o', None, 'x'],
            ['x', None, 'x'],
            [None, 'o', 'o'],
        ]
        expect = [
            x.Move(row=0, col=1, score=-2),
            x.Move(row=1, col=1, score=10),
            x.Move(row=2, col=0, score=8),
        ]
        self.assertEqual(expect, x.rank_available_moves(test_board, 'o'))
        test_board = [
            ['x', None, None],
            [None, None, None],
            [None, None, None],
        ]
        # self.assertEqual([], x.rank_available_moves(test_board))


if __name__ == '__main__':
    unittest.main()
