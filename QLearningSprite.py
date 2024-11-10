import numpy as np
import random
import time
import pygame

class QLearningSprite:
    def __init__(self, start_position, cell_size, rows, cols, alpha=0.5, gamma=0.99, epsilon=0.1, max_steps=1000):
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
        self.max_steps = max_steps  # Maximum number of steps allowed for exploration
        self.goal_position = [rows - 1, cols - 1]  # Bottom-right corner as the goal
        self.previous_position = None  # Track the previous position
        self.previous_action = None  # Track the previous action

    def reset(self):
        self.position = [0, 0]
        self.collected_rewards = 0
        self.step_penalties = 0
        self.training_complete = False
        self.is_exploring = True
        self.current_steps = 0
        self.previous_position = None
        self.previous_action = None

    def position_to_state(self):
        return self.position[0] * self.cols + self.position[1]

    def select_action(self, state):
        if random.random() < self.epsilon:
            return random.randint(0, 3)  # Random action: 0=up, 1=right, 2=down, 3=left
        else:
            return np.argmax(self.q_table[state])

    def take_step(self, grid):
        if self.training_complete:
            self.follow_policy(grid)
            return

        if self.current_steps >= self.max_steps:
            self.training_complete = True
            self.is_exploring = False
            self.position = [0, 0]  # Reset position to the start
            self.current_steps = 0  # Reset step counter for policy following
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

            # Calculate new position
            new_row = self.position[0] + moves[action][0]
            new_col = self.position[1] + moves[action][1]

            # Check if the move is valid
            if 0 <= new_row < self.rows and 0 <= new_col < self.cols and not grid.is_wall(new_row, new_col):
                new_position = [new_row, new_col]
                
                # Add a penalty for oscillation (repeating movement back and forth)
                if new_position == self.previous_position:
                    reward = -10  # Penalty for oscillating
                    self.q_table[state][action] += self.alpha * (reward - self.q_table[state][action])  # Update Q-table
                    print(f"Oscillation detected: Returning to previous position {new_position}. Penalty applied: {reward}")
                    continue  # Select a different action
                
                self.previous_position = self.position[:]  # Track previous position
                self.position = new_position
                valid_move = True
            else:
                # Apply penalty for invalid action
                reward = -5
                self.q_table[state][action] += self.alpha * (reward - self.q_table[state][action])  # Update Q-table
                print(f"Invalid move attempted from {self.position} with action {action}. Penalty applied: {reward}")

        # Apply default step penalty for valid moves
        reward = -1  # Default penalty for each step

        # Get new state regardless of reaching the goal or not
        new_state = self.position_to_state()

        if self.position == self.goal_position:
            reward = 150
            print("Goal reached during exploration! High reward given.")
        else:
            reward += grid.get_reward(self.position)  # Incorporate additional reward/punishment

        # Q-Learning update
        best_next_action = np.max(self.q_table[new_state])
        self.q_table[state][action] += self.alpha * (reward + self.gamma * best_next_action - self.q_table[state][action])

        self.current_steps += 1
        print(f"Step counter: {self.current_steps}, Reward: {reward}")


    def follow_policy(self, grid):
        # Check if the goal position is reached
        if self.position == self.goal_position:
            print("Goal reached during policy following. Stopping movement.")
            return  # End the function if the goal is reached

        state = self.position_to_state()
        action = np.argmax(self.q_table[state])  # Follow the optimal policy
        
        moves = {
            0: (-1, 0),  # Up
            1: (0, 1),   # Right
            2: (1, 0),   # Down
            3: (0, -1)   # Left
        }

        new_row = self.position[0] + moves[action][0]
        new_col = self.position[1] + moves[action][1]

        if 0 <= new_row < self.rows and 0 <= new_col < self.cols and not grid.is_wall(new_row, new_col):
            self.previous_position = self.position[:]  # Track previous position
            self.position = [new_row, new_col]
            print(f"Moved to new position: {self.position}")
        else:
            print(f"Invalid move attempted from {self.position} with action {action}. Staying in place.")

        time.sleep(1)  # Slow down for visualization during policy following


    def draw(self, screen):
        sprite_color = (0, 0, 255)  # Blue color
        x, y = self.position[1] * self.cell_size + self.cell_size // 2, self.position[0] * self.cell_size + self.cell_size // 2
        pygame.draw.circle(screen, sprite_color, (x, y), self.cell_size // 3)
