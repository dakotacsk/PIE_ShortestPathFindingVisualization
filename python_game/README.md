# Hatchling's Quest: Pathfinding Trials

## Table of Contents

1. [Overview](#overview)
2. [Gameplay](#gameplay)
3. [Features](#features)
4. [Flow Map](#flow-map)
5. [Folder Structure](#folder-structure)
6. [File Descriptions](#file-descriptions)
7. [Technical Details](#technical-details)
8. [How to Run](#how-to-run)
9. [Contributors](#contributors)
10. [Future Plans](#future-plans)

---

## Overview

**Hatchling's Quest: Pathfinding Trials** is an educational and engaging Python-based game where players guide a baby turtle ("the hatchling") through challenging levels using pathfinding algorithms. The game combines visual learning, interactive gameplay, and computational concepts like **Dijkstra's Algorithm** and **Q-Learning**.

This project is designed for:

- Students and educators exploring pathfinding algorithms.
- Gamers interested in learning about AI through gameplay.
- Developers seeking insights into combining educational tools and game development.

---

## Gameplay

### Levels:

1. **Level 1 (Dijkstra's Algorithm)**:

   - Players manually set up the grid and watch the hatchling follow the shortest path using Dijkstra's Algorithm.
   - Prepares the player for the advanced Q-Learning level.

2. **Level 2 (Q-Learning)**:
   - Players configure the environment and train the hatchling to learn optimal paths.
   - Handles penalties (red cells) and rewards (green cells) dynamically.
   - Includes interactive explanations for invalid moves, oscillations, and step management.

### Interactive Features:

- Grid customization (set rewards, penalties, and obstacles).
- Step-by-step pathfinding visualization.
- Adaptive explanations triggered during gameplay to deepen understanding.

---

## Features

1. **Algorithms**:

   - **Dijkstra's Algorithm** for deterministic shortest-path navigation.
   - **Q-Learning** for dynamic, reinforcement-based pathfinding.

2. **Educational Focus**:

   - Interactive explanations for key algorithmic behaviors.
   - Visual cues for penalties, rewards, and invalid actions.

3. **Replayability**:

   - Players can restart levels and try different grid configurations.
   - Selectable maximum steps in Level 2 for varied challenges.

4. **Leaderboard**:
   - Tracks high scores based on performance metrics like path efficiency and penalties.

---

## Flow Map

![pathfinders_flow](https://github.com/user-attachments/assets/52c6363c-0825-46ff-b6ea-436a00d26077)

This flow map outlines the logical structure of the game, including transitions between levels, explanations, and key algorithms like Dijkstra's and Q-Learning.

---

## Folder Structure

```
python_game/
├── fonts/                   # Fonts used throughout the game
├── grid/                    # Grid setup and logic
│   └── grid.py
├── images/                  # Sprite and asset images
├── leaderboard/             # Leaderboard data
│   └── leaderboard.csv
├── screens/                 # Screens and transitions
│   ├── main_menu.py
│   ├── intro_cutscene.py
│   ├── instructions/
│   │   ├── instructions.py
│   │   └── instructions2.py
│   ├── ending_scene.py
│   └── explanations/        # Dynamic explanations
│       ├── invalid_move_explanation.py
│       ├── many_steps_explanation.py
│       └── oscillation_explanation.py
├── sprites/                 # Sprites and gameplay logic
│   ├── DijkstraSprite.py
│   └── QLearningSprite.py
└── run_game.py              # Main entry point
```

---

## File Descriptions

### Core Files

- **`run_game.py`**: Main entry point for the game. Manages screen transitions and game initialization.
- **`grid.py`**: Defines the grid environment, including cell properties and drawing logic.

### Gameplay Levels

- **`game1.py`**: Implements Dijkstra's Algorithm with interactive grid setup.
- **`game2.py`**: Implements Q-Learning with interactive explanations for dynamic behaviors.

### Screens

- **`main_menu.py`**: The starting screen for choosing options like "Start Game" or "Exit."
- **`intro_cutscene.py`**: Provides an engaging narrative introduction to the game.
- **`instructions.py`**: Explains the gameplay for Level 1.
- **`instructions2.py`**: Prepares players for Level 2 (Q-Learning).
- **`ending_scene.py`**: Displays the final score and options to retry or return to the main menu.

### Explanations

- **`invalid_move_explanation.py`**: Explains invalid moves and their penalties.
- **`many_steps_explanation.py`**: Explains penalties for excessive steps.
- **`oscillation_explanation.py`**: Explains oscillations and how to address them.

### Leaderboard

- **`leaderboard.py`**: Manages saving, loading, and displaying scores.
- **`leaderboard.csv`**: Stores high scores.

---

## Technical Details

### Key Algorithms:

1. **Dijkstra's Algorithm**:

   - Computes the shortest path from the starting point to the goal.
   - Deterministic and straightforward, ideal for Level 1.

2. **Q-Learning**:
   - A reinforcement learning algorithm that adapts to the grid's rewards and penalties.
   - Demonstrates dynamic learning through training and exploration.

### Dynamic Explanations:

- Real-time explanations provide insights into gameplay events like invalid moves, oscillations, or step penalties.

---

## How to Run

1. **Install Dependencies**:

   - Ensure Python 3.8+ and `pygame` are installed:
     ```bash
     pip install pygame
     ```

2. **Run the Game**:

   - Navigate to the `python_game/` directory and execute:
     ```bash
     python run_game.py
     ```

3. **Controls**:
   - **Arrow Keys**: Move around the grid or select options.
   - **Spacebar**: Change grid cell colors.
   - **Enter**: Start pathfinding or confirm selections.

---

## Contributors

- **Dakota Chang** (Main Game and Algorithm Development), **Vishnu Eskew** (Plot Development), **Dan Khoi Nguyen** (Plot Development), **Chris Nie** (Mechanical)

---

## Future Plans

### Website

A dedicated website will be built to showcase the game and its educational benefits. Features will include:

- **Game Overview**: Information about the gameplay, algorithms, and educational value.
- **Download**: Links to download the game and access the source code.
- **Interactive Demos**: Embedded visuals or videos of gameplay.
- **Leaderboards**: Online leaderboard integration for competitive play.

### Enhancements

- Add more levels with advanced pathfinding algorithms.
- Incorporate an online mode for collaborative gameplay.
- Build a mobile-friendly version for wider accessibility.
