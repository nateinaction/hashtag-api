import sys
import random
from copy import deepcopy
from collections import namedtuple

Move = namedtuple('Move', ['row', 'col', 'score'])
SortedMoves = namedtuple('SortedMoves', ['score', 'moves'])


def select_next_move(board, seed=None):
    """
    Runs recursive function to rank available moves then returns the best move

    :param board: multidimensional array, game board
    :param seed: optional token to fix the random method
    :return: Move
    """
    if is_first_two_moves(board):
        return select_first_two_moves(board, seed)

    human_player = 'o' if get_current_turn(board) == 'x' else 'x'
    # if all available moves are losing moves, choose most negatively scored move
    ranked_moves = rank_available_moves(board, human_player)
    if are_all_losing_moves(ranked_moves):
        sorted_moves = minimize_moves(ranked_moves)
    else:
        sorted_moves = maximize_moves(ranked_moves)
    return select_sorted_move(sorted_moves, seed)


def is_first_two_moves(board):
    joined_board = board[0] + board[1] + board[2]
    return joined_board.count(None) > 7


def select_first_two_moves(board, seed=None):
    # if all corners are free, pick a corner else pick center
    corners = [
        board[0][0],
        board[0][2],
        board[2][0],
        board[2][2],
    ]
    if corners.count(None) == 4:
        sorted_moves = SortedMoves(
            score=0,
            moves=[
                Move(row=0, col=0, score=0),
                Move(row=0, col=2, score=0),
                Move(row=2, col=0, score=0),
                Move(row=2, col=2, score=0),
            ],
        )
    else:
        sorted_moves = SortedMoves(score=0, moves=[Move(row=1, col=1, score=0)])

    return select_sorted_move(sorted_moves, seed)


def rank_available_moves(board, human_player='x', recursive_level=0):
    """
    Recursive function to rank all available moves

    :param board: multidimensional array, game board
    :param human_player: token used by the human player
    :param recursive_level: depth of recursion
    :return: array of Move
    """
    available_moves = []

    # find who's turn it is
    current_turn = get_current_turn(board)
    if not current_turn:
        return available_moves

    # go through each empty space and find available moves
    for row_i in range(3):
        for col_i in range(3):
            new_board = board.copy()
            if not new_board[row_i][col_i]:
                new_board = deepcopy(board)
                new_board[row_i][col_i] = current_turn
                possible_win_groups = collate_possible_win_groups(new_board)
                winner = find_winner(possible_win_groups)
                if winner == human_player:
                    available_moves.append(Move(row=row_i, col=col_i, score=-10 - recursive_level))
                elif winner != human_player and winner is not None:
                    available_moves.append(Move(row=row_i, col=col_i, score=10 - recursive_level))
                else:
                    recursed_moves = rank_available_moves(new_board, human_player, recursive_level + 1)
                    if not recursed_moves:
                        available_moves.append(Move(row=row_i, col=col_i, score=0 - recursive_level))
                    else:
                        if current_turn == human_player:
                            sorted_moves = minimize_moves(recursed_moves)
                        else:
                            sorted_moves = maximize_moves(recursed_moves)
                        available_moves.append(Move(row=row_i, col=col_i, score=sorted_moves.score - recursive_level))

    return available_moves


def maximize_moves(available_moves):
    def max_min_func(sorted_moves, move): return sorted_moves.score < move.score
    default_score = -sys.maxsize
    return max_min_moves(available_moves, max_min_func, default_score)


def minimize_moves(available_moves):
    def max_min_func(sorted_moves, move): return sorted_moves.score > move.score
    default_score = sys.maxsize
    return max_min_moves(available_moves, max_min_func, default_score)


def max_min_moves(available_moves, max_min_func, default_score):
    """
    Sorts available moves and returns array of equally ranked moves

    :param available_moves: array of Moves
    :param max_min_func:
    :param default_score:
    :return: SortedMoves
    """
    sorted_moves = SortedMoves(score=default_score, moves=[])
    for move in available_moves:
        if max_min_func(sorted_moves, move):
            sorted_moves = SortedMoves(score=move.score, moves=[move])
        elif sorted_moves.score == move.score:
            sorted_moves.moves.append(move)
    return sorted_moves


def select_sorted_move(sorted_moves, random_seed=None):
    """
    When given an array of equally ranked Moves, choose one.

    :param sorted_moves: array of Moves
    :param random_seed: optional seed for random method
    :return: Move
    """
    if not sorted_moves.moves:
        return None

    random.seed(random_seed)
    return random.choice(sorted_moves.moves)


def are_all_losing_moves(available_moves):
    for move in available_moves:
        if move.score > -10:
            return False
    return True


def get_current_turn(board):
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


if __name__ == '__main__':
    pass

