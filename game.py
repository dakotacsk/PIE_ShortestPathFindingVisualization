import pygame
import sys
import time
from grid import Grid
from DijkstraSprite import DijkstraSprite
from QLearningSprite import QLearningSprite

GRID_ROWS = 5
GRID_COLS = 8  # Example of a rectangular grid
CELL_SIZE = 500 / max(GRID_ROWS, GRID_COLS)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((CELL_SIZE * GRID_COLS, CELL_SIZE * GRID_ROWS + 120))
        pygame.display.set_caption("Algorithm Simulation")
        self.grid = Grid(GRID_ROWS, GRID_COLS, CELL_SIZE)
        self.dijkstra_sprite = DijkstraSprite([0, 0], CELL_SIZE, self.grid)
        self.qlearning_sprite = QLearningSprite([0, 0], CELL_SIZE, GRID_ROWS, GRID_COLS)
        self.current_sprite = self.qlearning_sprite  # Start with Q-learning as default
        self.running = False
        self.font = pygame.font.SysFont("Arial", 20)
        self.clock = pygame.time.Clock()
        self.exploration_complete = False  # Track if exploration is complete

        # Dropdown menu for selecting algorithms
        self.algorithms = ["Dijkstra", "Q-learning"]
        self.selected_algorithm = self.algorithms[1]  # Default to Q-learning
        self.dropdown_active = False

    def handle_buttons(self, pos):
        # Start button
        if 10 <= pos[0] <= 110 and GRID_ROWS * CELL_SIZE + 10 <= pos[1] <= GRID_ROWS * CELL_SIZE + 40:
            if self.exploration_complete:
                self.reset_simulation()  # If exploration is complete, behave like reset
            else:
                self.start_simulation()

    def start_simulation(self):
        start = (0, 0)
        end = (GRID_ROWS - 1, GRID_COLS - 1)
        if self.selected_algorithm == "Dijkstra":
            self.current_sprite = self.dijkstra_sprite
            self.dijkstra_sprite.set_path(start, end)
        elif self.selected_algorithm == "Q-learning":
            self.current_sprite = self.qlearning_sprite
        self.running = True

    def reset_simulation(self):
        self.grid.reset_rewards_and_punishments()  # Reset grid rewards/punishments
        self.dijkstra_sprite.position = [0, 0]
        self.qlearning_sprite.reset()  # Hard reset the Q-learning agent
        self.running = False
        self.exploration_complete = False  # Reset exploration state

    def display_message(self, text):
        message = self.font.render(text, True, BLACK)
        self.screen.blit(message, (10, GRID_ROWS * CELL_SIZE + 50))

    def draw(self):
        self.screen.fill(WHITE)
        self.grid.draw(self.screen)
        self.current_sprite.draw(self.screen)

        # Draw the Start button
        pygame.draw.rect(self.screen, BLUE, (10, GRID_ROWS * CELL_SIZE + 10, 100, 30))
        self.screen.blit(self.font.render("Start", True, WHITE), (20, GRID_ROWS * CELL_SIZE + 15))

        # Draw dropdown for algorithm selection next to Start
        pygame.draw.rect(self.screen, (150, 150, 150), (130, GRID_ROWS * CELL_SIZE + 10, 150, 30))
        self.screen.blit(self.font.render(self.selected_algorithm, True, BLACK), (140, GRID_ROWS * CELL_SIZE + 15))
        if self.dropdown_active:
            for i, option in enumerate(self.algorithms):
                option_rect = pygame.Rect(130, GRID_ROWS * CELL_SIZE + 10 + (i + 1) * 30, 150, 30)
                pygame.draw.rect(self.screen, (100, 100, 100), option_rect)
                self.screen.blit(self.font.render(option, True, WHITE), (140, GRID_ROWS * CELL_SIZE + 15 + (i + 1) * 30))

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if mouse_pos[1] < GRID_ROWS * CELL_SIZE:
                    self.grid.toggle_cell(mouse_pos)  # Toggle cell color/state
                else:
                    self.handle_buttons(mouse_pos)
                    # Check if dropdown is clicked
                    if 130 <= mouse_pos[0] <= 280 and GRID_ROWS * CELL_SIZE + 10 <= mouse_pos[1] <= GRID_ROWS * CELL_SIZE + 40:
                        self.dropdown_active = not self.dropdown_active
                    elif self.dropdown_active:
                        for i, option in enumerate(self.algorithms):
                            option_rect = pygame.Rect(130, GRID_ROWS * CELL_SIZE + 10 + (i + 1) * 30, 150, 30)
                            if option_rect.collidepoint(mouse_pos):
                                self.selected_algorithm = option
                                self.dropdown_active = False
                                break

    def update(self):
        if self.running:
            if self.selected_algorithm == "Dijkstra":
                # Run Dijkstra's algorithm
                self.dijkstra_sprite.follow_path()
                time.sleep(0.1)
                if not self.dijkstra_sprite.path:
                    self.running = False
            elif self.selected_algorithm == "Q-learning":
                # Q-learning training or policy following
                self.qlearning_sprite.take_step(self.grid)
                # Check if exploration is complete
                if self.qlearning_sprite.training_complete:
                    self.exploration_complete = True

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
