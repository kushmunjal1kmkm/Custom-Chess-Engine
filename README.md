# Custom Python Chess Engine

Welcome to the Custom Python Chess Engine! This project is a fully functional chess application developed in Python. It features a complete set of chess rules, a graphical user interface (GUI) built with Pygame, and an integrated AI opponent that uses advanced search algorithms to play against you.

## Features

### Core Mechanics & Rules
- **Complete Move Generation:** Supports all standard piece movements.
- **Advanced Rules:** Fully implements Castling, En Passant, and automatic Pawn Promotion.
- **Game States:** Accurate detection of Checks, Checkmates, and Stalemates.
- **Move Log:** A dedicated panel that records and displays the move history using standard algebraic chess notation.

### Graphical User Interface (GUI)
- **Pygame-based UI:** Clean, responsive, and interactive 2D chessboard.
- **Square Highlighting:** Highlights the currently selected piece and shows all its valid destination squares to assist the player.
- **Smooth Animations:** Pieces glide smoothly across the board when a move is executed.
- **Keyboard Controls:** 
  - Press **`z`** to undo the last move.
  - Press **`r`** to reset the board and start a new game.

### Artificial Intelligence (AI)
- **NegaMax with Alpha-Beta Pruning:** The engine uses an optimized NegaMax search algorithm coupled with Alpha-Beta pruning to evaluate positions efficiently and choose the best moves.
- **Multiprocessing:** The AI calculates its moves on a separate background process. This ensures the GUI remains completely responsive while the AI is "thinking," allowing you to interact with the board or undo moves seamlessly.

## Project Structure
- `ChessMain.py`: The entry point of the application. Handles the Pygame GUI, user inputs, and multiprocessing for the AI.
- `ChessEngine.py`: The core backend. Manages the game state, validates moves, and enforces chess rules.
- `smartmovefinder.py`: The AI module. Contains the scoring functions and NegaMax alpha-beta search algorithms.

## How It Works
1. **Game State Management:** The board is represented as a 2D list. `ChessEngine.py` evaluates the board state to generate valid moves based on whose turn it is, considering checks and pins.
2. **Move Processing:** When a player clicks to move a piece, the move is validated against the generated list. If valid, the move is applied, and turn control switches.
3. **AI Integration:** When it's the AI's turn, `ChessMain.py` spawns a background process that calls `smartmovefinder.py`. The AI evaluates future possible board states up to a certain depth (default is depth 4), scoring them based on material advantages. The best found move is then passed back to the main thread via a queue and executed on the board.

## How to Run the Project

### Prerequisites
- **Python 3.x:** Make sure you have Python installed on your system.
- **Pygame:** This project requires the Pygame library for rendering the UI.

### Installation & Execution
1. Clone the repository or download the project files.
2. Open your terminal or command prompt.
3. Install Pygame (if you haven't already):
   ```bash
   pip install pygame
   ```
4. Run the main application file:
   ```bash
   python project_files/ChessMain.py
   ```

Enjoy playing against the engine or studying the move generations!
