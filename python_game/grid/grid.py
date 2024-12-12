import pygame

RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (240, 230, 140)
BLUE = (30, 144, 255)


class Grid:
    def __init__(self, rows, cols, cell_size):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.maze = [[YELLOW] * cols for _ in range(rows)]
        self.maze[rows - 1][cols - 1] = BLUE
        self.rewards = set()  # Set of reward positions
        self.punishments = set()  # Set of punishment positions
        self.collected_rewards = set()  # Track collected rewards
        self.goal_position = (rows - 1, cols - 1)  # Define goal as bottom-right corner
        self.maze[rows - 1][cols - 1] = BLUE

    def toggle_cell(self, pos):
        # Use floor division to ensure row and col are integers
        row, col = pos[1] // self.cell_size, pos[0] // self.cell_size
        row, col = int(row), int(col)  # Explicitly cast to int for safety

        # Toggle cell color/state between reward, punishment, and default
        if (row, col) in self.rewards:
            self.rewards.remove((row, col))
            self.punishments.add((row, col))
            self.maze[row][col] = RED
        elif (row, col) in self.punishments:
            self.punishments.remove((row, col))
            self.maze[row][col] = YELLOW
        else:
            self.rewards.add((row, col))
            self.maze[row][col] = GREEN

    def is_wall(self, row, col):
        return self.maze[row][col] == RED

    def get_reward(self, position):
        position = tuple(position)  # Convert list to tuple
        if position == self.goal_position:
            return 150  # High reward for reaching the goal
        elif position in self.rewards:
            self.collected_rewards.add(position)  # Mark the reward as collected
            return 50  # Reward for stepping on a green block
        elif position in self.punishments:
            return -150
        else:
            return -1  # Default move penalty

    def reset_rewards_and_punishments(self):
        self.rewards.clear()
        self.punishments.clear()
        self.collected_rewards.clear()  # Clear collected rewards
        self.maze = [[YELLOW] * self.cols for _ in range(self.rows)]

    def draw(self, screen):
        for row in range(self.rows):
            for col in range(self.cols):
                rect = pygame.Rect(
                    col * self.cell_size,
                    row * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                pygame.draw.rect(screen, self.maze[row][col], rect)
                # pygame.draw.rect(screen, BLACK, rect, 1)  # Border
