# game.py
import pygame
import sys
from grid import Grid
from sprite import Sprite
import heapq
import time

CELL_SIZE = 50
GRID_SIZE = 9
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((CELL_SIZE * GRID_SIZE, CELL_SIZE * GRID_SIZE + 70))
        pygame.display.set_caption("Dijkstra's Algorithm Simulator")
        self.grid = Grid(GRID_SIZE, CELL_SIZE)
        self.sprite = Sprite([0, 0], CELL_SIZE)
        self.running = False
        self.rewards_enabled = True  # Track whether rewards are enabled
        self.grid.place_rewards(5)  # Place rewards randomly

    def dijkstra(self, start, end):
        """Compute shortest path from start to end using Dijkstra's algorithm."""
        distances = {start: 0}
        previous_nodes = {start: None}
        queue = [(0, start)]
        
        while queue:
            current_distance, current_position = heapq.heappop(queue)
            
            if current_position == end:
                break  # Found shortest path to end

            row, col = current_position
            neighbors = [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]

            for neighbor in neighbors:
                n_row, n_col = neighbor
                if 0 <= n_row < GRID_SIZE and 0 <= n_col < GRID_SIZE and not self.grid.is_wall(n_row, n_col):
                    distance = current_distance + 1  # All edges have weight 1
                    if neighbor not in distances or distance < distances[neighbor]:
                        distances[neighbor] = distance
                        previous_nodes[neighbor] = current_position
                        heapq.heappush(queue, (distance, neighbor))
        
        # Reconstruct path from end to start
        path = []
        current = end
        while current is not None:
            path.insert(0, list(current))
            current = previous_nodes.get(current)
        
        return path

    def handle_buttons(self, pos):
        """Handle button clicks."""
        # Start Button
        if 10 <= pos[0] <= 110 and GRID_SIZE * CELL_SIZE + 10 <= pos[1] <= GRID_SIZE * CELL_SIZE + 40:
            self.start_simulation()
        # Reset Button
        elif 130 <= pos[0] <= 230 and GRID_SIZE * CELL_SIZE + 10 <= pos[1] <= GRID_SIZE * CELL_SIZE + 40:
            self.reset_simulation()
        # Toggle Rewards Button
        elif 250 <= pos[0] <= 350 and GRID_SIZE * CELL_SIZE + 10 <= pos[1] <= GRID_SIZE * CELL_SIZE + 40:
            self.toggle_rewards()

    def start_simulation(self):
        """Start the Dijkstra's algorithm simulation."""
        start = (0, 0)
        end = (GRID_SIZE - 1, GRID_SIZE - 1)
        path = self.dijkstra(start, end)
        self.sprite.set_path(path)
        self.running = True

    def reset_simulation(self):
        """Reset the simulation."""
        self.sprite.position = [0, 0]
        self.sprite.path = []
        self.running = False

    def toggle_rewards(self):
        """Toggle the reward collection functionality."""
        self.rewards_enabled = not self.rewards_enabled

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if mouse_pos[1] < GRID_SIZE * CELL_SIZE:  # Within grid
                    self.grid.toggle_wall(mouse_pos)
                else:  # Below grid, within button area
                    self.handle_buttons(mouse_pos)

    def update(self):
        if self.running:
            self.sprite.follow_path()
            time.sleep(0.1)
            if not self.sprite.path:
                self.running = False  # Stop if path is complete
            elif self.rewards_enabled:
                self.sprite.collect_reward(self.grid)  # Collect rewards if enabled

    def draw(self):
        self.screen.fill(WHITE)
        self.grid.draw(self.screen)
        self.sprite.draw(self.screen)

        # Draw buttons
        pygame.draw.rect(self.screen, BLUE, (10, GRID_SIZE * CELL_SIZE + 10, 100, 30))  # Start Button
        pygame.draw.rect(self.screen, BLUE, (130, GRID_SIZE * CELL_SIZE + 10, 100, 30))  # Reset Button
        pygame.draw.rect(self.screen, GREEN if self.rewards_enabled else (100, 100, 100),
                         (250, GRID_SIZE * CELL_SIZE + 10, 100, 30))  # Toggle Rewards Button

        # Optional: Draw simple text indicators
        pygame.draw.line(self.screen, WHITE, (35, GRID_SIZE * CELL_SIZE + 25), (65, GRID_SIZE * CELL_SIZE + 25), 3)  # Start indicator
        pygame.draw.line(self.screen, WHITE, (155, GRID_SIZE * CELL_SIZE + 25), (185, GRID_SIZE * CELL_SIZE + 25), 3)  # Reset indicator
        pygame.draw.line(self.screen, WHITE, (275, GRID_SIZE * CELL_SIZE + 25), (325, GRID_SIZE * CELL_SIZE + 25), 3)  # Toggle Rewards indicator

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
