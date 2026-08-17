# Chess Engine

A Python chess engine and GUI built by following Eddie Sharick's "Chess Engine in Python" tutorial series, with additional custom features and bug fixes.

## Features

- Full legal move generation (including castling, en passant, pawn promotion)
- Threefold repetition detection
- 50-move rule
- Insufficient material draw detection
- Tapered piece-square tables (including king PST) for evaluation
- Simple chess AI opponent using minimax/negamax with alpha-beta pruning (per the tutorial series)

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

## Controls

- **Left click**: select a square, then click a destination square to move
- **Z**: undo the last move
- **R**: reset/restart the game

## Project Structure

```
.
├── ChessMain.py       # Entry point, game loop, GUI/event handling
├── ChessEngine.py      # Board state, move generation, rules (repetition, 50-move, insufficient material)
├── ChessAI.py           # AI move search (minimax/negamax + PSTs, alpha-beta pruning)
├── images/                    # Piece sprite images
└── requirements.txt
```

> Note: adjust file names above to match your actual filenames if they differ — this reflects the structure used in Eddie Sharick's tutorial series.

## Known Fixes Applied

- Corrected en passant capture direction bug
- Fixed double-multiplied piece-square table score
- Fixed undefined `drawEndGameText` reference
- Fixed mis-nested castling rights `elif` logic

## Credits

Based on [Eddie Sharick's Chess Engine tutorial series](https://www.youtube.com/c/EddieSharick) (YouTube).
