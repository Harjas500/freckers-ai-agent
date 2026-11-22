# Freckers AI Agent

A Python game-playing agent for **Freckers**, developed as part of the University of Melbourne's COMP30024 Artificial Intelligence project.

The agent models the game board, generates candidate actions, and selects moves using a depth-limited **Minimax search with alpha-beta pruning**.

## Project Overview

Freckers is a two-player strategy game played on an 8 × 8 board. The agent maintains an internal board state, simulates possible moves, and evaluates positions to choose an action.

## Agent Architecture

### Board Representation

The `AgentBoard` class maintains a copy of the board and provides helper methods to:

- Find the frogs belonging to either player.
- Determine the directions in which each player can move.
- Check valid single-step moves and jumps.
- Apply movement and lily-pad growth actions.
- Check whether a frog has reached its goal row.

### Move Generation

The agent generates candidate actions for each frog, including valid single-step moves and multi-jump sequences. A breadth-first search is used to explore possible jump paths.

### Search Algorithm

The agent uses **Minimax** with a search depth of 3 and **alpha-beta pruning** to reduce the number of positions that need to be explored.

### Heuristic Evaluation

The evaluation function scores a board position using factors including:

- Progress towards the player's goal row.
- Rewards for reaching the goal row.
- Bonuses for advancing beyond the middle of the board.
- Penalties for frogs that remain close to their starting side.
- The corresponding progress of the opponent's frogs.

When no movement action is generated, the agent falls back to a growth action.

## Repository Structure

```text
freckers-ai-agent/
├── agent/
│   ├── __init__.py
│   ├── agent_board.py
│   └── program.py
├── report.pdf
└── README.md
```

## Technologies and Concepts

- **Language:** Python
- **Search:** Minimax
- **Optimisation:** Alpha-beta pruning
- **Move generation:** Breadth-first search (BFS)
- **Core concepts:** Game-tree search, board-state simulation, heuristic evaluation

## Running the Agent

The agent uses the COMP30024 referee game framework, including the `referee.game` package. That framework is not included in this repository.

To run the agent, set up the compatible COMP30024 game environment and follow the course referee instructions for loading an agent package. The exact launch command depends on the supplied referee environment.

## Project Report

The accompanying `report.pdf` contains the submitted project report.

## Attribution

This was developed as a group project. The repository presents the agent implementation and supporting report; contributions should be attributed in accordance with the original team submission and applicable course sharing rules.

---

**Author:** Harjas Singh  
**GitHub:** [Harjas500](https://github.com/Harjas500)
