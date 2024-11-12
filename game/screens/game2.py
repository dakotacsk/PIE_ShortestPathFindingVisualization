import pygame
from grid.grid import Grid
from sprites.QLearningSprite import QLearningSprite
from screens.oscillation_explanation import OscillationExplanation  # Import the oscillation explanation function

class Game2:
    def __init__(self, screen):
        self.screen = screen
        self.init_game()  # Initialize game variables and objects

    def init_game(self):
        self.grid = Grid(rows=5, cols=8, cell_size=100)  # Adjust as needed
        self.sprite = QLearningSprite(
            start_position=[0, 0],
            cell_size=100,
            rows=5,
            cols=8,
            oscillation_callback=self.handle_oscillation,  # Pass the oscillation callback
            screen=self.screen,
            retry_callback=self.retry_game  # Pass the retry callback
        )
        self.selected_position = [0, 0]  # Start at the first block
        self.blink = True
        self.blink_timer = 0
        self.blink_interval = 500  # Milliseconds
        self.running = True
        self.pathfinding_started = False  # Flag to control when pathfinding starts

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if not self.pathfinding_started:
                    if event.key == pygame.K_LEFT:
                        self.selected_position[1] = max(0, self.selected_position[1] - 1)  # Move left
                    elif event.key == pygame.K_RIGHT:
                        self.selected_position[1] = min(self.grid.cols - 1, self.selected_position[1] + 1)  # Move right
                    elif event.key == pygame.K_UP:
                        self.selected_position[0] = max(0, self.selected_position[0] - 1)  # Move up
                    elif event.key == pygame.K_DOWN:
                        self.selected_position[0] = min(self.grid.rows - 1, self.selected_position[0] + 1)  # Move down
                    elif event.key == pygame.K_SPACE:
                        # Cycle through colors: white -> red -> green -> white
                        current_color = self.grid.maze[self.selected_position[0]][self.selected_position[1]]
                        if current_color == (255, 255, 255):  # White (normal)
                            new_color = (255, 0, 0)  # Red (penalty)
                        elif current_color == (255, 0, 0):  # Red (penalty)
                            new_color = (0, 255, 0)  # Green (reward)
                        else:
                            new_color = (255, 255, 255)  # Back to white
                        self.grid.maze[self.selected_position[0]][self.selected_position[1]] = new_color
                    elif event.key == pygame.K_RETURN:
                        # Start pathfinding when Enter is pressed
                        self.pathfinding_started = True

    def update(self):
        if self.pathfinding_started:
            self.sprite.take_step(self.grid)
        else:
            # Update blinking timer
            current_time = pygame.time.get_ticks()
            if current_time - self.blink_timer >= self.blink_interval:
                self.blink = not self.blink
                self.blink_timer = current_time

    def render(self):
        self.screen.fill((0, 0, 0))  # Black background
        self.grid.draw(self.screen)

        # Highlight the selected position if not pathfinding
        if not self.pathfinding_started and self.blink:
            x = self.selected_position[1] * self.grid.cell_size
            y = self.selected_position[0] * self.grid.cell_size
            pygame.draw.rect(self.screen, (0, 0, 0), (x, y, self.grid.cell_size, self.grid.cell_size), 3)

        self.sprite.draw(self.screen, self.grid)  # Pass grid as a second argument
        pygame.display.flip()

    def handle_oscillation(self):
        # Call the oscillation explanation screen
        OscillationExplanation(self.screen, self.retry_game)

    def retry_game(self):
        # Reinitialize the game state for retrying
        self.init_game()
        self.run()  # Start the game loop again
