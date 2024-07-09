from flask import Flask, render_template, request, redirect, url_for
from game_logic import *

app = Flask(__name__)

board = [['-', '-', '-'],
         ['-', '-', '-'],
         ['-', '-', '-']]

players = ['X', 'O']
current_player = None
game_over = False
vs_computer = False

@app.route('/')
def index():
    return render_template('index.html', board=board)

@app.route('/play', methods=['POST'])
def play():
    global current_player, vs_computer
    if request.form['mode'] == 'vs_computer':
        vs_computer = True
        current_player = random.choice(players)
    else:
        current_player = players[0]
    return redirect(url_for('game'))

@app.route('/game')
def game():
    global game_over
    game_over = False
    return render_template('index.html', board=board, current_player=current_player, vs_computer=vs_computer)

@app.route('/move', methods=['POST'])
def move():
    global current_player, game_over
    if request.method == 'POST':
        row = int(request.form['row'])
        col = int(request.form['col'])
        if board[row][col] == '-' and not game_over:
            board[row][col] = current_player
            winner = check_winner(board)
            if winner:
                game_over = True
                return render_template('result.html', winner=winner)
            elif all(board[row][col] != '-' for row in range(3) for col in range(3)):
                game_over = True
                return render_template('result.html', winner=None)
            else:
                if vs_computer:
                    current_player = get_next_player(current_player)
                    computer_move(board, current_player)
                else:
                    current_player = get_next_player(current_player)
    return redirect(url_for('game'))

if __name__ == '__main__':
    app.run(debug=True)
