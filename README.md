# HexBot

![Static Badge](https://img.shields.io/badge/version-1.2.0-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

## Introduction

HexBot is a command-line implementation of the popular board game Catan (Settlers of Catan). The game features a hexagonal board with various resource-producing terrains, allowing players to build settlements, cities, and roads while trading resources and using development cards to gain advantages.

![Catan Image](./imgs/catan.png)

## Features

- Complete implementation of Catan game mechanics:
  - Resource collection based on dice rolls
  - Building settlements, cities, and roads
  - Trading with other players and the bank/ports
  - Development cards with various effects (Knight, Victory Point, Monopoly, Road Building, Year of Plenty)
  - Special achievements (Longest Road, Largest Army)
  - Robber mechanics for stealing resources
  - Victory point tracking

- Game modes:
  - Human vs. Human gameplay
  - Bot players for solo play or testing
  - Automatic setup option for quicker game starts

## Requirements

- Python 3.8 or higher
- Required Python packages (see requirements.txt)

## Setup

To get started with HexBot, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/AidanInceer/HexBot
   cd HexBot
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:

   ```bash
   python main.py
   ```

## Game Rules

### Setup Phase
- Players take turns placing their initial settlements and roads
- The second settlement placement grants immediate resources from adjacent tiles
- Automatic setup is available for quicker game starts

### Gameplay
1. Roll the dice to determine resource production
2. Trade resources with other players or the bank
3. Build settlements, cities, and roads to expand your territory
4. Purchase and play development cards for special actions
5. First player to reach 10 victory points wins!

### Victory Points
- Settlements: 1 point each
- Cities: 2 points each
- Longest Road: 2 points (requires at least 5 connected road segments)
- Largest Army: 2 points (requires at least 3 Knight cards played)
- Victory Point cards: 1 point each

## Configuration

You can adjust the game settings in the central configuration file `src/config/config.py`. This allows you to customize:

- Number of players
- Game type (manual or automatic setup)
- Other game parameters

## Project Structure

- `main.py`: Entry point for the application
- `src/catan/`: Core game implementation
  - `board/`: Board representation with tiles, nodes, and edges
  - `buildings/`: Settlement, city, and road implementations
  - `deck/`: Development cards implementation
  - `game/`: Game flow and turn management
  - `player/`: Player actions and resource management
  - `resources/`: Resource types and management
- `src/config/`: Configuration settings
- `src/interface/`: User interface handling
- `src/utils/`: Utility functions and helpers


## License

This project is licensed under the MIT License - see the LICENSE file for details.
