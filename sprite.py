import pygame
import random
import numpy as np

BLACK = (0, 0, 0)
ACTIONS = ['up', 'down', 'left', 'right']

class BaseSprite:
    def __init__(self, start_pos, cell_size):
        self.position = start_pos  # Position in the grid
        self.cell_size = cell_size

    def move(self, action, grid_size):
        row, col = self.position
        if action == "up" and row > 0:
            self.position[0] -= 1
        elif action == "down" and row < grid_size - 1:
            self.position[0] += 1
        elif action == "left" and col > 0:
            self.position[1] -= 1
        elif action == "right" and col < grid_size - 1:
            self.position[1] += 1

    def draw(self, screen):
        character_x = self.position[1] * self.cell_size + self.cell_size // 2
        character_y = self.position[0] * self.cell_size + self.cell_size // 2
        pygame.draw.circle(screen, BLACK, (character_x, character_y), self.cell_size // 3)


class DijkstraSprite(BaseSprite):
    def __init__(self, start_pos, cell_size):
        super().__init__(start_pos, cell_size)
        self.path = []  # Store the path for Dijkstra's algorithm

    def set_path(self, path):
        self.path = path

    def follow_path(self):
        if self.path:
            self.position = self.path.pop(0)


class QLearningSprite(BaseSprite):
    def __init__(self, start_pos, cell_size, grid_size):
        super().__init__(start_pos, cell_size)
        self.grid_size = grid_size
        self.q_table = {}  # Initialize Q-table for learning
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.epsilon = 0.1  # Exploration rate
        self.collected_rewards = 0

    def choose_action(self):
        state = tuple(self.position)
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(ACTIONS)
        return max(self.q_table.get(state, {}), key=self.q_table.get(state, {}).get, default=random.choice(ACTIONS))

    def update_q_value(self, old_state, action, reward, new_state):
        if old_state not in self.q_table:
            self.q_table[old_state] = {a: 0 for a in ACTIONS}
        if new_state not in self.q_table:
            self.q_table[new_state] = {a: 0 for a in ACTIONS}

        old_q_value = self.q_table[old_state][action]
        max_future_q = max(self.q_table[new_state].values())
        new_q_value = old_q_value + self.learning_rate * (reward + self.discount_factor * max_future_q - old_q_value)

        self.q_table[old_state][action] = new_q_value

    def take_step(self, grid):
        old_state = tuple(self.position)
        action = self.choose_action()
        self.move(action, self.grid_size)
        new_state = tuple(self.position)

        reward = 0
        if new_state in grid.rewards:
            reward = 10
            grid.rewards.remove(new_state)
            self.collected_rewards += 1
        elif grid.is_wall(new_state[0], new_state[1]):
            reward = -10

        self.update_q_value(old_state, action, reward, new_state)
