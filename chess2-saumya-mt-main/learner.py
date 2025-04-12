import csv
import chess
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import pickle

def fen_to_features(fen):
    """
    Converts a FEN string to a feature vector suitable for machine learning.
    Encodes piece positions and whose turn it is.
    """
    board = chess.Board(fen)
    feature_vector = []

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

def load_dataset(filename):
    """
    Loads the dataset from a CSV file.
    """
    x = []  # Features
    y = []  # Targets
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            fen = row['fen']
            evaluation = float(row['eval'])
            features = fen_to_features(fen)
            x.append(features)
            y.append(evaluation)
    return x, y

def train_model(x_train, y_train, model_type):
    """
    Trains a regression model using the provided training data.
    """
    if model_type == "Linear":
        model = LinearRegression()
    elif model_type == "Ridge":
        model = Ridge()
    elif model_type == "Lasso":
        model = Lasso()
    elif model_type == "DecisionTree":
        model = DecisionTreeRegressor()
    elif model_type == "RandomForest":
        model = RandomForestRegressor()
    else:
        raise ValueError(f"Unsupported model type: {model_type}")

    model.fit(x_train, y_train)
    return model

def evaluate_model(model, x_test, y_test, model_type):
    """
    Evaluates the trained model on the test data and prints evaluation metrics.
    """
    y_pred = model.predict(x_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"[{model_type}] Mean Squared Error: {mse}")
    print(f"[{model_type}] R-squared: {r2}")
    return r2  # Higher is better

def save_model(model, filename):
    """
    Saves the trained model to a file using pickle.
    """
    with open(filename, "wb") as f:
        pickle.dump(model, f)
    print(f"Model saved to {filename}")

def main():
    # Load dataset
    x, y = load_dataset('chess_evaluations.csv')

    # Split dataset into training and testing sets
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    # Define the models to train
    model_types = ["Linear", "Ridge", "Lasso", "DecisionTree", "RandomForest"]

    # Track the best model and its performance
    best_model = None
    best_model_type = None
    best_performance = float('-inf')  # Initialize with the worst possible value

    # Train and evaluate each model
    for model_type in model_types:
        print(f"Training {model_type} model...")
        model = train_model(x_train, y_train, model_type)

        print(f"Evaluating {model_type} model...")
        performance = evaluate_model(model, x_test, y_test, model_type)

        # Update the best model if the current one is better
        if performance > best_performance:
            best_model = model
            best_model_type = model_type
            best_performance = performance

    # Save the best model
    if best_model:
        save_model(best_model, f"best_model_killbillV2_{best_model_type}.pkl")
        print(f"Best model: {best_model_type} with performance: {best_performance}")

if __name__ == "__main__":
    main()
