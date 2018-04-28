from flask import Flask, request

app = Flask(__name__)


@app.route('/tic-tac-toe/next-move')
def poke():
    board = request.args.get('board')
    human_player = request.args.get('human-player')
    if board and human_player:
        if is_valid_board(board):
            if is_valid_player(human_player):
                pass
            else:
                return 'Invalid human player token. Try "x" or "o"', 401
        else:
            return 'Invalid board. ex. [["x", "o", None], ["x", None, None], [None, None, None]]', 401
    return 'No board or human player token provided. Correct request includes ?board=...&human-player=...', 401


def is_valid_board(board):
    if not board:
        return False
    if len(board) != 3:
        return False

    valid_tokens = [None, 'x', 'o']
    for row in board:
        if len(row) != 3:
            return False
        for token in row:
            if token not in valid_tokens:
                return False

    return True


def is_valid_player(player_token):
    valid_tokens = ['x', 'o']
    if player_token not in valid_tokens:
        return False
    return True
