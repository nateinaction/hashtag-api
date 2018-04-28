import sys
import random
from copy import deepcopy
from collections import namedtuple

Move = namedtuple('Move', ['row', 'col', 'score'])
BestMoves = namedtuple('BestMoves', ['score', 'moves'])


def select_next_move(board, human_player='x'):
    """
    Runs recursive function to rank available moves then returns the best move

    :param board: multidimensional array, game board
    :param human_player: token used by the human player
    :return: Move
    """
    ranked_available_moves = rank_available_moves(board, human_player)
    best_moves = find_best_moves(ranked_available_moves)
    return select_best_move(best_moves)


def rank_available_moves(board, human_player='x', recursive_level=0):
    """
    Recursive function to rank all available moves

    :param board: multidimensional array, game board
    :param human_player: token used by the human player
    :param recursive_level: depth of recursion
    :return: array of Move
    """
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
                    available_moves2 = rank_available_moves(new_board, human_player, recursive_level + 1)
                    if not available_moves2:
                        available_moves.append(Move(row=row_i, col=col_i, score=0 - recursive_level))
                    else:
                        best_move = find_best_moves(available_moves2)
                        available_moves.append(Move(row=row_i, col=col_i, score=best_move.score))

    return available_moves


def find_best_moves(available_moves):
    """
    Sorts available moves and returns array of equally ranked moves

    :param available_moves: array of Moves
    :return: BestMoves
    """
    best_moves = BestMoves(score=-sys.maxsize, moves=[])
    for move in available_moves:
        if best_moves.score < move.score:
            best_moves = BestMoves(score=move.score, moves=[move])
        elif best_moves.score == move.score:
            best_moves.moves.append(move)
    return best_moves


def select_best_move(best_moves, random_seed=None):
    """
    When given an array of equally ranked Moves, choose one.

    :param best_moves: array of Moves
    :param random_seed: optional seed for random method
    :return: Move
    """
    random.seed(random_seed)
    return random.choice(best_moves.moves)


def who_goes_next2(board):
    """
    Choose next piece to go based on current piece

    :param board: multidimensional array, game board
    :return: 'x' or 'o'
    """
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


def collate_possible_win_groups(board):
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
