import chess
import chess.pgn
import networkx as nx
import matplotlib.pyplot as plt
import sys
import random

# Evaluation Function

def evaluate_board(board: chess.Board) -> int:
    '''
    Evaluates the board state and returns an evaluation score.
    A positive score means White is favored, while a negative score means Black is favored.

    This evaluation is based on material value, mobility, pawn structure, king safety, and piece positioning.
    '''
    # Define piece values
    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0  # King is invaluable but must be counted for completeness
    }

    # Initialize evaluation score
    evaluation = 0

    # Evaluate material on the board
    # Calculate the value of all pieces on the board based on piece values
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            value = piece_values[piece.piece_type]
            if piece.color == chess.WHITE:
                evaluation += value
            else:
                evaluation -= value

    # Mobility: count the number of legal moves for each player
    # Adding a bonus for having more legal moves (better mobility)
    white_mobility = len(list(board.legal_moves if board.turn else board.mirror().legal_moves))
    black_mobility = len(list(board.mirror().legal_moves if board.turn else board.legal_moves))
    evaluation += 0.1 * (white_mobility - black_mobility)

    # Pawn structure: penalize isolated and doubled pawns
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece and piece.piece_type == chess.PAWN:
            file = chess.square_file(square)
            color = piece.color
            # Penalize isolated pawns (no friendly pawns on adjacent files)
            if not any(
                    board.piece_at(chess.square(file, rank))
                    for rank in range(8)
                    if rank != chess.square_rank(square) and board.piece_at(chess.square(file, rank)) and board.piece_at(chess.square(file, rank)).piece_type == chess.PAWN and board.piece_at(chess.square(file, rank)).color == color
            ):
                evaluation -= 0.5 if color == chess.WHITE else -0.5
            # Penalize doubled pawns (two pawns on the same file)
            if sum(
                    1 for rank in range(8)
                    if board.piece_at(chess.square(file, rank)) and board.piece_at(chess.square(file, rank)).piece_type == chess.PAWN and board.piece_at(chess.square(file, rank)).color == color
            ) > 1:
                evaluation -= 0.25 if color == chess.WHITE else -0.25

    # Piece positioning: bonus for central control and advanced pawns
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            color = piece.color
            rank = chess.square_rank(square)
            file = chess.square_file(square)

            # Control of center (d4, d5, e4, e5 squares)
            if square in [chess.D4, chess.D5, chess.E4, chess.E5]:
                evaluation += 0.5 if color == chess.WHITE else -0.5

            # Bonus for advanced pawns (pawns that have moved further up the board)
            if piece.piece_type == chess.PAWN:
                if (color == chess.WHITE and rank >= 4) or (color == chess.BLACK and rank <= 3):
                    evaluation += 0.2 if color == chess.WHITE else -0.2

    # King safety: penalize open king positions and lack of pawn cover
    for color in [chess.WHITE, chess.BLACK]:
        king_square = board.king(color)
        if king_square is not None:
            king_rank = chess.square_rank(king_square)
            king_file = chess.square_file(king_square)
            pawn_cover = 0

            # Count pawns protecting the king
            for delta_file in [-1, 0, 1]:
                if 0 <= king_file + delta_file < 8:
                    if color == chess.WHITE and king_rank > 0:
                        square = chess.square(king_file + delta_file, king_rank - 1)
                        if board.piece_at(square) and board.piece_at(square).piece_type == chess.PAWN and board.piece_at(square).color == chess.WHITE:
                            pawn_cover += 1
                    elif color == chess.BLACK and king_rank < 7:
                        square = chess.square(king_file + delta_file, king_rank + 1)
                        if board.piece_at(square) and board.piece_at(square).piece_type == chess.PAWN and board.piece_at(square).color == chess.BLACK:
                            pawn_cover += 1

            # Penalize lack of pawn cover near the king
            if pawn_cover < 2:
                evaluation -= 1 if color == chess.WHITE else -1

    return evaluation

# Minimax Algorithm Implementation

def minimax(graph, node, depth, maximizing_player):
    # Base case: if at maximum depth or node has no children, return the evaluation
    if depth == 0 or graph.out_degree(node) == 0:
        return graph.nodes[node]['evaluation']

    if maximizing_player:
        # Maximizing player's turn (White)
        max_eval = float('-inf')
        for neighbor in graph.successors(node):
            eval = minimax(graph, neighbor, depth - 1, False)
            max_eval = max(max_eval, eval)
            graph.nodes[neighbor]['minimax'] = eval
        return max_eval
    else:
        # Minimizing player's turn (Black)
        min_eval = float('inf')
        for neighbor in graph.successors(node):
            eval = minimax(graph, neighbor, depth - 1, True)
            min_eval = min(min_eval, eval)
            graph.nodes[neighbor]['minimax'] = eval
        return min_eval

# Alpha-Beta Pruning Algorithm Implementation

