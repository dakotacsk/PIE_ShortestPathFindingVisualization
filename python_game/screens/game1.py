import pygame
from grid.grid import Grid
from sprites.DijkstraSprite import DijkstraSprite
from screens.instructions.instructions2 import Instructions2
import time


class Game1:
    def __init__(self, screen):
        self.screen = screen
        self.grid = Grid(rows=5, cols=8, cell_size=240)  # Create the grid
        self.sprite = DijkstraSprite(start_pos=[0, 0], cell_size=240, grid=self.grid)  # Initialize the sprite
        self.selected_position = [0, 0]  # Default selected position
        self.blink = True
        self.blink_timer = pygame.time.get_ticks()
        self.blink_interval = 500  # Blink every 500ms
        self.running = True
        self.pathfinding_started = False  # Pathfinding not started yet

    def run(self):
        """Main game loop."""
        clock = pygame.time.Clock()
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            clock.tick(60)  # Cap the frame rate at 60 FPS

            # Check if the sprite reached the goal
            if self.sprite.reached_goal:
                self.handle_goal_reached()

    def handle_events(self):
        """Handle user inputs."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if not self.pathfinding_started:
                    if event.key == pygame.K_LEFT:
                        self.selected_position[1] = max(0, self.selected_position[1] - 1)
                    elif event.key == pygame.K_RIGHT:
                        self.selected_position[1] = min(self.grid.cols - 1, self.selected_position[1] + 1)
                    elif event.key == pygame.K_UP:
                        self.selected_position[0] = max(0, self.selected_position[0] - 1)
                    elif event.key == pygame.K_DOWN:
                        self.selected_position[0] = min(self.grid.rows - 1, self.selected_position[0] + 1)
                    elif event.key == pygame.K_SPACE:
                        # Toggle cell colors
                        current_color = self.grid.maze[self.selected_position[0]][self.selected_position[1]]
                        if current_color == (240, 230, 140):  # Yellow (default)
                            self.grid.maze[self.selected_position[0]][self.selected_position[1]] = (255, 0, 0)  # Red
                        elif current_color == (255, 0, 0):  # Red
                            self.grid.maze[self.selected_position[0]][self.selected_position[1]] = (0, 255, 0)  # Green
                        else:
                            self.grid.maze[self.selected_position[0]][self.selected_position[1]] = (240, 230, 140)  # Yellow
                if event.key == pygame.K_RETURN:
                    # Start pathfinding
                    self.sprite.set_path([0, 0], [self.grid.rows - 1, self.grid.cols - 1])
                    self.pathfinding_started = True

    def update(self):
        """Update the game state."""
        if self.pathfinding_started:
            self.sprite.follow_path()
        else:
            # Update blinking timer
            current_time = pygame.time.get_ticks()
            if current_time - self.blink_timer >= self.blink_interval:
                self.blink = not self.blink
                self.blink_timer = current_time

    def render(self):
        """Render the game elements."""
        self.screen.fill((0, 0, 0))  # Clear the screen
        self.grid.draw(self.screen)  # Draw the grid
        if not self.pathfinding_started and self.blink:
            x = self.selected_position[1] * self.grid.cell_size
            y = self.selected_position[0] * self.grid.cell_size
            pygame.draw.rect(
                self.screen,
                (0, 0, 0),
                (x, y, self.grid.cell_size, self.grid.cell_size),
                3,
            )
        self.sprite.draw(self.screen)  # Draw the sprite
        pygame.display.flip()

    def handle_goal_reached(self):
        """Handle what happens when the goal is reached."""
        self.sprite.draw(self.screen)
        pygame.display.flip()
        time.sleep(3)  # Pause for 3 seconds
        self.running = False
        self.show_cutscene()

    def show_cutscene(self):
        """Show the next set of instructions or transition screen."""
        instructions = Instructions2(self.screen)
        instructions.run()
