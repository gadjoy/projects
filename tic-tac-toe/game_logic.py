import random

# Define a function to print the board to the user
def print_board(board):
    for row in board:
        print(' | '.join(row))

# Define a function to get the user's move
def get_move(player, board):
    while True:
        move = input("Enter your move (1-9): ")
        move = int(move) - 1
        if 0 <= move < 9 and board[move // 3][move % 3] == '-':
            break
    return [move // 3, move % 3]

# Define a function to check if there is a winner
def check_winner(board):
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] != '-':
            return board[row][0]
        if board[0][row] == board[1][row] == board[2][row] != '-':
            return board[0][row]
    if board[0][0] == board[1][1] == board[2][2] != '-':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != '-':
        return board[0][2]
    return None

# Define a function to get the next player
def get_next_player(current_player):
    return 'O' if current_player == 'X' else 'X'

# Define a function to simulate computer move
def computer_move(board, player):
    while True:
        move = random.randint(0, 8)
        if board[move // 3][move % 3] == '-':
            return [move // 3, move % 3]
