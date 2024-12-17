import pygame
from utils import resource_path

from grid.grid import Grid
from sprites.QLearningSprite import QLearningSprite
from screens.explanations.oscillation_explanation import OscillationExplanation
from screens.explanations.many_steps_explanation import ManyStepsExplanation


class Game2:
    def __init__(self, screen):
        self.screen = screen
        self.max_steps_options = [10, 500, 1000, 5000]  # Options for max steps
        self.selected_option_index = 0  # Default to the first option
        self.running = True  # Track game state
        self.show_max_steps_selection = True  # Flag to show max steps selection screen
        self.init_game()

    def retry_game(self):
        self.show_max_steps_selection = (
            True  # Show the max steps selection screen again
        )
        self.init_game()
        self.run()

    def init_game(self):
        self.grid = Grid(rows=4, cols=8, cell_size=170)  # Adjust as needed
        self.sprite = QLearningSprite(
            start_position=[0, 0],
            cell_size=170,
            rows=4,
            cols=8,
            max_steps=1000,  # Default value, will be updated after selection
            screen=self.screen,
            retry_callback=self.retry_game,
        )
        self.selected_position = [0, 0]
        self.blink = True
        self.blink_timer = 0
        self.blink_interval = 500  # Milliseconds
        self.pathfinding_started = False  # Whether pathfinding has started

    def max_steps_selection_screen(self):
        font = pygame.font.Font(resource_path("fonts/PressStart2P-Regular.ttf"), 36)
        title_text = font.render("Select Max Steps", True, (255, 255, 255))
        instructions_text = (
            "Arrow Keys to Select,\nRed Button to Confirm"  # Multi-line text
        )

        running = True
        while running:
            self.screen.fill((0, 0, 0))
            # Render the title
            self.screen.blit(
                title_text,
                (self.screen.get_width() // 2 - title_text.get_width() // 2, 50),
            )

            # Render multi-line instructions
            instruction_lines = instructions_text.split("\n")
            for i, line in enumerate(instruction_lines):
                line_surface = font.render(line, True, (200, 200, 200))
                self.screen.blit(
                    line_surface,
                    (
                        self.screen.get_width() // 2 - line_surface.get_width() // 2,
                        150 + i * 40,
                    ),
                )

            # Render the options
            for i, option in enumerate(self.max_steps_options):
                color = (
                    (255, 255, 0)
                    if i == self.selected_option_index
                    else (255, 255, 255)
                )
                option_text = font.render(f"{option}", True, color)
                self.screen.blit(
                    option_text,
                    (
                        self.screen.get_width() // 2 - option_text.get_width() // 2,
                        250 + i * 50,
                    ),
                )

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.running = False
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_option_index = max(
                            0, self.selected_option_index - 1
                        )
                    elif event.key == pygame.K_DOWN:
                        self.selected_option_index = min(
                            len(self.max_steps_options) - 1,
                            self.selected_option_index + 1,
                        )
                    elif event.key == pygame.K_RETURN:
                        self.sprite.max_steps = self.max_steps_options[
                            self.selected_option_index
                        ]
                        self.show_max_steps_selection = False
                        running = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if not self.pathfinding_started:
                    if event.key == pygame.K_LEFT:
                        self.selected_position[1] = max(
                            0, self.selected_position[1] - 1
                        )
                    elif event.key == pygame.K_RIGHT:
                        self.selected_position[1] = min(
                            self.grid.cols - 1, self.selected_position[1] + 1
                        )
                    elif event.key == pygame.K_UP:
                        self.selected_position[0] = max(
                            0, self.selected_position[0] - 1
                        )
                    elif event.key == pygame.K_DOWN:
                        self.selected_position[0] = min(
                            self.grid.rows - 1, self.selected_position[0] + 1
                        )
                    elif event.key == pygame.K_SPACE:
                        current_color = self.grid.maze[self.selected_position[0]][
                            self.selected_position[1]
                        ]
                        if current_color == (240, 230, 140):  # Yellow (normal)
                            new_color = (255, 0, 0)  # Red (penalty)
                        elif current_color == (255, 0, 0):  # Red (penalty)
                            new_color = (0, 255, 0)  # Green (reward)
                        else:
                            new_color = (240, 230, 140)  # Back to yellow
                        self.grid.maze[self.selected_position[0]][
                            self.selected_position[1]
                        ] = new_color
                    elif event.key == pygame.K_RETURN:
                        self.pathfinding_started = True

    def update(self):
        if self.pathfinding_started:
            self.sprite.take_step(self.grid)
        else:
            current_time = pygame.time.get_ticks()
            if current_time - self.blink_timer >= self.blink_interval:
                self.blink = not self.blink
                self.blink_timer = current_time

    def render(self):
        self.screen.fill((0, 0, 0))
        self.grid.draw(self.screen)
        if not self.pathfinding_started and self.blink:
            x = self.selected_position[1] * self.grid.cell_size
            y = self.selected_position[0] * self.grid.cell_size
            pygame.draw.rect(
                self.screen,
                (0, 0, 0),
                (x, y, self.grid.cell_size, self.grid.cell_size),
                3,
            )
        self.sprite.draw(self.screen, self.grid)
        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            if self.show_max_steps_selection:
                self.max_steps_selection_screen()
            else:
                self.handle_events()
                self.update()
                self.render()
            clock.tick(60)
