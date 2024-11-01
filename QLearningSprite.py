import pygame
import random
import time  # For delays

BLACK = (0, 0, 0)
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

        reward = -1
        self.step_penalties += 1

        if new_state == (self.grid_size - 1, self.grid_size - 1):
            reward = 50
            self.goal_reached_count += 1
            if self.goal_reached_count >= 5:
                self.training_complete = True
                if not self.optimal_path:
                    self.compute_optimal_path(grid)
        elif new_state in grid.rewards:
            reward += 5
            self.collected_rewards += 5
            grid.rewards.remove(new_state)
        elif new_state in grid.punishments:
            reward -= 100
            self.position = [0, 0]

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
        current_position = (0, 0)
        self.optimal_path = [current_position]

        while current_position != (self.grid_size - 1, self.grid_size - 1):
            if current_position not in self.q_table:
                break

            best_action = max(
                ((action, q_value) for action, q_value in self.q_table[current_position].items()
                 if self.is_valid_move(current_position, action) and not self.will_hit_wall(current_position, action, grid)),
                key=lambda x: x[1],
                default=(None, None)
            )[0]

            if not best_action:
                break

            next_position = self.get_next_position(current_position, best_action)
            self.optimal_path.append(next_position)
            current_position = next_position

    def is_valid_move(self, position, action):
        row, col = position
        if action == "up" and row > 0:
            return True
        elif action == "down" and row < self.grid_size - 1:
            return True
        elif action == "left" and col > 0:
            return True
        elif action == "right" and col < self.grid_size - 1:
            return True
        return False

    def will_hit_wall(self, position, action, grid):
        row, col = self.get_next_position(position, action)
        return grid.is_wall(row, col)

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
            pygame.time.delay(200)

    def draw(self, screen):
        x = self.position[1] * self.cell_size + self.cell_size // 2
        y = self.position[0] * self.cell_size + self.cell_size // 2
        pygame.draw.circle(screen, BLACK, (x, y), self.cell_size // 3)
