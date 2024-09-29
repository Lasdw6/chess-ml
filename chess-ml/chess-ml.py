import chess
import chess.engine
import random

# Initialize the chess board
board = chess.Board()

# Function to make a random legal move
def make_random_move(board):
    # Get all legal moves
    legal_moves = list(board.legal_moves)
    # Select a random move from the list of legal moves
    move = random.choice(legal_moves)
    # Push the move to the board
    board.push(move)

# Simulate a simple game with random moves until the game is over
while not board.is_game_over():
    print(board)  # Print the board
    print("\n")
    
    # Make a random move for white
    if board.turn == chess.WHITE:
        print("White's move:")
        make_random_move(board)
    # Make a random move for black
    else:
        print("Black's move:")
        make_random_move(board)

# Game over, print the result
result = board.result()
print("Game Over!")
print("Result:", result)
