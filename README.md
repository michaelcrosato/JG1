# Sci-Fi Hex Strategy Game

A turn-based strategy game with hexagonal grid system, featuring a futuristic sci-fi theme similar to Warhammer 40K. This is a 1v1 hot-seat multiplayer game where two players take turns commanding their units on a hexagonal battlefield.

![Game Preview](https://i.imgur.com/placeholder.png)

## Features

- **Hexagonal Grid System**: Tactical gameplay with hexagonal tiles for more strategic movement options
- **Turn-Based Combat**: Players alternate turns with movement and attack phases
- **Multiple Unit Types**: 
  - **Marines**: Balanced units with moderate health, damage, and mobility
  - **Assault**: Heavy units with high health and damage but limited movement
  - **Snipers**: Long-range units with high damage but low health
- **Hot-Seat Multiplayer**: Two players can play on the same computer
- **Sci-Fi Theme**: Futuristic aesthetic with cyan/blue color scheme
- **Visual Feedback**: Movement ranges, attack ranges, and unit health bars

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Setup
1. Clone or download this repository
2. Navigate to the game directory
3. Install dependencies:
```bash
pip install -r requirements.txt
```

## How to Run

```bash
python main.py
```

## How to Play

### Objective
Eliminate all enemy units to win the game.

### Game Flow
1. **Player 1 (Green)** starts first
2. Each turn, players can:
   - Select their units by left-clicking
   - Move selected units to valid positions
   - Attack enemy units within range
3. Press **SPACE** to end your turn
4. **Player 2 (Red)** takes their turn
5. Repeat until one player has no units remaining

### Controls
- **Left Click**: Select unit / Move unit / Attack target
- **SPACE**: End current turn
- **M**: Switch to movement mode (when unit selected)
- **A**: Switch to attack mode (when unit selected)
- **ESC**: Deselect current unit

### Unit Types

| Unit Type | Health | Damage | Movement | Attack Range | Role |
|-----------|--------|--------|----------|--------------|------|
| Marine    | 80     | 20     | 3        | 1            | Balanced infantry |
| Assault   | 120    | 35     | 2        | 1            | Heavy melee unit |
| Sniper    | 60     | 40     | 2        | 3            | Long-range support |

### Gameplay Mechanics

1. **Movement Phase**: 
   - Select a unit to see its movement range (green overlay)
   - Click on a valid hex to move the unit
   - Units can only move once per turn

2. **Attack Phase**:
   - After moving (or instead of moving), units can attack
   - Select attack mode to see attack range (red overlay)
   - Click on enemy units within range to attack
   - Units can only attack once per turn

3. **Turn Management**:
   - Each unit can move AND attack once per turn
   - Use SPACE to end your turn and pass control to the other player
   - Units reset their movement and attack status at the start of their player's turn

### Strategy Tips

- **Positioning**: Use the hexagonal grid to your advantage - units have 6 adjacent hexes instead of 4
- **Unit Synergy**: Combine different unit types for effective tactics
  - Use Marines for flexible positioning
  - Use Assault units to tank damage and deal heavy melee damage
  - Use Snipers to provide long-range support from safe positions
- **Movement Planning**: Plan your movement carefully - you can move then attack, but not attack then move
- **Range Advantage**: Snipers can attack from 3 hexes away, use this to avoid retaliation

## File Structure

```
JG1/
├── main.py          # Entry point
├── game.py          # Main game logic and loop
├── hexgrid.py       # Hexagonal grid system
├── units.py         # Unit classes and combat logic
├── constants.py     # Game configuration and colors
├── requirements.txt # Python dependencies
└── README.md        # This file
```

## Technical Details

- Built with **Python** and **Pygame**
- Uses axial coordinate system for hexagonal grid calculations
- Modular design allows for easy expansion of unit types and game mechanics
- 60 FPS rendering with optimized drawing routines

## Future Enhancements

Potential improvements that could be added:
- AI opponents with different difficulty levels
- Terrain effects and obstacles
- More unit types and special abilities
- Multiplayer over network
- Campaign mode with scenarios
- Sound effects and music
- Improved graphics and animations

## Troubleshooting

### Common Issues

1. **ImportError**: Make sure you've installed the requirements:
   ```bash
   pip install pygame numpy
   ```

2. **Game won't start**: Ensure you have Python 3.7+ installed:
   ```bash
   python --version
   ```

3. **Performance issues**: The game runs at 60 FPS by default. If you experience lag, your system might be underpowered for the current settings.

## Contributing

Feel free to fork this project and submit pull requests for improvements!

## License

This project is open source and available under the MIT License. 