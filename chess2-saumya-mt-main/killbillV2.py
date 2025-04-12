#!/usr/bin/env python
import chess
import sys
import pickle

# Load the trained model
def load_model(filename="best_model_killbillV2_Lasso.pkl"):
    try:
        with open(filename, "rb") as f:
            model = pickle.load(f)
        print(f"Loaded model from {filename}")
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        sys.exit(1)

# Convert FEN to features for the model
def fen_to_features(fen):
    """
    Converts a FEN string to a feature vector suitable for the model.
    """
    board = chess.Board(fen)
    feature_vector = []

    try:
        piece_map = board.piece_map()
        for square in chess.SQUARES:
            piece = piece_map.get(square)
            if piece:
                piece_type = piece.piece_type
                piece_color = piece.color
                # Encode piece type (1-6) and color (1 for white, 2 for black)
                feature_vector.append((piece_type, 1 if piece_color else 2))
            else:
                feature_vector.append((0, 0))
        # Flatten the feature vector
        feature_vector_flat = [val for sublist in feature_vector for val in sublist]
        # Include whose turn it is (0 for white's turn, 1 for black's turn)
        turn_feature = 0 if board.turn == chess.WHITE else 1
        feature_vector_flat.append(turn_feature)
        return feature_vector_flat
    except Exception as e:
        print(f"Error in fen_to_features: {e}")
        return []

# Evaluate a board position using the model
def evaluate_board(board, model):
    """
    Evaluates the board state using the model.
    """
    try:
        fen = board.fen()  # Get FEN representation of the board
        features = fen_to_features(fen)  # Convert FEN to features
        if not features:
            raise ValueError("Feature extraction failed.")
        evaluation = model.predict([features])[0]  # Predict using the model
        return evaluation
    except Exception as e:
        print(f"Error in evaluate_board: {e}")
        return float('-inf') if board.turn == chess.WHITE else float('inf')

# Select the best move based on evaluation
def make_best_move(board, model):
    '''Returns the best move based on the model evaluation'''
    legal_moves = list(board.legal_moves)
    if not legal_moves:
        print("No legal moves available. Game might be over.")
        return None

    best_move = None
    is_white_turn = board.turn  # Snapshot of turn state
    best_evaluation = float('-inf') if is_white_turn else float('inf')

    print("Evaluating moves...")
    for move in legal_moves:
        board.push(move)
        try:
            evaluation = evaluate_board(board, model)
            if evaluation is None:
                print(f"Move {move.uci()} skipped: Evaluation returned None.")
                board.pop()
                continue  # Skip moves with evaluation errors
        except Exception as e:
            print(f"Error evaluating move {move.uci()}: {e}")
            board.pop()
            continue

        print(f"Move: {move.uci()}, Evaluation: {evaluation}")

        # Update the best move based on the current player's turn
        if (is_white_turn and evaluation > best_evaluation) or \
                (not is_white_turn and evaluation < best_evaluation):
            print(f"Updating best move: {move.uci()} (Evaluation: {evaluation})")
            best_move = move
            best_evaluation = evaluation

        board.pop()

    if best_move:
        print(f"Selected best move: {best_move.uci()} with evaluation {best_evaluation}")
    else:
        print("No valid best move found.")
    return best_move




# Load the model
model = load_model("best_model_killbillV2_Lasso.pkl")

board = chess.Board()

def uci(msg: str):
    '''Processes UCI commands with the internal board state'''
    if msg == "uci":
        print("id name Chess Bot")
        print("id author Your Name")
        print("uciok")
    elif msg == "isready":
        print("readyok")
    elif msg.startswith("position startpos moves"):
        board.clear()
        board.set_fen(chess.STARTING_FEN)
        moves = msg.split()[3:]
        for move in moves:
            board.push(chess.Move.from_uci(move))
    elif msg.startswith("position fen"):
        fen = msg.removeprefix("position fen ")
        board.set_fen(fen)
    elif msg.startswith("go"):
        move = make_best_move(board, model)  # Fix: Include 'board' as an argument
        if move:
            print(f"bestmove {move.uci()}")
        else:
            print("bestmove (none)")
    elif msg == "quit":
        sys.exit(0)
    else:
        print(f"Unknown command: {msg}")


def main():
    '''Main loop to process UCI commands'''
    try:
        while True:
            uci(input())
    except Exception as e:
        print(f"Fatal Error: {e}")

if __name__ == "__main__":
    main()
