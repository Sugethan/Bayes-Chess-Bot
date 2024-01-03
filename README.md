Simple chess bot program using Bayesian Inferences. If you give it a game in PGN format and a database (collection of PGN files with at least a game per file), it will :

1) Find all the games in the database that have the exact same opening
2) Among those games, it will select all the games where all the moves from your game have been played (without caring for the order in which they have been played).
3) Return the move with the highest probability of victory based on the selected games

Used Libraries :

- Os (https://github.com/python/cpython/blob/3.12/Lib/os.py)
- Python Chess (https://github.com/python/cpython/blob/3.12/Lib/os.py)