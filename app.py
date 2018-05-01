import os
import hashtag
from collections import defaultdict
from flask import Flask, request, abort, jsonify

app = Flask(__name__)


@app.route('/', methods=['POST'])
def api():
    if not is_valid_request(request.json):
        abort(400, 'POST should have Content-Type header set to application/json '
                   'and json object should have a valid board key')

    board = request.json.get('board')
    if not is_valid_board(board):
        abort(400, 'Invalid board. ex. [["x", null, null], ["x", "o", null], [null, null, null]]')

    next_move = hashtag.select_next_move(board)
    return jsonify({
        'row': next_move[0],
        'col': next_move[1],
    })


def is_valid_request(json_obj):
    if not json_obj:
        return False

    board = json_obj.get('board')
    human_player = json_obj.get('humanPlayer')
    if not board or not human_player:
        return False

    return True


def is_valid_board(board):
    # Verify board is a list
    if not isinstance(board, list):
        return False

    # Verify board has 3 rows
    if len(board) != 3:
        return False

    token_count = defaultdict(int)
    valid_tokens = [None, 'x', 'o']
    for row in board:
        # Verify row is a list
        if not isinstance(row, list):
            return False
        # Verify each row has 3 columns
        if len(row) != 3:
            return False
        for token in row:
            # Verify tokens are either None, 'x', or 'o'
            if token not in valid_tokens:
                return False
            token_count[token] += 1

    # Verify tokens have not taken more turns than they're allotted
    if 1 < abs(token_count['x'] - token_count['o']):
        return False

    return True


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
