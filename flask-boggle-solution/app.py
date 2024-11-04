from flask import Flask, render_template, request, session, jsonify
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

boggle_game = Boggle()

@app.route('/')
def show_board():
    """Show the boggle board. Initialize a new game."""
    board = boggle_game.make_board()
    session['board'] = board
    return render_template('board.html', board=board)

@app.route('/check-word', methods=['POST'])
def check_word():
    """Check if a word is a valid word in the dictionary and/or the boggle board"""
    word = request.json.get('word')
    board = session.get('board')
    result = boggle_game.check_valid_word(board, word)
    return jsonify({'result': result})

@app.route('/get-stats')
def get_stats():
    """
    Retrieve the number of games played and the high score.
    Returns the number of games played and the high score.
    """
    games_played = session.get('games_played', 0)
    high_score = session.get('high_score', 0)
    return jsonify({
        'games_played': games_played,
        'high_score': high_score
    })
    
@app.route('/set-board-size', methods=['POST'])
def set_board_size():
    size = request.json.get('size', 5)
    board = boggle_game.make_board(size)
    session['board'] = board
    return jsonify({'board': board})

@app.route('/hint', methods=['POST'])
def get_hint():
    """ Provide a hint by returning the first availabe letter of a valid word."""
    board = session.get('board')
    # Logic to find a hint goes here
    hint_word = boggle_game.find_word(board)
    hint_letter = hint_word[0] if hint_word else None
    return jsonify({'hint': hint_letter})


@app.route('/submit-score', methods=['POST'])
def submit_score():
    """ update and store game stats 
    Increment the number of games played and update the high score if necessary.
    """
    score = request.json.get('score')
    games_played = session.get('games_played', 0) + 1
    high_score = max(session.get('high_score', 0), score)
    
    session['games_played'] = games_played
    session['high_score'] = high_score
    
    return jsonify({
        'games_played': games_played,
        'high_score': high_score
    })
    
@app.route('/custom-board', methods=['POST'])
def custom_board():
    """
    Create a custom board of the specified size.
    """
    size = request.json.get('size', 5)
    board = boggle_game.make_board(size)
    session['board'] = board
    return render_template('board.html', board=board)

@app.route('/create-board', methods=['POST'])
def create_board():
    size = request.json.get('size', 5)
    board = boggle_game.make_board(size)
    session['board'] = board
    return jsonify({'board': board})


if __name__ == '__main__':
    app.run(debug=True)
