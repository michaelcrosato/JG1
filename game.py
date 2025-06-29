import pygame
import sys
from constants import *
from hexgrid import HexGrid
from units import Marine, Assault, Sniper

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Sci-Fi Hex Strategy")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Game state
        self.grid = HexGrid()
        self.units = {}
        self.current_player = 1
        self.selected_unit = None
        self.game_mode = "move"  # "move" or "attack"
        self.turn_number = 1
        
        self.setup_initial_units()
    
    def setup_initial_units(self):
        """Setup initial unit positions"""
        # Player 1 units (left side)
        self.add_unit(Marine(2, 2, 1))
        self.add_unit(Marine(3, 3, 1))
        self.add_unit(Assault(1, 4, 1))
        self.add_unit(Sniper(2, 5, 1))
        
        # Player 2 units (right side)
        self.add_unit(Marine(12, 2, 2))
        self.add_unit(Marine(11, 3, 2))
        self.add_unit(Assault(13, 4, 2))
        self.add_unit(Sniper(12, 5, 2))
    
    def add_unit(self, unit):
        """Add a unit to the game"""
        self.units[(unit.q, unit.r)] = unit
    
    def remove_unit(self, q, r):
        """Remove a unit from the game"""
        if (q, r) in self.units:
            del self.units[(q, r)]
    
    def get_unit_at(self, q, r):
        """Get unit at specific hex coordinates"""
        return self.units.get((q, r))
    
    def move_unit(self, unit, target_q, target_r):
        """Move a unit to new position"""
        # Remove from old position
        del self.units[(unit.q, unit.r)]
        
        # Move unit
        unit.move_to(target_q, target_r)
        
        # Add to new position
        self.units[(unit.q, unit.r)] = unit
    
    def handle_hex_click(self, hex_coord):
        """Handle clicking on a hexagon"""
        q, r = hex_coord
        clicked_unit = self.get_unit_at(q, r)
        
        if self.selected_unit is None:
            # Select a unit
            if clicked_unit and clicked_unit.player == self.current_player:
                self.selected_unit = clicked_unit
                self.game_mode = "move"
        else:
            # Unit is selected
            if clicked_unit == self.selected_unit:
                # Deselect unit
                self.selected_unit = None
            elif clicked_unit and clicked_unit.player == self.current_player:
                # Select different unit
                self.selected_unit = clicked_unit
                self.game_mode = "move"
            elif self.game_mode == "move":
                # Try to move
                if self.selected_unit.can_move_to(q, r, self):
                    self.move_unit(self.selected_unit, q, r)
                    self.game_mode = "attack"
            elif self.game_mode == "attack":
                # Try to attack
                target_unit = self.get_unit_at(q, r)
                if target_unit and self.selected_unit.can_attack(q, r, self):
                    if self.selected_unit.attack(target_unit):
                        if target_unit.health <= 0:
                            self.remove_unit(q, r)
                    self.selected_unit = None
                    self.game_mode = "move"
    
    def end_turn(self):
        """End current player's turn"""
        # Reset all units for current player
        for unit in self.units.values():
            if unit.player == self.current_player:
                unit.reset_turn()
        
        # Switch players
        self.current_player = 2 if self.current_player == 1 else 1
        self.selected_unit = None
        self.game_mode = "move"
        
        if self.current_player == 1:
            self.turn_number += 1
    
    def check_win_condition(self):
        """Check if game is won"""
        player1_units = sum(1 for unit in self.units.values() if unit.player == 1)
        player2_units = sum(1 for unit in self.units.values() if unit.player == 2)
        
        if player1_units == 0:
            return 2
        elif player2_units == 0:
            return 1
        return None
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    hex_coord = self.grid.handle_mouse_event(event.pos, "click")
                    if hex_coord:
                        self.handle_hex_click(hex_coord)
            
            elif event.type == pygame.MOUSEMOTION:
                self.grid.handle_mouse_event(event.pos, "hover")
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.end_turn()
                elif event.key == pygame.K_ESCAPE:
                    self.selected_unit = None
                    self.game_mode = "move"
                elif event.key == pygame.K_m and self.selected_unit:
                    self.game_mode = "move"
                elif event.key == pygame.K_a and self.selected_unit:
                    self.game_mode = "attack"
        
        return True
    
    def draw_ui(self):
        """Draw the user interface"""
        # Background panel
        ui_rect = pygame.Rect(0, 0, SCREEN_WIDTH, 80)
        pygame.draw.rect(self.screen, UI_BACKGROUND, ui_rect)
        pygame.draw.rect(self.screen, CYAN, ui_rect, 2)
        
        # Current player
        player_text = self.font.render(f"Player {self.current_player}'s Turn", True, UI_TEXT)
        self.screen.blit(player_text, (10, 10))
        
        # Turn number
        turn_text = self.small_font.render(f"Turn: {self.turn_number}", True, UI_TEXT)
        self.screen.blit(turn_text, (10, 45))
        
        # Game mode
        if self.selected_unit:
            mode_text = self.small_font.render(f"Mode: {self.game_mode.capitalize()}", True, UI_TEXT)
            self.screen.blit(mode_text, (200, 10))
            
            # Unit info
            unit_info = f"{self.selected_unit.unit_type} - HP: {self.selected_unit.health}/{self.selected_unit.max_health}"
            unit_text = self.small_font.render(unit_info, True, UI_TEXT)
            self.screen.blit(unit_text, (200, 30))
            
            # Movement info
            if not self.selected_unit.has_moved:
                move_text = self.small_font.render(f"Movement: {self.selected_unit.movement_points}", True, UI_TEXT)
                self.screen.blit(move_text, (200, 50))
        
        # Instructions
        instructions = [
            "Left Click: Select/Move/Attack",
            "Space: End Turn",
            "M: Move Mode",
            "A: Attack Mode",
            "Esc: Deselect"
        ]
        
        for i, instruction in enumerate(instructions):
            inst_text = self.small_font.render(instruction, True, UI_TEXT)
            self.screen.blit(inst_text, (SCREEN_WIDTH - 250, 10 + i * 20))
    
    def draw(self):
        """Draw the game"""
        self.screen.fill(BLACK)
        
        # Draw grid
        self.grid.draw(self.screen)
        
        # Draw movement/attack range for selected unit
        if self.selected_unit:
            if self.game_mode == "move":
                self.selected_unit.draw_movement_range(self.screen, self.grid)
            elif self.game_mode == "attack":
                self.selected_unit.draw_attack_range(self.screen, self.grid)
        
        # Draw units
        for unit in self.units.values():
            unit.draw(self.screen)
            
            # Highlight selected unit
            if unit == self.selected_unit:
                x, y = unit.get_pixel_position()
                pygame.draw.circle(self.screen, WHITE, (x, y), unit.size + 5, 3)
        
        # Draw UI
        self.draw_ui()
        
        # Check win condition
        winner = self.check_win_condition()
        if winner:
            win_text = self.font.render(f"Player {winner} Wins!", True, WHITE)
            text_rect = win_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            pygame.draw.rect(self.screen, BLACK, text_rect.inflate(20, 20))
            pygame.draw.rect(self.screen, WHITE, text_rect.inflate(20, 20), 2)
            self.screen.blit(win_text, text_rect)
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        running = True
        while running:
            running = self.handle_events()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit() 