[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-2972f46106e565e64193e422d61a12cf1da4916b45550586e14ef0a7c637dd04.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=17172865)
# Homework - Learning Chess ♔♕♗♘♙♖

Topics: Machine Learning

For this assignment you will be tranining a new chessbot that uses learning. You do not need to program the rules of chess in order to complete this assignment.

## Part 0 - Pre-req

On top of the libraries that we used in the earlier chess assignment, you will need one more.

* scikit-learn - [https://scikit-learn.org/](https://scikit-learn.org/) a library containing many pre-built learning models. Install with the command `pip install -U scikit-learn`

## Part 1 -Instructions

This assignment is meant to ensure that you:

* Understand various models in machine learning
* Can program an agent to uses learning
* Experience evaluating different learning algorithms
* Can argue for chosing one regression model over another in different contexts

In order to test your agent, you'll need Stockfish [https://stockfishchess.org/](https://stockfishchess.org/). This is because you will use Stockfish as training data for your own brand new agent. Your new agent will apply various learning models to create an evaluation function that will replace the more traditional-type of evaluation functions that we used in the earlier assignment.

You are tasked to:

0. Generate thousands of games using [fen_generator.py](fen_generator.py) which you will need to update to include the Path to Stockfish.
1. Apply [learner.py](learner.py) on your training data.
2. Use serialization [https://saturncloud.io/blog/sklearn-how-to-save-a-model-created-from-a-pipeline-and-gridsearchcv-using-joblib-or-pickle/#saving-a-model](https://saturncloud.io/blog/sklearn-how-to-save-a-model-created-from-a-pipeline-and-gridsearchcv-using-joblib-or-pickle/#saving-a-model) to save your learned model so that you do not have to re-train it. **Important** do *NOT* name your model files along the lines of 'mymodle.pkl' because others might use the same name and then we won't be able to run your agent.
3. You will need to try at least four (4) different kinds of regression models and compare their results. The types of learning models are up to you but the teaching team might recommend Linear, Ridge, Lasso, Support Vector Machines, Decision Trees, Forests, or a Boosting method.
4. Create a new version of your earlier chessbot that replaces the evaluation function with one provided by your trained model. Come up with a updated name for this bot that differentiates it from your first one. Using your name, or NEU id, as the name of your bot will be an *automatic zero* for the assignment.
5. Your new agent does **not** have to beat the random chessbot.


Ensure that your new chessbot follows normal PyDoc specs for documentation and readability.

---
***Important Change***

The way that [fen_generator.py](fen_generator.py) works is by creating a random board position and then evaluating that board. This means that it really can't learn about small changes to input impacting the output. Imagine going to a random page in a Physics textbook and trying to understand it, then going to a random page in a Music texbook and doing the same, then going to a Turkish texbook and so on. What if you instead start at the first page and read that, then go to the next page then the next one? Consider changing the generation to instead evaluate the board after every individual move. This way your bot can start to learn trends from move-to-move rather than just completely different games.

---


## Part 2 - Report

Create a Jupyter notebook report that:

* Details the kinds of learning models that you used
* Displays the results of your test tournaments and performance metrics (including learning performance) as visuals such as charts, graphs, and plots (just text or limited visuals will not earn credit)
* Explains what these results mean
* Justifies why you beleive that the learning models you selected performed the way they did
* Identifies which .pkl file is yours so that we can include that along with your new agent in the class tournament
* Include answers to the following Reflection Questions:

1. Describe your experiences using these models. What things did you learn? What aspects were a challenge?
2. There is an issue with the training data, it doesn't include forced mate as an evaluation. This is because if you ran the code:

  ```python
  # assuming engine set to stockfish
  board = chess.Board("r1bqkbnr/p1pp1ppp/1pn5/4p3/2B1P3/5Q2/PPPP1PPP/RNB1K1NR w KQkq - 2 4")
  info = engine.analyse(board, chess.engine.Limit(depth=20))
  print("Score:", info['score'])
  print("Score:", info["score"].relative.score())
  ```
  
  It outputs:

  ```text
  Score: PovScore(Mate(+1), WHITE)
  Score: None
  ```

  This is because Mate-In-1 doesn't reflect well as a floating point number that the example learning model expected. Describe how you would fix this issue. If you actually did implement this fix, did it improve the performance of your bot?

3. You'll notice that in the prior example the engine was limited by depth instead of time. Which approach is better and why?
4. These board fens that it learned from were randomly generated, but, would it be better if instead instead your bot learned from games played by strong bots? Why or why not?
5. If a human learned how to play chess by playing against Stockfish, would they begin to play like Stockfish? Explain why you feel this is or isn't the case.
6. (Optional) What did you think of this homework? Challenging? Difficult? Fun? Worth-while? Useful? Etc.?