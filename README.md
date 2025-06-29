# Sci-Fi Hex Strategy Game

A turn-based strategy game with hexagonal grid system, featuring a futuristic sci-fi theme similar to Warhammer 40K. This is a 1v1 hot-seat multiplayer game where two players take turns commanding their units on a hexagonal battlefield.

![Game Preview](https://i.imgur.com/placeholder.png)

## Features

- **Hexagonal Grid System**: Tactical gameplay with hexagonal tiles for more strategic movement options
- **Turn-Based Combat**: Players alternate turns with movement and attack phases
- **Advanced Combat System**: Hit chance mechanics with special unit interactions
- **Six Distinct Unit Types**: 
  - **Marines**: Balanced units with moderate health, damage, and 2-hex attack range
  - **Assault**: Fast heavy units with high health, damage, increased mobility, and sniper disruption
  - **Snipers**: Long-range units with high damage but reduced accuracy near Assault units
  - **Artillery**: Extreme long-range bombardment units with massive damage but very fragile
  - **Tanks**: Heavy armored units with high durability and decent firepower
  - **Anti-Vehicle**: Vehicle specialists that excel vs Tanks/Artillery but struggle vs infantry
- **Hot-Seat Multiplayer**: Two players can play on the same computer
- **Large-Scale Battles**: Each player starts with 12 units across 6 different types
- **Sci-Fi Theme**: Futuristic aesthetic with cyan/blue color scheme
- **Visual Feedback**: Movement ranges, attack ranges, unit health bars, and clear unit identification
- **Battlefield Clarity**: Units display clear abbreviations (MA=Marine, AM=Assault, SN=Sniper, AR=Artillery, T=Tank, AV=Anti-Vehicle)

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

| Unit Type | Display | Health | Damage | Movement | Attack Range | Role | Special Ability |
|-----------|---------|--------|--------|----------|--------------|------|------------------|
| Marine    | MA      | 80     | 20     | 3        | 2            | Balanced infantry | None |
| Assault   | AM      | 120    | 35     | 4        | 1            | Fast heavy unit | Disrupts enemy snipers |
| Sniper    | SN      | 60     | 40     | 2        | 3            | Long-range support | Reduced accuracy near Assault units |
| Artillery | AR      | 50     | 60     | 1        | 4            | Long-range bombardment | Extreme range, fragile |
| Tank      | T       | 150    | 45     | 2        | 2            | Heavy armor | High durability |
| Anti-Vehicle | AV   | 70     | 30     | 3        | 2            | Vehicle specialist | 2x damage + 95% accuracy vs vehicles; 50% accuracy vs infantry |

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

4. **Combat System**:
   - All attacks have an 85% base hit chance - attacks can miss!
   - **Assault Disruption**: Enemy snipers adjacent to your Assault units have 50% reduced hit chance (42.5% total)
   - **Anti-Vehicle Specialization**: 
     - vs Vehicles (Tanks/Artillery): 2x damage + 95% hit chance
     - vs Infantry (Marines/Assault/Snipers): 42.5% hit chance (50% penalty)
   - Position your Assault units strategically to protect other units from sniper fire
   - Use Anti-Vehicle Marines specifically against enemy armor and artillery - they're weak vs infantry!
   - Failed attacks still consume the unit's attack for that turn

### Strategy Tips

- **Positioning**: Use the hexagonal grid to your advantage - units have 6 adjacent hexes instead of 4
- **Unit Synergy**: Combine different unit types for effective tactics
  - **Marines (MA)**: Flexible positioning with 2-hex attack range - solid frontline units
  - **Assault (AM)**: Fast heavy units (4 movement!) - rush enemy positions and disrupt snipers
  - **Snipers (SN)**: Long-range support but vulnerable to Assault unit interference
  - **Artillery (AR)**: Extreme range bombardment (4 hexes) but very fragile - protect them!
  - **Tanks (T)**: Heavily armored frontline units - can absorb massive damage
  - **Anti-Vehicle (AV)**: Specialists vs vehicles (2x damage) but weak vs infantry (50% hit chance penalty)
- **Movement Planning**: Plan your movement carefully - you can move then attack, but not attack then move
- **Range Advantage**: Artillery (4 hex) > Snipers (3 hex) > Marines/Tanks/Anti-Vehicle (2 hex) > Assault (1 hex)
- **Assault Tactics**: Use their increased 4-hex movement to quickly position and disrupt enemy snipers
- **Vehicle Warfare**: Anti-Vehicle Marines are specialists - excellent vs vehicles but poor vs infantry
- **Tactical Specialization**: Use AV units against T/AR, but protect them from enemy infantry
- **Hit Chance**: 85% base, snipers near AM: 42.5%, AV vs vehicles: 95%, AV vs infantry: 42.5%

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