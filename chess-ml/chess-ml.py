import pygame
import chess
import chess.engine
import threading

# Constants
WIDTH, HEIGHT = 800, 800
SQUARE_SIZE = WIDTH // 8
FPS = 60

# Colors
LIGHT_SQUARE_COLOR = (222, 184, 135)
DARK_SQUARE_COLOR = (165, 105, 48)
SELECTED_SQUARE_COLOR = (0, 255, 0)
LEGAL_MOVE_COLOR = (0, 0, 255)

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")
clock = pygame.time.Clock()

# Load Stockfish engine
engine_path = "C:/Users/vivid/Downloads/stockfish-windows-x86-64-avx2/stockfish/stockfish.exe"
engine = chess.engine.SimpleEngine.popen_uci(engine_path)

# Initialize board
board = chess.Board()

# Load piece images
pieces = {}
piece_names = {
    'p': 'black-pawn.png', 'P': 'white-pawn.png',
    'r': 'black-rook.png', 'R': 'white-rook.png',
    'n': 'black-knight.png', 'N': 'white-knight.png',
    'b': 'black-bishop.png', 'B': 'white-bishop.png',
    'q': 'black-queen.png', 'Q': 'white-queen.png',
    'k': 'black-king.png', 'K': 'white-king.png'
}

for piece, filename in piece_names.items():
    pieces[piece] = pygame.image.load(f"pieces/{filename}")
    pieces[piece] = pygame.transform.scale(pieces[piece], (SQUARE_SIZE, SQUARE_SIZE))

def draw_board(selected_square=None, legal_moves=None):
    for rank in range(8):
        for file in range(8):
            color = LIGHT_SQUARE_COLOR if (rank + file) % 2 == 0 else DARK_SQUARE_COLOR
            pygame.draw.rect(screen, color, pygame.Rect(file * SQUARE_SIZE, rank * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            # Draw selected square highlight
            if selected_square and (rank, file) == selected_square:
                pygame.draw.rect(screen, SELECTED_SQUARE_COLOR, pygame.Rect(file * SQUARE_SIZE, rank * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)

            # Highlight legal moves
            if legal_moves and chess.square(file, 7 - rank) in legal_moves:  # Corrected for display
                pygame.draw.rect(screen, LEGAL_MOVE_COLOR, pygame.Rect(file * SQUARE_SIZE, rank * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)

    # Draw pieces
    for square in range(64):
        piece = board.piece_at(square)
        if piece:
            piece_image = pieces[piece.symbol()]  # Use the symbol directly to access the piece
            file, rank = chess.square_file(square), chess.square_rank(square)
            screen.blit(piece_image, (file * SQUARE_SIZE, (7 - rank) * SQUARE_SIZE))  # Flip rank for display

def analyze_position():
    # Get Stockfish evaluation
    info = engine.analyse(board, chess.engine.Limit(time=2.0))

    # Extract the relative score
    score = info["score"].relative

    if score.is_mate():  # Handle mate scenarios
        if score.mate() > 0:
            print("Stockfish evaluation: White has a forced mate in", score.mate(), "moves.")
        else:
            print("Stockfish evaluation: Black has a forced mate in", abs(score.mate()), "moves.")
    else:
        centipawn_score = score.score()
        print(f"Stockfish evaluation: {centipawn_score / 100:.2f}")
        
def main():
    selected_square = None
    legal_moves = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                engine.quit()
                pygame.quit()
                return
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                x, y = event.pos
                file, rank = x // SQUARE_SIZE, 7 - (y // SQUARE_SIZE)  # Convert to board coordinates
                clicked_square = chess.square(file, rank)

                if selected_square is None:
                    # Check if the clicked square has a piece of the current turn
                    if board.piece_at(clicked_square) is not None and board.color_at(clicked_square) == board.turn:
                        selected_square = clicked_square
                        legal_moves = [move.to_square for move in board.legal_moves if move.from_square == selected_square]  # Get legal moves for selected piece
                else:
                    move = chess.Move(selected_square, clicked_square)
                    if move in board.legal_moves:  # Validate move
                        board.push(move)  # Execute the move
                        selected_square = None
                        legal_moves = []  # Clear legal moves after executing a move

                        # Start analysis in a separate thread
                        threading.Thread(target=analyze_position, daemon=True).start()

                    else:
                        selected_square = None  # Deselect if illegal move
                        legal_moves = []  # Clear legal moves

        screen.fill((0, 0, 0))  # Clear screen
        draw_board(selected_square, legal_moves)  # Draw board and pieces
        pygame.display.flip()  # Update display
        clock.tick(FPS)  # Maintain frame rate

if __name__ == "__main__":
    main()
