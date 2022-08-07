from boggle import Boggle
from flask import Flask, request, session, render_template, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = "peggyhill"
boggle_game = Boggle()
high_score = 0
times_played = 0

@app.route('/')
def show_start_screen():
    """shows the start screen with a button to direct the user to the page containing the game."""
    return render_template("start_screen.html")

@app.route('/game')
def display_board():
    """displays the page where the game is played and draws the board"""
    session['board'] = boggle_game.make_board()
    return render_template('game.html', game = session['board'])

@app.route('/check')
def check_guess():
    """receives the guess from the js file and checks whether it's valid, and returns a dictionary of the result and its status"""
    word = request.args["word"]
    board = session['board']
    result = boggle_game.check_valid_word(board, word)
    return jsonify({'result': result})

@app.route('/submitscore', methods=["POST"])
def post_scores():
    """receives score and # of games played and returns an updated value for the times played and an updated high
    score value if the player has indeed gotten a high score"""
    params = request.json['params']
    score = params['score']
    global times_played
    global high_score
    times_played = times_played + 1
    if score > high_score:
        high_score = score
    return jsonify({'highscore': high_score, 'timesplayed': times_played})
    