# Chess Engine

A Python chess engine and GUI built by following Eddie Sharick's "Chess Engine in Python" tutorial series, with additional custom features and bug fixes.

## Features

- Full legal move generation (including castling, en passant, pawn promotion)
- Automatic draw after 100 plies without a pawn move or capture (50-move rule)
- Depth-5 plies Negamax AI search with alpha-beta pruning
- Move ordering that prioritizes captures, pawn promotions, and castling
- Piece-square table evaluation for material and positional scoring

## Requirements

- Python 3.9+
- pygame

## Installation

1. Clone or download this repository.
2. (Recommended) Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Make sure the `images/` (piece icon) folder is present in the project root alongside `ChessMain.py` — the GUI loads piece sprites from there at startup.

## Running

From the project root:

```bash
python ChessMain.py
```

This launches the pygame window with the interactive chessboard.

## Game Modes

Player and AI control is configured in `ChessMain.py` using the `playerOne` and
`playerTwo` flags inside `main()`. Set the values as follows, then restart the
game:

| Mode | `playerOne` | `playerTwo` |
| --- | --- | --- |
| Human vs. AI (White) | `True` | `False` |
| AI vs. Human (Black) | `False` | `True` |
| Human vs. Human | `True` | `True` |
| AI vs. AI | `False` | `False` |

`playerOne` controls White and `playerTwo` controls Black. A value of `True`
enables mouse input for that side; a value of `False` lets the AI choose moves.

For example, to play as Black against the AI, update the configuration in
`ChessMain.py`:

```python
playerOne = False
playerTwo = True
```

## Controls

- **Left click**: select a square, then click a destination square to move
- **Z**: undo the last move
- **R**: reset/restart the game

## Project Structure

```
.
├── ChessMain.py       # Entry point, game loop, GUI/event handling
├── ChessEngine.py      # Board state, move generation, and chess rules
├── SmartMoveFinder.py  # AI search, move ordering, and board evaluation
├── images/             # Piece sprite images
└── requirements.txt
```

## Known Fixes Applied

- Corrected en passant capture direction bug
- Fixed double-multiplied piece-square table score
- Fixed undefined `drawEndGameText` reference
- Fixed mis-nested castling rights `elif` logic

## Credits

Based on [Eddie Sharick's Chess Engine tutorial series](https://www.youtube.com/c/EddieSharick) (YouTube).
