import unittest
import sys
import random
from copy import deepcopy
from collections import namedtuple

Move = namedtuple('Move', ['row', 'col', 'score'])
BestMoves = namedtuple('BestMoves', ['score', 'moves'])


def x(arr):
    pass


def select_next_move(board, human_player='x'):
    ranked_available_moves = rank_available_moves(board, human_player)
    best_moves = find_best_moves(ranked_available_moves)
    return select_best_move(best_moves)


def rank_available_moves(board, human_player='x', recursive_level=0):
    # find which player goes next in the game
    next_player = who_goes_next2(board)
    if not next_player:
        return []

    # go through each empty space and find available moves
    available_moves = []
    for row_i in range(3):
        for col_i in range(3):
            new_board = board.copy()
            if not new_board[row_i][col_i]:
                new_board = deepcopy(board)
                new_board[row_i][col_i] = next_player
                winner = find_winner(new_board)
                if winner == human_player:
                    available_moves.append(Move(row=row_i, col=col_i, score=-10 - recursive_level))
                elif winner != human_player and winner is not None:
                    available_moves.append(Move(row=row_i, col=col_i, score=10 - recursive_level))
                else:
                    # not finished
                    available_moves2 = rank_available_moves(new_board, human_player, recursive_level + 1)
                    if not available_moves2:
                        available_moves.append(Move(row=row_i, col=col_i, score=0 - recursive_level))
                    else:
                        best_move = find_best_moves(available_moves2)
                        available_moves.append(Move(row=row_i, col=col_i, score=best_move.score))

    return available_moves


def find_best_moves(available_moves):
    best_moves = BestMoves(score=-sys.maxsize, moves=[])
    for move in available_moves:
        if best_moves.score < move.score:
            best_moves = BestMoves(score=move.score, moves=[move])
        elif best_moves.score == move.score:
            best_moves.moves.append(move)
    return best_moves


def select_best_move(best_moves, random_seed=None):
    random.seed(random_seed)
    return random.choice(best_moves.moves)


def who_goes_next2(board):
    joined_board = []
    for row in board:
        joined_board += row
    num_none = joined_board.count(None)
    if num_none == 0:
        return None
    return 'o' if num_none % 2 == 0 else 'x'


def who_goes_next(piece):
    """
    Choose next piece to go based on current piece

    :param piece: None, 'x' or 'o'
    :return: 'x' or 'o'
    """
    if piece != 'x' and piece != 'o':
        return 'x'
    return 'x' if piece == 'o' else 'o'


def possible_win_groups(board):
    """
    All of the possible groups that could win the game

    :param board: tic-tac-toe matrix
    :return: matrix of all possible winning groups
    """
    return [
        board[0],
        board[1],
        board[2],
        [board[i][0] for i in range(3)],
        [board[i][1] for i in range(3)],
        [board[i][2] for i in range(3)],
        [board[i][i] for i in range(3)],
        [board[i][2 - i] for i in range(3)],
    ]


def find_winner(possible_win_groups):
    """
    Check matrix of win groups to see if 'x' or 'o' occur 3 times

    :param possible_win_groups:
    :return:
    """
    for possible_win in possible_win_groups:
        if possible_win.count('x') == 3:
            return 'x'
        if possible_win.count('o') == 3:
            return 'o'
    return None


