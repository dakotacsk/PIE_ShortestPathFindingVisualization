# grid.py
import pygame
import random

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

class Grid:
    def __init__(self, grid_size, cell_size):
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.maze = [[0] * grid_size for _ in range(grid_size)]  # 0 = empty, 1 = wall
        self.rewards = []  # List to store reward positions

    def toggle_wall(self, pos):
        row, col = pos[1] // self.cell_size, pos[0] // self.cell_size
        self.maze[row][col] = 1 if self.maze[row][col] == 0 else 0  # Toggle between wall (1) and empty (0)

    def is_wall(self, row, col):
        return self.maze[row][col] == 1

    def place_rewards(self, num_rewards):
        """Place a specified number of rewards randomly on the grid."""
        self.rewards = []  # Clear any existing rewards
        for _ in range(num_rewards):
            while True:
                row = random.randint(0, self.grid_size - 1)
                col = random.randint(0, self.grid_size - 1)
                if self.maze[row][col] == 0 and (row, col) not in self.rewards:  # Place only on empty cells
                    self.rewards.append((row, col))
                    break

    def draw(self, screen):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                rect = pygame.Rect(col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
                if (row, col) in self.rewards:
                    pygame.draw.rect(screen, GREEN, rect)  # Draw reward blocks
                elif self.maze[row][col] == 1:
                    pygame.draw.rect(screen, RED, rect)
                else:
                    pygame.draw.rect(screen, WHITE, rect)
                pygame.draw.rect(screen, BLACK, rect, 1)  # Border
