import pygame
import sys
from grid import Grid
from DijkstraSprite import DijkstraSprite
from QLearningSprite import QLearningSprite
import time

CELL_SIZE = 50
GRID_SIZE = 10
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
        self.current_sprite = self.dijkstra_sprite
        self.running = False
        self.rewards_enabled = True
        self.font = pygame.font.SysFont("Arial", 20)
        self.clock = pygame.time.Clock()  # Frame rate control

        # Algorithm selection dropdown
        self.algorithms = ["Dijkstra", "Q-learning"]
        self.selected_algorithm = self.algorithms[0]
        self.dropdown_active = False

        # Scores for Q-learning
        self.reward_score = 0
        self.punishment_score = 0


    def handle_buttons(self, pos):
        if 10 <= pos[0] <= 110 and GRID_SIZE * CELL_SIZE + 10 <= pos[1] <= GRID_SIZE * CELL_SIZE + 40:
            self.start_simulation()
        elif 130 <= pos[0] <= 230 and GRID_SIZE * CELL_SIZE + 10 <= pos[1] <= GRID_SIZE * CELL_SIZE + 40:
            self.reset_simulation()
        elif 250 <= pos[0] <= 350 and GRID_SIZE * CELL_SIZE + 10 <= pos[1] <= GRID_SIZE * CELL_SIZE + 40:
            self.toggle_rewards()

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
        # Reset the grid's rewards and punishments
        self.grid.reset_rewards_and_punishments()

        # Reset the position and scores of the sprites
        self.dijkstra_sprite.position = [0, 0]
        self.qlearning_sprite.position = [0, 0]

        # Reset Q-learning specific metrics
        self.qlearning_sprite.collected_rewards = 0
        self.qlearning_sprite.step_penalties = 0
        self.qlearning_sprite.training_complete = False
        self.qlearning_sprite.optimal_path = []
        self.qlearning_sprite.goal_reached_count = 0

        # Reset display scores
        self.reward_score = 0
        self.punishment_score = 0

        self.running = False

    def toggle_rewards(self):
        self.rewards_enabled = not self.rewards_enabled

    def display_scores(self):
        if self.selected_algorithm == "Q-learning":
            score_text = self.font.render(f"Rewards: {self.qlearning_sprite.collected_rewards} | Penalties: {self.qlearning_sprite.step_penalties}", True, BLACK)
            self.screen.blit(score_text, (10, self.screen.get_height() - 30))  # Lower-left corner display
        # self.screen.blit(score_text, (10, 10))

    def draw(self):
        self.screen.fill(WHITE)
        self.grid.draw(self.screen)
        self.current_sprite.draw(self.screen)

        pygame.draw.rect(self.screen, BLUE, (10, GRID_SIZE * CELL_SIZE + 10, 100, 30))
        self.screen.blit(self.font.render("Start", True, WHITE), (20, GRID_SIZE * CELL_SIZE + 15))
        pygame.draw.rect(self.screen, BLUE, (130, GRID_SIZE * CELL_SIZE + 10, 100, 30))
        self.screen.blit(self.font.render("Reset", True, WHITE), (140, GRID_SIZE * CELL_SIZE + 15))
        pygame.draw.rect(self.screen, GREEN if self.rewards_enabled else (100, 100, 100), (250, GRID_SIZE * CELL_SIZE + 10, 100, 30))
        self.screen.blit(self.font.render("Toggle Rewards", True, WHITE), (260, GRID_SIZE * CELL_SIZE + 15))

        pygame.draw.rect(self.screen, (150, 150, 150), (400, GRID_SIZE * CELL_SIZE + 10, 150, 30))
        self.screen.blit(self.font.render(self.selected_algorithm, True, BLACK), (410, GRID_SIZE * CELL_SIZE + 15))
        
        if self.dropdown_active:
            for i, option in enumerate(self.algorithms):
                option_rect = pygame.Rect(400, GRID_SIZE * CELL_SIZE + 10 + (i+1) * 30, 150, 30)
                pygame.draw.rect(self.screen, (100, 100, 100), option_rect)
                self.screen.blit(self.font.render(option, True, WHITE), (410, GRID_SIZE * CELL_SIZE + 15 + (i+1) * 30))

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
                    if 400 <= mouse_pos[0] <= 550 and GRID_SIZE * CELL_SIZE + 10 <= mouse_pos[1] <= GRID_SIZE * CELL_SIZE + 40:
                        self.dropdown_active = not self.dropdown_active
                    elif self.dropdown_active:
                        for i, option in enumerate(self.algorithms):
                            option_rect = pygame.Rect(400, GRID_SIZE * CELL_SIZE + 10 + (i+1) * 30, 150, 30)
                            if option_rect.collidepoint(mouse_pos):
                                self.selected_algorithm = option
                                self.dropdown_active = False
                                break

    def update(self):
        if self.running:
            if self.selected_algorithm == "Dijkstra":
                self.dijkstra_sprite.follow_path()
                time.sleep(0.1)
                if not self.dijkstra_sprite.path:
                    self.running = False
            elif self.selected_algorithm == "Q-learning":
                if not self.qlearning_sprite.training_complete:
                    self.qlearning_sprite.take_step(self.grid)
                    time.sleep(0.2)
                else:
                    self.qlearning_sprite.follow_optimal_path()
                    time.sleep(0.3)
                    if not self.qlearning_sprite.optimal_path:
                        self.running = False


    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
