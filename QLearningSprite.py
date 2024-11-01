import pygame
import random
import time

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
ACTIONS = ['up', 'down', 'left', 'right']

class QLearningSprite:
    def __init__(self, start_pos, cell_size, grid_size):
        self.position = start_pos
        self.cell_size = cell_size
        self.grid_size = grid_size
        self.q_table = {}
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.epsilon = 0.1
        self.collected_rewards = 0
        self.step_penalties = 0
        self.training_complete = False
        self.optimal_path = []
        self.goal_reached_count = 0
        self.is_exploring = False

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
        max_future_q = max(self.q_table[new_state].values(), default=0)
        new_q_value = old_q_value + self.learning_rate * (reward + self.discount_factor * max_future_q - old_q_value)
        self.q_table[old_state][action] = new_q_value

    def take_step(self, grid):
        if self.training_complete:
            return

        old_state = tuple(self.position)
        action = self.choose_action()
        self.move(action, grid)
        new_state = tuple(self.position)

        reward = -1  # Default penalty for each step
        self.step_penalties += 1

        if new_state == (self.grid_size - 1, self.grid_size - 1):  # Final goal
            reward = 50
            self.goal_reached_count += 1
            if self.goal_reached_count >= 5:  # Repeat enough to stabilize training
                self.training_complete = True
                self.is_exploring = False  # Disable exploring during optimal path calculation
                if not self.optimal_path:
                    self.compute_optimal_path(grid)  # Compute path for exploration phase
        elif new_state in grid.rewards:
            reward += 5
            self.collected_rewards += 5
            grid.rewards.remove(new_state)
        elif new_state in grid.punishments:
            reward -= 100
            self.position = [0, 0]  # Reset to start if a wall is hit

        self.update_q_value(old_state, action, reward, new_state)

    def move(self, action, grid):
        row, col = self.position
        if action == "up" and row > 0 and not grid.is_wall(row - 1, col):
            self.position[0] -= 1
        elif action == "down" and row < self.grid_size - 1 and not grid.is_wall(row + 1, col):
            self.position[0] += 1
        elif action == "left" and col > 0 and not grid.is_wall(row, col - 1):
            self.position[1] -= 1
        elif action == "right" and col < self.grid_size - 1 and not grid.is_wall(row, col + 1):
            self.position[1] += 1

    def compute_optimal_path(self, grid):
        if not self.training_complete:
            return

        current_position = (0, 0)  # Start from initial position
        self.optimal_path = [current_position]
        visited_positions = set()
        max_steps = self.grid_size * self.grid_size

        while current_position != (self.grid_size - 1, self.grid_size - 1):
            if current_position in visited_positions or len(self.optimal_path) > max_steps:
                break

            visited_positions.add(current_position)

            if current_position in self.q_table:
                best_action = max(self.q_table[current_position], key=self.q_table[current_position].get)
            else:
                best_action = None

            if not best_action:
                break

            next_position = self.get_next_position(current_position, best_action)
            if grid.is_wall(*next_position) or next_position in visited_positions:
                break

            self.optimal_path.append(next_position)
            current_position = next_position

        if current_position == (self.grid_size - 1, self.grid_size - 1):
            print("Reached goal during exploration; path will reset.")

    def get_next_position(self, position, action):
        row, col = position
        if action == "up":
            return (row - 1, col)
        elif action == "down":
            return (row + 1, col)
        elif action == "left":
            return (row, col - 1)
        elif action == "right":
            return (row, col + 1)
        return position

    def follow_optimal_path(self):
        if self.optimal_path:
            self.position = self.optimal_path.pop(0)
            pygame.time.delay(200)  # Slow down movement for visualization

    def draw(self, screen):
        color = BLUE if self.is_exploring else BLACK  # Blue when exploring
        x = self.position[1] * self.cell_size + self.cell_size // 2
        y = self.position[0] * self.cell_size + self.cell_size // 2
        pygame.draw.circle(screen, color, (x, y), self.cell_size // 3)
