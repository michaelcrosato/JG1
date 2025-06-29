#!/usr/bin/env python3
"""
Sci-Fi Hex Strategy Game
A turn-based strategy game with hexagonal grid
Theme: Futuristic Warhammer 40K style
"""

from game import Game

def main():
    """Main entry point"""
    try:
        game = Game()
        game.run()
    except KeyboardInterrupt:
        print("\nGame interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

if __name__ == "__main__":
    main() 