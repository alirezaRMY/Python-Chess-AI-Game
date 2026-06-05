# ♟️ Python Chess AI Game

A fully functional chess game built with Python and Pygame, featuring three game modes and a custom-built AI engine. Developed as a bachelor's degree final project by **Alireza Ramyad**.

---

## 🎮 Game Modes

| Mode | Description |
|------|-------------|
| **Player vs Player** | Two humans play on the same computer |
| **Player vs AI** | You challenge the chess AI engine |
| **AI vs AI** | Watch two AI engines play each other (tutorial/demo mode) |

---

## ⬇️ Download & Run (No Python Required)

You do **not** need Python or any other software installed on your computer.

1. Download the latest release from the [Releases page](https://github.com/alirezaRMY/Python-Chess-AI-Game/releases/latest)
2. Extract / copy the **Chess** folder to your computer
3. Open the folder: `Chess` → `Chess`
4. Scroll down and find the **application file** (`.exe`)
5. Double-click it — the game starts immediately!

> ✅ No Python interpreter needed. No pip install. Just download and play.

---

## 🧠 About the AI Engine

The AI was built from scratch using only fundamental algorithms — no machine learning, no neural networks, no genetic algorithms. The goal was to prove that a **smart and challenging AI** can be built with simple, well-understood techniques:

- **Negamax** — a clean variant of the Minimax algorithm, where each player tries to maximize their own score
- **Alpha-Beta Pruning** — cuts off branches that can't possibly affect the final decision, making the search significantly faster
- **Piece-Square Tables** — positional scoring tables for each piece type (knights prefer the center, rooks prefer open files, pawns are rewarded for advancing, etc.)
- **Search Depth: 3** — tested and chosen as the best balance between speed and intelligence. The AI thinks fast and plays well

### How strong is it?
Tested with real chess players:
- For **beginners** → it feels **hard**
- For **intermediate players** → it feels like a solid **intermediate** opponent
- It won't beat a grandmaster, but it will punish your mistakes

---

## 🕹️ Controls

| Action | Control |
|--------|---------|
| Select & move a piece | Mouse click |
| Undo last move | `Z` key |
| Reset the game | `R` key |

- Selected pieces are highlighted in **blue**
- Possible moves are highlighted in **yellow**

---

## ✨ Features

- Clean, animated piece movement
- Full chess rules: castling, en passant, pawn promotion
- Move log panel displayed during the game
- Stopwatch tracking time for each player
- Checkmate and stalemate detection
- Works as a standalone `.exe` — no installation needed

---

## 🖼️ Screenshots & Demo

### Main Menu
![Menu](gifs/Play%20VS%20AI%20game%20only.gif)

### Player vs AI
![Player vs AI](gifs/Player%20VS%20AI%20with%20score%20board.gif)

### AI vs AI
![AI vs AI](gifs/AI%20vs%20AI%20with%20score%20board.gif)

### Player vs Player
![PvP](gifs/PVP.gif)

---

## 🛠️ Run from Source (For Developers)

If you want to run or modify the code:

**Requirements:**
- Python 3.x
- Pygame

```bash
pip install pygame
```

Then run:
```bash
python Chess/Button.py
```

To increase AI difficulty (slower but smarter), open `Chess/ChessAI.py` and change:
```python
DEPTH = 3  # increase to 4 or 5 for harder AI (significantly slower)
```

---

## 📁 Project Structure

```
Chess/
├── images/          # Piece images (PNG)
├── ChessEngine.py   # Game logic, move validation, all chess rules
├── ChessAI.py       # AI engine (Negamax + Alpha-Beta Pruning)
├── ChessMain.py     # Main game loop and rendering
├── Button.py        # Entry point / main menu
├── predisplay.py    # Pre-game display screens
└── __init__.py
```

---

## 👨‍💻 Author

**Alireza Ramyad**
Bachelor's Degree Final Project

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

*If you enjoyed this project, please consider giving it a ⭐ — it means a lot!*