def alphabeta(graph, node, depth, alpha, beta, maximizing_player):
    # Base case: if at maximum depth or node has no children, return the evaluation
    if depth == 0 or graph.out_degree(node) == 0:
        return graph.nodes[node]['evaluation']

    if maximizing_player:
        # Maximizing player's turn (White)
        max_eval = float('-inf')
        neighbors = list(graph.successors(node))  # Create a list to avoid modification during iteration
        for neighbor in neighbors:
            eval = alphabeta(graph, neighbor, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            graph.nodes[neighbor]['alphabeta'] = eval
            # Prune branches where beta <= alpha
            if beta <= alpha:
                # Remove edges that were not considered due to pruning
                edges_to_remove = [(node, n) for n in neighbors if n != neighbor]
                graph.remove_edges_from(edges_to_remove)
                break
        return max_eval
    else:
        # Minimizing player's turn (Black)
        min_eval = float('inf')
        neighbors = list(graph.successors(node))  # Create a list to avoid modification during iteration
        for neighbor in neighbors:
            eval = alphabeta(graph, neighbor, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            graph.nodes[neighbor]['alphabeta'] = eval
            # Prune branches where beta <= alpha
            if beta <= alpha:
                # Remove edges that were not considered due to pruning
                edges_to_remove = [(node, n) for n in neighbors if n != neighbor]
                graph.remove_edges_from(edges_to_remove)
                break
        return min_eval

# Generate Game Tree from Opening Sequence

def generate_game_tree(opening_moves, depth=4):  # Updated depth to 4 for clarity
    board = chess.Board()
    graph = nx.DiGraph()
    # Create the root node with the initial board state
    graph.add_node(0, fen=board.fen(), evaluation=evaluate_board(board))
    node_counter = 1

    # Apply opening moves
    for move in opening_moves:
        board.push(chess.Move.from_uci(move))
    graph.nodes[0]['fen'] = board.fen()

    # Generate game tree recursively
    def add_children(node, current_depth):
        nonlocal node_counter
        if current_depth >= depth:
            return

        legal_moves = list(board.legal_moves)
        random.shuffle(legal_moves)
        for move in legal_moves[:3]:  # Top 3 moves instead of 2 for better exploration
            board.push(move)
            graph.add_node(node_counter, fen=board.fen(), evaluation=evaluate_board(board))
            graph.add_edge(node, node_counter, move=move.uci())
            add_children(node_counter, current_depth + 1)
            board.pop()
            node_counter += 1

    add_children(0, 0)
    return graph

# Convert Graph to Tree-like Structure

def convert_to_tree(graph):
    tree = nx.DiGraph()
    root_node = 0
    tree.add_node(root_node, **graph.nodes[root_node])

    def add_to_tree(parent, node):
        for child in graph.successors(node):
            if child not in tree:
                tree.add_node(child, **graph.nodes[child])
                tree.add_edge(parent, child, **graph.edges[(node, child)])
                add_to_tree(child, child)

    add_to_tree(root_node, root_node)
    return tree

# Example Game Tree Printing

def print_example_game_tree():
    # Generate a random game tree for demonstration purposes
    graph = generate_game_tree(opening_moves=["d2d4", "d7d5", "c2c4", "e7e5"], depth=3)
    tree_graph = convert_to_tree(graph)
    print(nx.forest_str(tree_graph))  # Print the structure of the game tree
    for node in tree_graph.nodes():
        print(node, tree_graph.nodes[node].get("evaluation", "No evaluation"))  # Print node and its evaluation

# Draw the Game Tree

def draw_game_tree(graph, title="Game Tree with Minimax and Alpha-Beta Pruning"):
    # Generate positions for the nodes
    pos = nx.spring_layout(graph)
    # Labels for the edges representing the moves
    labels = {edge: graph.edges[edge]['move'] for edge in graph.edges}
    # Labels for nodes showing minimax values
    minimax_labels = {node: f"Minimax: {graph.nodes[node].get('minimax', '')}" for node in graph.nodes}
    # Labels for nodes showing alpha-beta values
    alpha_beta_labels = {node: f"AlphaBeta: {graph.nodes[node].get('alphabeta', '')}" for node in graph.nodes}

    # Draw the graph with node and edge labels
    plt.figure(figsize=(12, 8))
    nx.draw(graph, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=8)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels, font_color='red')
    nx.draw_networkx_labels(graph, pos, labels=minimax_labels, font_color='green', verticalalignment='bottom')
    nx.draw_networkx_labels(graph, pos, labels=alpha_beta_labels, font_color='purple', verticalalignment='top')
    plt.title(title)
    plt.show()

# Main function to run with command line argument 'draw'
if __name__ == "__main__":
    # Define the opening moves (e.g., Queen's Gambit Declined as default)
    opening_moves = ["d2d4", "d7d5", "c2c4", "e7e6"]
    # Generate the game tree from the given opening moves
    graph = generate_game_tree(opening_moves)

    # If 'draw' argument is provided, draw the game tree with minimax and alpha-beta pruning values
    if len(sys.argv) > 1 and sys.argv[1] == "draw":
        minimax(graph, 0, 4, True)  # Updated depth to 4
        alphabeta(graph, 0, 4, float('-inf'), float('inf'), True)  # Updated depth to 4
        # Extract the best move from the root node after running Minimax
        best_move = max(graph.successors(0), key=lambda n: graph.nodes[n].get('minimax', float('-inf')))
        best_move_notation = graph.edges[(0, best_move)]['move']
        draw_game_tree(graph, title=f"Game Tree with Minimax and Alpha-Beta Pruning (Best Move: {best_move_notation})")
    else:
        # Print the example game tree structure
        print_example_game_tree()
