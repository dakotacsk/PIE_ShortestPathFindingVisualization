import pygame
import sys
import time
from grid import Grid
from DijkstraSprite import DijkstraSprite
from QLearningSprite import QLearningSprite

CELL_SIZE = 50
GRID_SIZE = 6
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((CELL_SIZE * GRID_SIZE, CELL_SIZE * GRID_SIZE + 120))
        pygame.display.set_caption("Algorithm Simulation")
        self.grid = Grid(GRID_SIZE, CELL_SIZE)
        self.dijkstra_sprite = DijkstraSprite([0, 0], CELL_SIZE, self.grid)
        self.qlearning_sprite = QLearningSprite([0, 0], CELL_SIZE, GRID_SIZE)
        self.current_sprite = self.qlearning_sprite  # Start with Q-learning as default
        self.running = False
        self.font = pygame.font.SysFont("Arial", 20)
        self.clock = pygame.time.Clock()
        self.training_complete = False
        self.exploration_started = False  # Track if exploration phase has started

        # Dropdown menu for selecting algorithms
        self.algorithms = ["Dijkstra", "Q-learning"]
        self.selected_algorithm = self.algorithms[1]  # Default to Q-learning
        self.dropdown_active = False

    def handle_buttons(self, pos):
        # Start button
        if 10 <= pos[0] <= 110 and GRID_SIZE * CELL_SIZE + 10 <= pos[1] <= GRID_SIZE * CELL_SIZE + 40:
            self.start_simulation()
        # Reset button
        elif 130 <= pos[0] <= 230 and GRID_SIZE * CELL_SIZE + 10 <= pos[1] <= GRID_SIZE * CELL_SIZE + 40:
            self.reset_simulation()
        # Done button for exploring with Q-learning (only visible after training completes)
        elif 370 <= pos[0] <= 470 and GRID_SIZE * CELL_SIZE + 10 <= pos[1] <= GRID_SIZE * CELL_SIZE + 40 and self.training_complete and not self.exploration_started:
            self.start_new_exploration()

    def start_simulation(self):
        start = (0, 0)
        end = (GRID_SIZE - 1, GRID_SIZE - 1)
        if self.selected_algorithm == "Dijkstra":
            self.current_sprite = self.dijkstra_sprite
            self.dijkstra_sprite.set_path(start, end)
        elif self.selected_algorithm == "Q-learning":
            self.current_sprite = self.qlearning_sprite
        self.running = True

    def reset_simulation(self):
        self.grid.reset_rewards_and_punishments()
        self.dijkstra_sprite.position = [0, 0]
        self.qlearning_sprite.position = [0, 0]
        self.qlearning_sprite.collected_rewards = 0
        self.qlearning_sprite.step_penalties = 0
        self.qlearning_sprite.training_complete = False
        self.qlearning_sprite.optimal_path = []
        self.qlearning_sprite.goal_reached_count = 0
        self.running = False
        self.training_complete = False
        self.exploration_started = False  # Reset exploration status

    def start_new_exploration(self):
        # Start exploration phase for Q-learning
        if self.training_complete:
            self.qlearning_sprite.position = [0, 0]  # Reset position to start at (0, 0)
            self.qlearning_sprite.is_exploring = True
            self.qlearning_sprite.compute_optimal_path(self.grid)  # Generate optimal path
            # Ensure the optimal path is valid
            if not self.qlearning_sprite.optimal_path:
                print("No valid optimal path found.")
                self.qlearning_sprite.is_exploring = False  # Stop exploration if no valid path
            self.current_sprite = self.qlearning_sprite
            self.running = True
            self.exploration_started = True  # Mark exploration as started

    def display_message(self, text):
        message = self.font.render(text, True, BLACK)
        self.screen.blit(message, (10, GRID_SIZE * CELL_SIZE + 50))

    def display_scores(self):
        # Show rewards and penalties only during Q-learning phases
        if self.selected_algorithm == "Q-learning":
            score_text = self.font.render(
                f"Rewards: {self.qlearning_sprite.collected_rewards} | Penalties: {self.qlearning_sprite.step_penalties}", 
                True, BLACK
            )
            self.screen.blit(score_text, (10, self.screen.get_height() - 30))

    def draw(self):
        self.screen.fill(WHITE)
        self.grid.draw(self.screen)
        self.current_sprite.draw(self.screen)

        # Draw the Start and Reset buttons
        pygame.draw.rect(self.screen, BLUE, (10, GRID_SIZE * CELL_SIZE + 10, 100, 30))
        self.screen.blit(self.font.render("Start", True, WHITE), (20, GRID_SIZE * CELL_SIZE + 15))
        pygame.draw.rect(self.screen, BLUE, (130, GRID_SIZE * CELL_SIZE + 10, 100, 30))
        self.screen.blit(self.font.render("Reset", True, WHITE), (140, GRID_SIZE * CELL_SIZE + 15))

        # Draw dropdown for algorithm selection next to Reset
        pygame.draw.rect(self.screen, (150, 150, 150), (250, GRID_SIZE * CELL_SIZE + 10, 150, 30))
        self.screen.blit(self.font.render(self.selected_algorithm, True, BLACK), (260, GRID_SIZE * CELL_SIZE + 15))
        if self.dropdown_active:
            for i, option in enumerate(self.algorithms):
                option_rect = pygame.Rect(250, GRID_SIZE * CELL_SIZE + 10 + (i + 1) * 30, 150, 30)
                pygame.draw.rect(self.screen, (100, 100, 100), option_rect)
                self.screen.blit(self.font.render(option, True, WHITE), (260, GRID_SIZE * CELL_SIZE + 15 + (i + 1) * 30))

        # Conditionally display the "Done" button after Q-learning training completes and before exploration
        if self.training_complete and not self.exploration_started:
            pygame.draw.rect(self.screen, BLUE, (370, GRID_SIZE * CELL_SIZE + 10, 100, 30))
            self.screen.blit(self.font.render("Done", True, WHITE), (380, GRID_SIZE * CELL_SIZE + 15))

        # Display prompt for exploration phase
        if self.training_complete and self.selected_algorithm == "Q-learning" and not self.exploration_started:
            self.display_message("Optimal policy trained! Modify map, then click 'Done'")

        # Display rewards and penalties
        self.display_scores()
        
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if mouse_pos[1] < GRID_SIZE * CELL_SIZE:
                    self.grid.toggle_cell(mouse_pos)  # Toggle cell color/state
                else:
                    self.handle_buttons(mouse_pos)
                    # Check if dropdown is clicked
                    if 250 <= mouse_pos[0] <= 400 and GRID_SIZE * CELL_SIZE + 10 <= mouse_pos[1] <= GRID_SIZE * CELL_SIZE + 40:
                        self.dropdown_active = not self.dropdown_active
                    elif self.dropdown_active:
                        for i, option in enumerate(self.algorithms):
                            option_rect = pygame.Rect(250, GRID_SIZE * CELL_SIZE + 10 + (i + 1) * 30, 150, 30)
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
                # Q-learning training or exploration
                if not self.qlearning_sprite.training_complete and not self.qlearning_sprite.is_exploring:
                    self.qlearning_sprite.take_step(self.grid)
                    time.sleep(0.1)
                elif self.qlearning_sprite.training_complete and not self.qlearning_sprite.is_exploring:
                    self.training_complete = True
                    self.running = False
                elif self.qlearning_sprite.is_exploring:
                    if self.qlearning_sprite.position == (GRID_SIZE - 1, GRID_SIZE - 1):
                        # Reset to start if goal is reached during exploration
                        self.qlearning_sprite.position = [0, 0]
                    self.qlearning_sprite.follow_optimal_path()
                    time.sleep(0.1)
                    if not self.qlearning_sprite.optimal_path:
                        # Regenerate optimal path to continue exploring
                        self.qlearning_sprite.compute_optimal_path(self.grid)

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
