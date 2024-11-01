import pygame

RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Grid:
    def __init__(self, grid_size, cell_size):
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.maze = [[WHITE] * grid_size for _ in range(grid_size)]
        self.rewards = set()
        self.punishments = set()

    def toggle_cell(self, pos):
        row, col = pos[1] // self.cell_size, pos[0] // self.cell_size
        if (row, col) in self.rewards:
            self.rewards.remove((row, col))
            self.punishments.add((row, col))
            self.maze[row][col] = RED
        elif (row, col) in self.punishments:
            self.punishments.remove((row, col))
            self.maze[row][col] = WHITE
        else:
            self.rewards.add((row, col))
            self.maze[row][col] = GREEN

    def is_wall(self, row, col):
        return self.maze[row][col] == RED

    def reset_rewards_and_punishments(self):
        self.rewards.clear()
        self.punishments.clear()
        self.maze = [[WHITE] * self.grid_size for _ in range(self.grid_size)]

    def draw(self, screen):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                rect = pygame.Rect(col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(screen, self.maze[row][col], rect)
                pygame.draw.rect(screen, BLACK, rect, 1)  # Border
