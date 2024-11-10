import numpy as np
import random
import time
import pygame

RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

class QLearningSprite:
    def __init__(self, start_position, cell_size, rows, cols, alpha=0.2, gamma=0.99, epsilon=0.6, max_steps=5000):
        self.position = start_position
        self.cell_size = cell_size
        self.rows = rows
        self.cols = cols
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = np.zeros((rows * cols, 4))  # 4 possible actions: up, right, down, left
        self.training_complete = False
        self.is_exploring = True
        self.collected_rewards = 0
        self.step_penalties = 0
        self.current_steps = 0
        self.max_steps = max_steps
        self.goal_position = [rows - 1, cols - 1]
        self.previous_position = None
        self.previous_action = None
        self.recent_positions = []
        self.color = BLACK

    def reset(self):
        self.position = [0, 0]
        self.collected_rewards = 0
        self.step_penalties = 0
        self.training_complete = False
        self.is_exploring = True
        self.q_table = np.zeros((self.rows * self.cols, 4))  # 4 possible actions: up, right, down, left
        self.current_steps = 0
        self.previous_position = None
        self.previous_action = None
        self.recent_positions.clear()
        self.color = BLACK  # Reset color to default

    def position_to_state(self):
        return self.position[0] * self.cols + self.position[1]

    def select_action(self, state):
        return random.randint(0, 3) if random.random() < self.epsilon else np.argmax(self.q_table[state])

    def apply_penalty(self, state, action, penalty):
        """Apply penalty to the Q-table for a given action."""
        self.q_table[state][action] += self.alpha * (penalty - self.q_table[state][action])

    def take_step(self, grid):
        if self.training_complete:
            self.follow_policy(grid)
            return

        if self.current_steps >= self.max_steps:
            self.training_complete = True
            self.is_exploring = False
            self.position = [0, 0]
            self.current_steps = 0
            print("Exploration limit reached. Switching to exploitation phase and resetting position.")
            return

        state = self.position_to_state()
        valid_move = False

        while not valid_move:
            action = self.select_action(state)

            moves = {
                0: (-1, 0),  # Up
                1: (0, 1),   # Right
                2: (1, 0),   # Down
                3: (0, -1)   # Left
            }

            new_row = self.position[0] + moves[action][0]
            new_col = self.position[1] + moves[action][1]
            new_position = [new_row, new_col]

            if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                if len(self.recent_positions) > 1 and new_position == self.recent_positions[-2]:
                    self.apply_penalty(state, action, -50)
                    print(f"Oscillation detected: Returning to previous position {new_position}. Penalty applied: -50")
                    continue
                
                if grid.maze[new_row][new_col] == RED:
                    self.apply_penalty(state, action, -500)
                    print(f"Moved onto a red block at {new_position}. Heavy penalty applied: -500")

                self.recent_positions.append(self.position[:])
                if len(self.recent_positions) > 10:
                    self.recent_positions.pop(0)

                self.previous_position = self.position[:]
                self.position = new_position
                valid_move = True
            else:
                self.apply_penalty(state, action, -15)
                print(f"Invalid move attempted from {self.position} with action {action}. Penalty applied: -15")

        reward = -1 # default step penalty
        reward += grid.get_reward(self.position)
        new_state = self.position_to_state()
        best_next_action = np.max(self.q_table[new_state])
        self.q_table[state][action] += self.alpha * (reward + self.gamma * best_next_action - self.q_table[state][action])

        self.current_steps += 1
        print(f"Step counter: {self.current_steps}, Reward: {reward}")

    def follow_policy(self, grid):
        if self.position == self.goal_position:
            self.color = YELLOW
            print("Goal reached during policy following.")
            return

        state = self.position_to_state()
        action = np.argmax(self.q_table[state])

        moves = {
            0: (-1, 0),  # Up
            1: (0, 1),   # Right
            2: (1, 0),   # Down
            3: (0, -1)   # Left
        }

        new_row = self.position[0] + moves[action][0]
        new_col = self.position[1] + moves[action][1]

        if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
            self.previous_position = self.position[:]
            self.position = [new_row, new_col]
            print(f"Moved to new position: {self.position}")
        else:
            print(f"Invalid move attempted from {self.position} with action {action}. Staying in place.")
            self.color = RED
            time.sleep(1)  # Flash red for invalid moves during policy following

        time.sleep(0.5)

    def draw(self, screen):
        x, y = self.position[1] * self.cell_size + self.cell_size // 2, self.position[0] * self.cell_size + self.cell_size // 2
        pygame.draw.circle(screen, self.color, (x, y), self.cell_size // 3)
