import pygame
import math
import random
from constants import *

class Unit:
    def __init__(self, q, r, player, unit_type="Marine"):
        self.q = q
        self.r = r
        self.player = player
        self.unit_type = unit_type
        self.health = UNIT_HEALTH
        self.max_health = UNIT_HEALTH
        self.damage = UNIT_DAMAGE
        self.movement_points = MAX_MOVEMENT
        self.max_movement = MAX_MOVEMENT
        self.attack_range = MAX_ATTACK_RANGE
        self.has_attacked = False
        self.has_moved = False
        
        # Visual properties
        self.color = PLAYER1_COLOR if player == 1 else PLAYER2_COLOR
        self.size = HEX_RADIUS // 2
    
    def can_move_to(self, target_q, target_r, game_state):
        """Check if unit can move to target hex"""
        if self.has_moved:
            return False
        
        # Check if target is occupied
        if game_state.get_unit_at(target_q, target_r):
            return False
        
        # Check if within movement range
        distance = game_state.grid.get_distance(self.q, self.r, target_q, target_r)
        return distance <= self.movement_points
    
    def can_attack(self, target_q, target_r, game_state):
        """Check if unit can attack target hex"""
        if self.has_attacked:
            return False
        
        target_unit = game_state.get_unit_at(target_q, target_r)
        if not target_unit or target_unit.player == self.player:
            return False
        
        distance = game_state.grid.get_distance(self.q, self.r, target_q, target_r)
        return distance <= self.attack_range
    
    def move_to(self, target_q, target_r):
        """Move unit to target position"""
        distance = abs(target_q - self.q) + abs(target_r - self.r)
        self.movement_points -= distance
        self.q = target_q
        self.r = target_r
        self.has_moved = True
    
    def attack(self, target_unit, game_state):
        """Attack target unit with hit chance calculation"""
        if target_unit:
            # Base hit chance is 85%
            hit_chance = 0.85
            damage = self.damage
            
            # Check for Assault Marine interference (sniper penalty)
            if self.unit_type == "SN" and target_unit.player != self.player:
                # Check if target is adjacent to any enemy Assault units
                target_neighbors = game_state.grid.get_neighbors(target_unit.q, target_unit.r)
                for neighbor_q, neighbor_r in target_neighbors:
                    neighbor_unit = game_state.get_unit_at(neighbor_q, neighbor_r)
                    if (neighbor_unit and neighbor_unit.unit_type == "AM" 
                        and neighbor_unit.player != self.player):
                        hit_chance *= 0.5  # 50% less chance to hit
                        break
            
            # Anti-Vehicle Marine bonus damage against vehicles
            if (self.unit_type == "AV" and 
                target_unit.unit_type in ["T", "AR"]):
                damage = int(damage * 2.0)  # Double damage vs vehicles
                hit_chance = 0.95  # Higher accuracy vs vehicles
            
            # Roll for hit
            if random.random() <= hit_chance:
                target_unit.take_damage(damage)
                self.has_attacked = True
                return True  # Hit successful
            else:
                self.has_attacked = True
                return False  # Missed
        return False
    
    def take_damage(self, damage):
        """Take damage and return True if unit dies"""
        self.health -= damage
        return self.health <= 0
    
    def reset_turn(self):
        """Reset unit for new turn"""
        self.movement_points = self.max_movement
        self.has_attacked = False
        self.has_moved = False
    
    def get_pixel_position(self):
        """Get pixel position for drawing"""
        x = HEX_RADIUS * (math.sqrt(3) * self.q + math.sqrt(3)/2 * self.r)
        y = HEX_RADIUS * (3/2 * self.r)
        return (int(x + GRID_OFFSET_X), int(y + GRID_OFFSET_Y))
    
    def draw(self, screen):
        """Draw the unit"""
        x, y = self.get_pixel_position()
        
        # Draw unit body
        pygame.draw.circle(screen, self.color, (x, y), self.size)
        pygame.draw.circle(screen, UNIT_OUTLINE, (x, y), self.size, 2)
        
        # Draw health bar
        if self.health < self.max_health:
            bar_width = HEX_RADIUS
            bar_height = 4
            bar_x = x - bar_width // 2
            bar_y = y - self.size - 10
            
            # Background
            pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
            
            # Health
            health_width = int((self.health / self.max_health) * bar_width)
            pygame.draw.rect(screen, GREEN, (bar_x, bar_y, health_width, bar_height))
        
        # Draw unit type indicator
        font = pygame.font.Font(None, 16)
        text = font.render(self.unit_type, True, WHITE)  # Full unit type abbreviation
        text_rect = text.get_rect(center=(x, y))
        screen.blit(text, text_rect)
    
    def draw_movement_range(self, screen, grid):
        """Draw movement range overlay"""
        if self.has_moved:
            return
        
        valid_moves = grid.get_hexagons_in_range(self.q, self.r, self.movement_points)
        for hex_q, hex_r in valid_moves:
            if (hex_q, hex_r) != (self.q, self.r):  # Don't highlight current position
                hexagon = grid.hexagons[(hex_q, hex_r)]
                # Draw semi-transparent overlay
                surface = pygame.Surface((HEX_RADIUS * 2, HEX_RADIUS * 2))
                surface.set_alpha(100)
                surface.fill(GREEN)
                screen.blit(surface, (hexagon.x - HEX_RADIUS, hexagon.y - HEX_RADIUS))
    
    def draw_attack_range(self, screen, grid):
        """Draw attack range overlay"""
        if self.has_attacked:
            return
        
        valid_attacks = grid.get_hexagons_in_range(self.q, self.r, self.attack_range)
        for hex_q, hex_r in valid_attacks:
            if (hex_q, hex_r) != (self.q, self.r):  # Don't highlight current position
                hexagon = grid.hexagons[(hex_q, hex_r)]
                # Draw semi-transparent overlay
                surface = pygame.Surface((HEX_RADIUS * 2, HEX_RADIUS * 2))
                surface.set_alpha(100)
                surface.fill(RED)
                screen.blit(surface, (hexagon.x - HEX_RADIUS, hexagon.y - HEX_RADIUS))

class Marine(Unit):
    def __init__(self, q, r, player):
        super().__init__(q, r, player, "MA")
        self.health = 80
        self.max_health = 80
        self.damage = 20
        self.movement_points = 3
        self.max_movement = 3
        self.attack_range = 2

class Assault(Unit):
    def __init__(self, q, r, player):
        super().__init__(q, r, player, "AM")
        self.health = 120
        self.max_health = 120
        self.damage = 35
        self.movement_points = 4
        self.max_movement = 4
        self.attack_range = 1

class Sniper(Unit):
    def __init__(self, q, r, player):
        super().__init__(q, r, player, "SN")
        self.health = 60
        self.max_health = 60
        self.damage = 40
        self.movement_points = 2
        self.max_movement = 2
        self.attack_range = 3

class Artillery(Unit):
    def __init__(self, q, r, player):
        super().__init__(q, r, player, "AR")
        self.health = 50
        self.max_health = 50
        self.damage = 60
        self.movement_points = 1
        self.max_movement = 1
        self.attack_range = 4

class Tank(Unit):
    def __init__(self, q, r, player):
        super().__init__(q, r, player, "T")
        self.health = 150
        self.max_health = 150
        self.damage = 45
        self.movement_points = 2
        self.max_movement = 2
        self.attack_range = 2

class AntiVehicle(Unit):
    def __init__(self, q, r, player):
        super().__init__(q, r, player, "AV")
        self.health = 70
        self.max_health = 70
        self.damage = 30
        self.movement_points = 3
        self.max_movement = 3
        self.attack_range = 2 