import numpy as np
import random
import time
import pygame
from screens.explanations.oscillation_explanation import OscillationExplanation
from screens.explanations.many_steps_explanation import ManyStepsExplanation
from screens.explanations.invalid_move_explanation import InvalidMoveExplanation
from screens.ending_scene import EndingScene

RED = (255, 0, 0)

class QLearningSprite:
    def __init__(self, start_position, cell_size, rows, cols, alpha=0.2, gamma=0.5, epsilon=0.9, max_steps=1000, oscillation_callback=None, retry_callback=None, screen=None):
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
        self.state = "normal"  # Possible states: "normal", "crashed", "caught"
        self.current_message = ""
        self.step_message = ""
        self.oscillation_count = 0
        self.oscillation_callback = oscillation_callback
        self.retry_callback = retry_callback
        self.policy_steps = 0
        self.screen = screen

        # Load images for the sprite states
        self.images = {
            "normal": pygame.image.load("sprites/deer_normal.png"),
            "crashed": pygame.image.load("sprites/deer_crashed.png"),
            "caught": pygame.image.load("sprites/deer_caught.png"),
        }
        # Scale images to fit the cell size
        for key in self.images:
            self.images[key] = pygame.transform.scale(self.images[key], (self.cell_size, self.cell_size))

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
        self.state = "normal"

    def position_to_state(self):
        return self.position[0] * self.cols + self.position[1]

    def select_action(self, state):
        return random.randint(0, 3) if random.random() < self.epsilon else np.argmax(self.q_table[state])

    def take_step(self, grid):
        """Perform one step in the environment."""
        if self.training_complete:
            self.follow_policy(grid)
            return

        if self.current_steps >= self.max_steps:
            self.training_complete = True
            self.position = [0, 0]
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
                    self.q_table[state][action] += self.alpha * (-5 - self.q_table[state][action])
                    self.add_message(f"Oscillation detected. Penalty applied.")
                    continue

                if grid.maze[new_row][new_col] == RED:
                    self.q_table[state][action] += self.alpha * (-150 - self.q_table[state][action])
                    self.add_message(f"Moved onto a red block. Heavy penalty applied.")
                    self.state = "crashed"  # Set sprite to crashed state
                else:
                    self.state = "normal"  # Reset sprite to normal state

                self.previous_position = self.position[:]
                self.position = new_position
                valid_move = True
                self.add_message(f"Step Count: {self.current_steps}.", is_step_message=True)
            else:
                self.q_table[state][action] += self.alpha * (-100 - self.q_table[state][action])
                self.add_message(f"Invalid move attempted. Heavy penalty applied.")

        reward = grid.get_reward(self.position)
        if self.position == self.goal_position:
            self.state = "caught"  # Set sprite to caught state
        else:
            self.state = "normal"  # Reset sprite to normal state

        new_state = self.position_to_state()
        best_next_action = np.max(self.q_table[new_state])
        self.q_table[state][action] += self.alpha * (reward + self.gamma * best_next_action - self.q_table[state][action])
        self.current_steps += 1

    def follow_policy(self, grid):
        if self.position == self.goal_position:
            self.state = "caught"  # Replace YELLOW with 'caught' state
            self.add_message("Goal reached during policy following.")
            time.sleep(2)
            self.trigger_ending_screen()
            return

        self.policy_steps += 1

        if self.policy_steps >= 25:  # Detect when steps exceed 5 during policy following
            self.trigger_many_steps_explanation()
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

            # Check for oscillation
            if len(self.recent_positions) > 2 and self.position in self.recent_positions[-2:]:
                self.oscillation_count += 1
                self.add_message("Oscillation detected during policy following.")
                self.state = "crashed"  # Replace RED with 'crashed' state

                # Check if oscillation count exceeds threshold
                if self.oscillation_count > 3:
                    self.trigger_oscillation_explanation()
            else:
                self.oscillation_count = 0  # Reset count if no oscillation detected

            self.recent_positions.append(self.position[:])
            if len(self.recent_positions) > 10:  # Limit the size of the recent positions list
                self.recent_positions.pop(0)

            self.add_message(f"Moved to new position: {self.position}")
        else:
            # Invalid move detected during policy following
            self.add_message(f"Invalid move attempted from {self.position} with action {action}. Staying in place.")
            self.state = "crashed"  # Replace RED with 'crashed' state
            self.trigger_invalid_move_explanation()  # Call the explanation screen for invalid moves
            time.sleep(1)  # Flash 'crashed' state for invalid moves during policy following

        time.sleep(0.5)


    def draw_q_values_on_grid(self, screen):
        font = pygame.font.Font('./fonts/PressStart2P-Regular.ttf', 12)
        offsets = [(0, -self.cell_size // 4), (self.cell_size // 4, 0), (0, self.cell_size // 4), (-self.cell_size // 4, 0)]
        for row in range(self.rows):
            for col in range(self.cols):
                state = row * self.cols + col
                q_values = self.q_table[state]
                rounded_q_values = [round(value, 1) for value in q_values]

                cell_x = col * self.cell_size
                cell_y = row * self.cell_size
                center_x = cell_x + self.cell_size // 2
                center_y = cell_y + self.cell_size // 2

                for i, q_value in enumerate(rounded_q_values):
                    text_surface = font.render(f"{q_value:.1f}", True, (0, 0, 0))
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

        if self.step_message:
            wrapped_lines = self.wrap_text(self.step_message, font, max_width)
            for line in wrapped_lines:
                text_surface = font.render(line, True, (255, 255, 255))
                screen.blit(text_surface, (10, y_offset))
                y_offset += 20

        if self.current_message:
            wrapped_lines = self.wrap_text(self.current_message, font, max_width)
            for line in wrapped_lines:
                text_surface = font.render(line, True, (255, 255, 255))
                screen.blit(text_surface, (10, y_offset))
                y_offset += 20

    def draw(self, screen, grid):
        image = self.images[self.state]
        x = self.position[1] * self.cell_size
        y = self.position[0] * self.cell_size
        screen.blit(image, (x, y))
        self.draw_q_values_on_grid(screen)
        self.draw_message(screen)

    def trigger_ending_screen(self):
        ending_screen = EndingScene(self.screen, self.retry_callback, user_score=100)
        ending_screen.run()

    def trigger_oscillation_explanation(self):
        explanation_screen = OscillationExplanation(self.screen, self.retry_callback)
        explanation_screen.run()

    def trigger_many_steps_explanation(self):
        explanation_screen = ManyStepsExplanation(self.screen, self.retry_callback)
        explanation_screen.run()

    def trigger_invalid_move_explanation(self):
        explanation_screen = InvalidMoveExplanation(self.screen, self.retry_callback)
        explanation_screen.run()

# import numpy as np
# import random
# import time
# import pygame
# from screens.explanations.oscillation_explanation import OscillationExplanation
# from screens.explanations.many_steps_explanation import ManyStepsExplanation
# from screens.explanations.invalid_move_explanation import InvalidMoveExplanation
# from screens.ending_scene import EndingScene


# RED = (255, 0, 0)
# BLACK = (0, 0, 0)

# class QLearningSprite:
#     def __init__(self, start_position, cell_size, rows, cols, alpha=0.2, gamma=0.5, epsilon=0.9, max_steps=1000, oscillation_callback=None, retry_callback=None, screen=None):
#         self.position = start_position
#         self.cell_size = cell_size
#         self.rows = rows
#         self.cols = cols
#         self.alpha = alpha
#         self.gamma = gamma
#         self.epsilon = epsilon
#         self.q_table = np.zeros((rows * cols, 4))  # 4 possible actions: up, right, down, left
#         self.training_complete = False
#         self.collected_rewards = 0
#         self.step_penalties = 0
#         self.current_steps = 0
#         self.max_steps = max_steps
#         self.goal_position = [rows - 1, cols - 1]
#         self.previous_position = None
#         self.recent_positions = []
#         self.state = "normal"  # Possible states: "normal", "crashed", "caught"
#         self.current_message = ""  # For displaying messages
#         self.step_message = ""  # For displaying step count messages
#         self.oscillation_count = 0  # Count number of oscillations
#         self.oscillation_callback = oscillation_callback  # Store the callback
#         self.screen = screen
#         self.retry_callback = retry_callback
#         self.oscillation_detected = False  # Flag to indicate if oscillation was detected
#         self.policy_steps = 0

#         # Load images
#         self.images = {
#             "normal": pygame.image.load("deer_normal.png"),
#             "crashed": pygame.image.load("deer_crashed.png"),
#             "caught": pygame.image.load("deer_caught.png")
#         }

#         # Scale images to fit the cell size
#         for key in self.images:
#             self.images[key] = pygame.transform.scale(self.images[key], (self.cell_size, self.cell_size))


#     def add_message(self, message, is_step_message=False):
#         if is_step_message:
#             self.step_message = message
#         else:
#             self.current_message = message

#     def reset(self):
#         self.position = [0, 0]
#         self.collected_rewards = 0
#         self.step_penalties = 0
#         self.training_complete = False
#         self.q_table = np.zeros((self.rows * self.cols, 4))
#         self.current_steps = 0
#         self.previous_position = None
#         self.recent_positions.clear()
#         self.color = BLACK  # Reset color to default

#     def position_to_state(self):
#         return self.position[0] * self.cols + self.position[1]

#     def select_action(self, state):
#         return random.randint(0, 3) if random.random() < self.epsilon else np.argmax(self.q_table[state])

   
    # def follow_policy(self, grid):
    #     if self.position == self.goal_position:
    #         self.color = YELLOW
    #         self.add_message("Goal reached during policy following.")
    #         time.sleep(2)
    #         self.trigger_ending_screen()
    #         return

    #     self.policy_steps = self.policy_steps+1
        
    #     if self.policy_steps >= 5:  # Detect when steps exceed 50 during policy following
    #         self.trigger_many_steps_explanation()
    #         return
        
    #     state = self.position_to_state()
    #     action = np.argmax(self.q_table[state])  # Choose the action with the highest Q-value

    #     moves = {
    #         0: (-1, 0),  # Up
    #         1: (0, 1),   # Right
    #         2: (1, 0),   # Down
    #         3: (0, -1)   # Left
    #     }

    #     new_row = self.position[0] + moves[action][0]
    #     new_col = self.position[1] + moves[action][1]

    #     if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
    #         self.previous_position = self.position[:]  # Store the previous position
    #         self.position = [new_row, new_col]  # Move to the new position
            
    #         # Check for oscillation
    #         if len(self.recent_positions) > 2 and self.position in self.recent_positions[-2:]:
    #             self.oscillation_count += 1
    #             self.add_message("Oscillation detected during policy following.")
    #             self.color = RED  # Optionally change color to indicate oscillation

    #             # Check if oscillation count exceeds threshold
    #             if self.oscillation_count > 3:
    #                 self.trigger_oscillation_explanation()
    #         else:
    #             self.oscillation_count = 0  # Reset count if no oscillation detected

    #         self.recent_positions.append(self.position[:])
    #         if len(self.recent_positions) > 10:  # Limit the size of the recent positions list
    #             self.recent_positions.pop(0)

    #         self.add_message(f"Moved to new position: {self.position}")
    #     else:
    #         # Invalid move detected during policy following
    #         self.add_message(f"Invalid move attempted from {self.position} with action {action}. Staying in place.")
    #         self.color = RED
    #         self.trigger_invalid_move_explanation()  # Call the explanation screen for invalid moves
    #         time.sleep(1)  # Flash red for invalid moves during policy following

    #     time.sleep(0.5)

#     def draw_q_values_on_grid(self, screen):
#         font = pygame.font.Font('./fonts/PressStart2P-Regular.ttf', 12)  # Retro font
#         offsets = [(0, -self.cell_size // 4), (self.cell_size // 4, 0), (0, self.cell_size // 4), (-self.cell_size // 4, 0)]  # Positions for up, right, down, left

#         for row in range(self.rows):
#             for col in range(self.cols):
#                 state = row * self.cols + col
#                 q_values = self.q_table[state]
                
#                 # Round the Q-values to 1 decimal place
#                 rounded_q_values = [round(value, 1) for value in q_values]

#                 cell_x = col * self.cell_size
#                 cell_y = row * self.cell_size
#                 center_x = cell_x + self.cell_size // 2
#                 center_y = cell_y + self.cell_size // 2

#                 for i, q_value in enumerate(rounded_q_values):
#                     # Display only the rounded Q-value, without the direction
#                     text_surface = font.render(f"{q_value:.1f}", True, (0, 0, 0))  # Display with 1 decimal place
#                     text_rect = text_surface.get_rect(center=(center_x + offsets[i][0], center_y + offsets[i][1]))
#                     screen.blit(text_surface, text_rect)

#     def wrap_text(self, text, font, max_width):
#         words = text.split(' ')
#         lines = []
#         while words:
#             line = ''
#             while words and font.size(line + words[0])[0] <= max_width:
#                 line += words.pop(0) + ' '
#             lines.append(line.strip())
#         return lines

#     def draw_message(self, screen):
#         font = pygame.font.Font('./fonts/PressStart2P-Regular.ttf', 8)
#         max_width = screen.get_width() - 20
#         y_offset = screen.get_height() - 50

#         # Draw step message if available
#         if self.step_message:
#             wrapped_lines = self.wrap_text(self.step_message, font, max_width)
#             for line in wrapped_lines:
#                 text_surface = font.render(line, True, (255, 255, 255))
#                 screen.blit(text_surface, (10, y_offset))
#                 y_offset += 20

#         # Draw current message if available
#         if self.current_message:
#             wrapped_lines = self.wrap_text(self.current_message, font, max_width)
#             for line in wrapped_lines:
#                 text_surface = font.render(line, True, (255, 255, 255))
#                 screen.blit(text_surface, (10, y_offset))
#                 y_offset += 20

#     def draw(self, screen, grid):
#         # Draw the sprite
#         x, y = self.position[1] * self.cell_size + self.cell_size // 2, self.position[0] * self.cell_size + self.cell_size // 2
#         pygame.draw.circle(screen, self.color, (x, y), self.cell_size // 3)

#         # Draw the Q-values on the grid cells
#         self.draw_q_values_on_grid(screen)

#         # Draw the current message at the bottom of the screen
#         self.draw_message(screen)

    
#     def trigger_ending_screen(self):
#         ending_screen = EndingScene(self.screen, self.retry_callback, user_score=100)
#         ending_screen.run()  # Pass the retry callback when running

#     def trigger_oscillation_explanation(self):
#         explanation_screen = OscillationExplanation(self.screen, self.retry_callback)
#         explanation_screen.run()  # Pass the retry callback when running

#     def trigger_many_steps_explanation(self):
#         explanation_screen = ManyStepsExplanation(self.screen, self.retry_callback)
#         explanation_screen.run() 

#     def trigger_invalid_move_explanation(self):
#         explanation_screen = InvalidMoveExplanation(self.screen, self.retry_callback)
#         explanation_screen.run()  # Pass the retry callback when running
