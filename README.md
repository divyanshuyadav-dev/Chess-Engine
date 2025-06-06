
# Chess Engine

A chess engine implementing core AI components like Minimax, Alpha-Beta pruning, and move evaluation.

---

## Features

* **Board Representation:** 8x8 matrix with standard chess piece encodings.
* **Move Generation:** Legal moves for all pieces including castling and promotion.
* **Evaluation Function:** Material-based score with Piece-Square Tables (PST) and positional heuristics.
* **Search Algorithm:** Minimax with Alpha-Beta pruning.
* **Optimizations:**

  * Move ordering using MVV-LVA heuristic
  * Pruning statistics tracking
  * Undo functionality for backtracking

---

## Requirements

* Python 3.8+
* No external dependencies (standard library only)

---

## How to Run

To play against the AI:

```bash
python main.py
```

To test Minimax and view pruning metrics:

```bash
python main.py
# Edit the `main()` function call near the bottom of the file
# Uncomment stats() function
# Comment play_game() function
```

---

## Example Input

During gameplay, enter moves in algebraic notation:

```
e2e4
g8f6
```

Enter `q` to quit.
