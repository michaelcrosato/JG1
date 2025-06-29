import pygame
import math
from constants import *

class HexGrid:
    def __init__(self):
        self.hexagons = {}
        self.selected_hex = None
        self.hovered_hex = None
        self.create_grid()
    
    def create_grid(self):
        """Create the hexagonal grid"""
        for q in range(GRID_WIDTH):
            for r in range(GRID_HEIGHT):
                # Offset coordinates for better grid layout
                self.hexagons[(q, r)] = Hexagon(q, r)
    
    def pixel_to_hex(self, x, y):
        """Convert pixel coordinates to hex coordinates"""
        # Adjust for grid offset
        x -= GRID_OFFSET_X
        y -= GRID_OFFSET_Y
        
        # Convert to hex coordinates using axial coordinate system
        q = (math.sqrt(3)/3 * x - 1/3 * y) / HEX_RADIUS
        r = (2/3 * y) / HEX_RADIUS
        
        # Round to nearest hex
        return self.hex_round(q, r)
    
    def hex_round(self, q, r):
        """Round fractional hex coordinates to nearest hex"""
        s = -q - r
        rq = round(q)
        rr = round(r)
        rs = round(s)
        
        q_diff = abs(rq - q)
        r_diff = abs(rr - r)
        s_diff = abs(rs - s)
        
        if q_diff > r_diff and q_diff > s_diff:
            rq = -rr - rs
        elif r_diff > s_diff:
            rr = -rq - rs
        
        return (rq, rr)
    
    def hex_to_pixel(self, q, r):
        """Convert hex coordinates to pixel coordinates"""
        x = HEX_RADIUS * (math.sqrt(3) * q + math.sqrt(3)/2 * r)
        y = HEX_RADIUS * (3/2 * r)
        return (int(x + GRID_OFFSET_X), int(y + GRID_OFFSET_Y))
    
    def get_neighbors(self, q, r):
        """Get all neighboring hexagons"""
        directions = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]
        neighbors = []
        for dq, dr in directions:
            nq, nr = q + dq, r + dr
            if (nq, nr) in self.hexagons:
                neighbors.append((nq, nr))
        return neighbors
    
    def get_distance(self, q1, r1, q2, r2):
        """Calculate distance between two hexagons"""
        return (abs(q1 - q2) + abs(q1 + r1 - q2 - r2) + abs(r1 - r2)) / 2
    
    def get_hexagons_in_range(self, q, r, range_limit):
        """Get all hexagons within a certain range"""
        hexagons_in_range = []
        for hex_q, hex_r in self.hexagons:
            if self.get_distance(q, r, hex_q, hex_r) <= range_limit:
                hexagons_in_range.append((hex_q, hex_r))
        return hexagons_in_range
    
    def handle_mouse_event(self, mouse_pos, event_type):
        """Handle mouse events on the grid"""
        hex_coord = self.pixel_to_hex(mouse_pos[0], mouse_pos[1])
        
        if hex_coord in self.hexagons:
            if event_type == "hover":
                self.hovered_hex = hex_coord
            elif event_type == "click":
                self.selected_hex = hex_coord
                return hex_coord
        return None
    
    def draw(self, screen):
        """Draw the hexagonal grid"""
        for (q, r), hexagon in self.hexagons.items():
            color = HEX_FILL
            
            # Highlight selected or hovered hex
            if (q, r) == self.selected_hex:
                color = HEX_SELECTED
            elif (q, r) == self.hovered_hex:
                color = HEX_HOVER
            
            hexagon.draw(screen, color)

class Hexagon:
    def __init__(self, q, r):
        self.q = q
        self.r = r
        self.x, self.y = self.hex_to_pixel()
        self.points = self.calculate_points()
    
    def hex_to_pixel(self):
        """Convert hex coordinates to pixel coordinates"""
        x = HEX_RADIUS * (math.sqrt(3) * self.q + math.sqrt(3)/2 * self.r)
        y = HEX_RADIUS * (3/2 * self.r)
        return (int(x + GRID_OFFSET_X), int(y + GRID_OFFSET_Y))
    
    def calculate_points(self):
        """Calculate the six corner points of the hexagon"""
        points = []
        for i in range(6):
            angle = math.pi / 3 * i
            x = self.x + HEX_RADIUS * math.cos(angle)
            y = self.y + HEX_RADIUS * math.sin(angle)
            points.append((int(x), int(y)))
        return points
    
    def draw(self, screen, fill_color):
        """Draw the hexagon"""
        pygame.draw.polygon(screen, fill_color, self.points)
        pygame.draw.polygon(screen, HEX_OUTLINE, self.points, 2) 