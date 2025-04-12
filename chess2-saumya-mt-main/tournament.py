from chester.timecontrol import TimeControl
from chester.tournament import play_tournament

# Each string is the name/path to an executable UCI engine.
players = ["random_chess_bot.exe", "/opt/homebrew/bin/stockfish"]

# Specify time and increment, both in seconds.
time_control = TimeControl(initial_time=180, increment=10)

# Play each math-up twice.
n_games = 5

# Tabulate scores at the end.
scores = {}

for pgn in play_tournament(
    players,
    time_control,
    n_games=n_games,
    repeat=True,  # Each opening played twice,
):
    # Printing out the game result.
    pgn.headers["Event"] = "CS5100 Tournament"
    pgn.headers["Site"] = "My Computer"
    print(pgn, "\n")

    # Update scores.
    white = pgn.headers["White"]
    black = pgn.headers["Black"]
    scores.setdefault(white,0) # If bot hasn't been added start at 0.
    scores.setdefault(black,0)
    results = pgn.headers["Result"].split('-')
    scores[white] += float(eval(results[0]))
    scores[black] += float(eval(results[1]))

for (bot,score) in scores.items():
    print(bot , ":", score)