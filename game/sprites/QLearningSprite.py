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
        self.collected_rewards = 0
        self.step_penalties = 0
        self.current_steps = 0
        self.max_steps = max_steps
        self.goal_position = [rows - 1, cols - 1]
        self.previous_position = None
        self.recent_positions = []
        self.color = BLACK
        self.current_message = ""  # For displaying messages
        self.step_message = ""  # For displaying step count messages

    def add_message(self, message, is_step_message=False):
        if is_step_message:
            self.step_message = message
        else:
            self.current_message = message


    def reset(self):
        self.position = [0, 0]
        self.collected_rewards = 0
        self.step_penalties = 0
        self.training_complete = False
        self.q_table = np.zeros((self.rows * self.cols, 4))
        self.current_steps = 0
        self.previous_position = None
        self.recent_positions.clear()
        self.color = BLACK  # Reset color to default

    def position_to_state(self):
        return self.position[0] * self.cols + self.position[1]

    def select_action(self, state):
        return random.randint(0, 3) if random.random() < self.epsilon else np.argmax(self.q_table[state])

    def take_step(self, grid):
        if self.training_complete:
            self.follow_policy(grid)
            return

        if self.current_steps >= self.max_steps:
            self.training_complete = True
            self.position = [0, 0]
            self.current_steps = 0
            self.add_message("Exploration limit reached. Resetting position.")
            return

        state = self.position_to_state()
        valid_move = False

        while not valid_move:
            action = self.select_action(state)
            moves = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}  # Up, Right, Down, Left
            new_row = self.position[0] + moves[action][0]
            new_col = self.position[1] + moves[action][1]
            new_position = [new_row, new_col]

            if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                if len(self.recent_positions) > 1 and new_position == self.recent_positions[-2]:
                    self.q_table[state][action] += self.alpha * (-50 - self.q_table[state][action])
                    self.add_message(f"Oscillation detected. Penalty applied.")
                    continue

                if grid.maze[new_row][new_col] == RED:
                    self.q_table[state][action] += self.alpha * (-500 - self.q_table[state][action])
                    self.add_message(f"Moved onto a red block. Heavy penalty applied.")
                
                self.recent_positions.append(self.position[:])
                if len(self.recent_positions) > 10:
                    self.recent_positions.pop(0)

                self.previous_position = self.position[:]
                self.position = new_position
                valid_move = True
                self.add_message(f"Step Count: {self.current_steps}.", is_step_message=True)

            else:
                self.q_table[state][action] += self.alpha * (-15 - self.q_table[state][action])
                self.add_message(f"Invalid move attempted. Penalty applied.")

        reward = -1
        reward += grid.get_reward(self.position)
        new_state = self.position_to_state()
        best_next_action = np.max(self.q_table[new_state])
        self.q_table[state][action] += self.alpha * (reward + self.gamma * best_next_action - self.q_table[state][action])
        self.current_steps += 1

    def follow_policy(self, grid):
        if self.position == self.goal_position:
            self.color = YELLOW
            self.add_message("Goal reached during policy following.")
            return

        state = self.position_to_state()
        action = np.argmax(self.q_table[state])  # Choose the action with the highest Q-value

        moves = {
            0: (-1, 0),  # Up
            1: (0, 1),   # Right
            2: (1, 0),   # Down
            3: (0, -1)   # Left
        }

        new_row = self.position[0] + moves[action][0]
        new_col = self.position[1] + moves[action][1]

        if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
            self.previous_position = self.position[:]  # Store the previous position
            self.position = [new_row, new_col]  # Move to the new position
            self.add_message(f"Moved to new position: {self.position}")
        else:
            self.add_message(f"Invalid move attempted from {self.position} with action {action}. Staying in place.")
            self.color = RED
            time.sleep(1)  # Flash red for invalid moves during policy following

        time.sleep(0.5)

    def draw_q_values_on_grid(self, screen):
        font = pygame.font.Font('./fonts/PressStart2P-Regular.ttf', 8)  # Retro font
        offsets = [(0, -self.cell_size // 4), (self.cell_size // 4, 0), (0, self.cell_size // 4), (-self.cell_size // 4, 0)]  # Positions for up, right, down, left

        for row in range(self.rows):
            for col in range(self.cols):
                state = row * self.cols + col
                q_values = self.q_table[state]
                
                # Round the Q-values to 1 decimal place
                rounded_q_values = [round(value, 1) for value in q_values]

                cell_x = col * self.cell_size
                cell_y = row * self.cell_size
                center_x = cell_x + self.cell_size // 2
                center_y = cell_y + self.cell_size // 2

                for i, q_value in enumerate(rounded_q_values):
                    # Display only the rounded Q-value, without the direction
                    text_surface = font.render(f"{q_value:.1f}", True, (0, 0, 0))  # Display with 1 decimal place
                    text_rect = text_surface.get_rect(center=(center_x + offsets[i][0], center_y + offsets[i][1]))
                    screen.blit(text_surface, text_rect)



    def wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        while words:
            line = ''
            while words and font.size(line + words[0])[0] <= max_width:
                line += words.pop(0) + ' '
            lines.append(line.strip())
        return lines

    def draw_message(self, screen):
        font = pygame.font.Font('./fonts/PressStart2P-Regular.ttf', 8)
        max_width = screen.get_width() - 20
        y_offset = screen.get_height() - 50

        # Draw step message if available
        if self.step_message:
            wrapped_lines = self.wrap_text(self.step_message, font, max_width)
            for line in wrapped_lines:
                text_surface = font.render(line, True, (255, 255, 255))
                screen.blit(text_surface, (10, y_offset))
                y_offset += 20

        # Draw current message if available
        if self.current_message:
            wrapped_lines = self.wrap_text(self.current_message, font, max_width)
            for line in wrapped_lines:
                text_surface = font.render(line, True, (255, 255, 255))
                screen.blit(text_surface, (10, y_offset))
                y_offset += 20


    def draw(self, screen, grid):
        # Draw the sprite
        x, y = self.position[1] * self.cell_size + self.cell_size // 2, self.position[0] * self.cell_size + self.cell_size // 2
        pygame.draw.circle(screen, self.color, (x, y), self.cell_size // 3)

        # Draw the Q-values on the grid cells
        self.draw_q_values_on_grid(screen)

        # Draw the current message at the bottom of the screen
        self.draw_message(screen)


    