class TestMe(unittest.TestCase):
    def test_who_won(self):
        self.assertEqual(find_winner([[None, None, None]]), None)
        self.assertEqual(find_winner([['x', None, 'x']]), None)
        self.assertEqual(find_winner([['y', 'y', 'y']]), None)
        self.assertEqual(find_winner([['x', None, 'x', 'x', 'x']]), None)
        self.assertEqual(find_winner([['x', 'x']]), None)
        self.assertEqual(find_winner([['x', 'x', 'o']]), None)
        self.assertEqual(find_winner([['x', 'x', 'x']]), 'x')
        self.assertEqual(find_winner([['o', 'o', 'o']]), 'o')
        self.assertEqual(find_winner([['x', None, 'x', 'x']]), 'x')
        self.assertEqual(find_winner([['x', 'x', 'x'], ['x', 'x', 'o']]), 'x')
        self.assertEqual(find_winner([[None, None, None], ['x', 'x', 'x']]), 'x')

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
        self.assertEqual(expect, possible_win_groups(input_board))

    def test_who_goes_next(self):
        self.assertEqual('x', who_goes_next(None))
        self.assertEqual('x', who_goes_next('o'))
        self.assertEqual('o', who_goes_next('x'))
        self.assertEqual('x', who_goes_next(123))

    def test_who_goes_next2(self):
        self.assertEqual('x', who_goes_next2([[None, None, None], [None, None, None], [None, None, None]]))
        self.assertEqual('o', who_goes_next2([['x', None, None], [None, None, None], [None, None, None]]))
        self.assertEqual('x', who_goes_next2([['x', 'o', None], [None, None, None], [None, None, None]]))
        self.assertEqual('x', who_goes_next2([['x', 'x', None], [None, None, None], [None, None, None]]))
        self.assertEqual(None, who_goes_next2([['x', 'x', 'x']]))

    def test_find_best_moves(self):
        available_moves = [
            Move(row=0, col=1, score=-16),
            Move(row=1, col=2, score=6),
            Move(row=2, col=1, score=-1),
            Move(row=2, col=2, score=1),
            Move(row=2, col=2, score=6),
        ]
        expected_best_moves = BestMoves(
            score=6,
            moves=[
                Move(row=1, col=2, score=6),
                Move(row=2, col=2, score=6),
            ]
        )
        self.assertEqual(expected_best_moves, find_best_moves(available_moves))
        available_moves = [Move(row=2, col=0, score=-2)]
        expected_best_moves = BestMoves(
            score=-2,
            moves=[Move(row=2, col=0, score=-2)]
        )
        self.assertEqual(expected_best_moves, find_best_moves(available_moves))

    def test_select_best_move(self):
        seed = 0
        best_moves = BestMoves(
            score=6,
            moves=[
                Move(row=1, col=2, score=6),
                Move(row=2, col=2, score=6),
            ],
        )
        expect = Move(row=2, col=2, score=6)
        self.assertEqual(expect, select_best_move(best_moves, seed))
        best_moves = BestMoves(
            score=-2,
            moves=[
                Move(row=2, col=0, score=-2),
            ],
        )
        expect = Move(row=2, col=0, score=-2)
        self.assertEqual(expect, select_best_move(best_moves, seed))

    def test_rank_available_moves(self):
        test_board = [
            ['x', 'o', 'x'],
            ['o', 'x', 'o'],
            ['o', 'x', None],
        ]
        self.assertEqual([Move(row=2, col=2, score=0)], rank_available_moves(test_board),
                         "No win scenario should return None")
        test_board = [
            ['o', 'x', 'o'],
            ['x', None, 'x'],
            ['o', 'x', 'o'],
        ]
        self.assertEqual([Move(row=1, col=1, score=-10)], rank_available_moves(test_board))
        test_board = [
            [None, 'x', 'x'],
            ['x', None, 'x'],
            ['x', 'x', None],
        ]
        self.assertEqual([Move(row=0, col=0, score=10), Move(row=1, col=1, score=10), Move(row=2, col=2, score=10)], rank_available_moves(test_board, 'o'))
        test_board = [
            ['o', None, 'x'],
            ['x', None, 'x'],
            [None, 'o', 'o'],
        ]
        expect = [
            Move(row=0, col=1, score=9),
            Move(row=1, col=1, score=-10),
            Move(row=2, col=0, score=-2),
        ]
        self.assertEqual(expect, rank_available_moves(test_board))
        test_board = [
            ['o', None, 'x'],
            ['x', None, 'x'],
            [None, 'o', 'o'],
        ]
        expect = [
            Move(row=0, col=1, score=-2),
            Move(row=1, col=1, score=10),
            Move(row=2, col=0, score=8),
        ]
        self.assertEqual(expect, rank_available_moves(test_board, 'o'))
        test_board = [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ]
        self.assertEqual([], rank_available_moves(test_board))


if __name__ == '__main__':
    unittest.main()
