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

# Define the board as a 3x3 array
board = [['-', '-', '-'],
         ['-', '-', '-'],
         ['-', '-', '-']]

# Define the players as X and O
players = ['X', 'O']

# Choose the first player randomly
current_player = random.choice(players)

# Start the game loop
while True:

    # Display the board to the user
    print_board(board)

    # Get the user's move
    move = get_move(current_player, board)

    # Update the board with the user's move
    board[move[0]][move[1]] = current_player

    # Check if the game is over
    if check_winner(board):
        break

    # Switch players
    current_player = get_next_player(current_player)

# Display the winning message
winner = check_winner(board)
if winner:
    print(f"{winner} wins!")
else:
    print("The game is a tie.")
