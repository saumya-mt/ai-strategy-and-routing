import csv
import chess
import chess.engine
import random

def generate_game_final_position(engine, writer, start_itr, game_num, max_moves=5):
    board = chess.Board()
    itr = start_itr
    move_count = 0

    for move_num in range(1, max_moves + 1):
        legal_moves = list(board.legal_moves)
        if not legal_moves:
            reason = "No legal moves (Checkmate or Stalemate)"
            print(f"Game {game_num} completed at move {move_num} due to {reason}.")
            break  # Exit the move loop

        move = random.choice(legal_moves)
        board.push(move)
        move_count += 1

        if board.is_game_over():
            reason = board.result(claim_draw=True) if board.is_stalemate() or board.is_insufficient_material() else "Checkmate"
            print(f"Game {game_num} completed at move {move_num}: {reason}.")
            break

    # Evaluate the final position
    evaluation = evaluate_position(board, engine)
    if evaluation is not None:
        writer.writerow({'itr': itr, 'fen': board.fen(), 'eval': evaluation})
        itr += 1

    return itr, move_count


def evaluate_position(board, engine, depth=15):
    """
    Evaluates the current board position using the provided chess engine with a specified depth.

    :param board: The chess.Board object representing the current position.
    :param engine: The chess engine instance for evaluation.
    :param depth: The search depth for the engine analysis.
    :return: The evaluation score from the engine, or None if unavailable.
    """
    try:
        # Use depth-based limit instead of time-based
        result = engine.analyse(board, chess.engine.Limit(depth=depth))
        score = result['score'].relative
        depth_reached = result.get('depth', depth)  # Get actual depth reached, fallback to requested depth

        if score is not None:
            # Convert the score to centipawns; positive for White advantage, negative for Black
            eval_score = score.score(mate_score=10000)
            return eval_score
    except Exception as e:
        print(f"Error evaluating position: {e}")
    return None

def main():
    engine_path = "/opt/homebrew/bin/stockfish"  # Change this path to your Stockfish executable
    engine = chess.engine.SimpleEngine.popen_uci(engine_path)

    try:
        with open('chess_evaluations.csv', 'w', newline='') as csvfile:
            fieldnames = ['itr', 'fen', 'eval']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            total_iterations = 0
            num_games = 1000  # Number of separate games to generate
            max_moves_per_game = 5  # Define maximum moves per game

            for game_num in range(1, num_games + 1):
                itr, moves_made = generate_game_final_position(
                    engine, writer, total_iterations, game_num, max_moves=max_moves_per_game
                )
                total_iterations = itr
    finally:
        engine.quit()


if __name__ == "__main__":
    main()
