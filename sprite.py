# sprite.py
import pygame

BLACK = (0, 0, 0)

class Sprite:
    def __init__(self, start_pos, cell_size):
        self.position = start_pos  # Position in the grid
        self.cell_size = cell_size
        self.collected_rewards = 0  # Track the number of collected rewards

    def move(self, direction, grid):
        row, col = self.position
        if direction == "up" and row > 0 and not grid.is_wall(row - 1, col):
            self.position[0] -= 1
        elif direction == "down" and row < grid.grid_size - 1 and not grid.is_wall(row + 1, col):
            self.position[0] += 1
        elif direction == "left" and col > 0 and not grid.is_wall(row, col - 1):
            self.position[1] -= 1
        elif direction == "right" and col < grid.grid_size - 1 and not grid.is_wall(row, col + 1):
            self.position[1] += 1

        # Check for reward collection
        self.collect_reward(grid)

    def collect_reward(self, grid):
        """Check if the sprite's current position matches a reward block."""
        if tuple(self.position) in grid.rewards:
            grid.rewards.remove(tuple(self.position))  # Remove reward from grid
            self.collected_rewards += 1  # Increase collected reward count

    def draw(self, screen):
        character_x = self.position[1] * self.cell_size + self.cell_size // 2
        character_y = self.position[0] * self.cell_size + self.cell_size // 2
        pygame.draw.circle(screen, BLACK, (character_x, character_y), self.cell_size // 3)
