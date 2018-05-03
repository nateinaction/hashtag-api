import os
import hashtag
from collections import defaultdict
from flask import Flask, request, abort, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['POST'])
def api():
    if not is_valid_request(request.json):
        abort(400, 'Invalid POST Request: Content-Type must be "application/json" '
                   'and json object should have a key called "board".')

    board = request.json.get('board')
    if not is_list_with_3_elements(board):
        abort(400, 'Invalid board: Board must be an array of length 3.')

    if not are_rows_valid(board):
        abort(400, 'Invalid rows: Rows must each be arrays with a length of 3.')

    if not are_tokens_valid(board):
        abort(400, 'Invalid tokens: Valid tokens are "x", "o" or null.')

    if not is_game_fair(board):
        abort(400, 'Unfair game: Tokens must not be played more than once per turn.')

    game_state = hashtag.get_game_state(board)
    return game_state_to_json(game_state)


def is_valid_request(json_obj):
    if not isinstance(json_obj, dict) or 'board' not in json_obj:
        return False

    return True


def is_list_with_3_elements(a_list):
    # Verify item is a list and has 3 elements
    if not isinstance(a_list, list) or len(a_list) != 3:
        return False

    return True


def are_rows_valid(board):
    for row in board:
        if not is_list_with_3_elements(row):
            return False

    return True


def are_tokens_valid(board):
    valid_tokens = [None, 'x', 'o']
    for token in board[0] + board[1] + board[2]:
        if token not in valid_tokens:
            return False

    return True


def is_game_fair(board):
    token_count = defaultdict(int)
    for token in board[0] + board[1] + board[2]:
        token_count[token] += 1

    # Verify tokens have not taken more turns than they're allotted
    x_count = token_count['x'] - token_count['o']
    if 1 < x_count or x_count < 0:
        return False

    return True


def game_state_to_json(game_state):
    next_move = None
    if game_state.best_next_move:
        next_move = {
            'row': game_state.best_next_move.row,
            'col': game_state.best_next_move.col,
        }

    return jsonify({
        'boardState': game_state.state,
        'token': game_state.token,
        'suggestedMove': next_move
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
