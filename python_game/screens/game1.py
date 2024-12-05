import pygame
from grid.grid import Grid
from sprites.DijkstraSprite import DijkstraSprite
import time
from screens.instructions.instructions2 import Instructions2

class Game1:
    def __init__(self, screen):
        self.screen = screen
        self.grid = Grid(rows=3, cols=5, cell_size=160)  # Adjust as needed
        self.sprite = DijkstraSprite(start_pos=[0, 0], cell_size=160, grid=self.grid)
        self.selected_position = [0, 0]  # Start at the first block
        self.blink = True
        self.blink_timer = pygame.time.get_ticks()
        self.blink_interval = 500  # Milliseconds (1 second) - Increase to slow down blinking
        self.running = True
        self.pathfinding_started = False  # Flag to control when pathfinding starts

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            clock.tick(60)

            # Check if the goal has been reached and handle the delay/transition
            if self.sprite.reached_goal:
                self.handle_goal_reached()

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
                        # Toggle cell color logic
                        current_color = self.grid.maze[self.selected_position[0]][self.selected_position[1]]
                        if current_color == (255, 255, 255):  # White (normal)
                            new_color = (255, 0, 0)  # Red (wall/penalty)
                        elif current_color == (255, 0, 0):  # Red (wall/penalty)
                            new_color = (0, 255, 0)  # Green (reward)
                        else:
                            new_color = (255, 255, 255)  # Back to white
                        self.grid.maze[self.selected_position[0]][self.selected_position[1]] = new_color
                if event.key == pygame.K_RETURN:
                    # Start pathfinding when Enter is pressed
                    self.sprite.set_path([0, 0], [self.grid.rows - 1, self.grid.cols - 1])
                    self.pathfinding_started = True

    def update(self):
        if self.pathfinding_started:
            self.sprite.follow_path()
        else:
            # Update blinking timer
            current_time = pygame.time.get_ticks()
            if current_time - self.blink_timer >= self.blink_interval:
                self.blink = not self.blink
                self.blink_timer = current_time

    def render(self):
        self.screen.fill((0, 0, 0))  # Black background
        self.grid.draw(self.screen)
        if not self.pathfinding_started and self.blink:
            x = self.selected_position[1] * self.grid.cell_size
            y = self.selected_position[0] * self.grid.cell_size
            pygame.draw.rect(self.screen, (0, 0, 0), (x, y, self.grid.cell_size, self.grid.cell_size), 3)
        self.sprite.draw(self.screen)
        pygame.display.flip()

    def handle_goal_reached(self):
        # Change color to yellow and hold for 3 seconds before transitioning
        self.sprite.draw(self.screen)
        pygame.display.flip()
        time.sleep(3)  # Hold for 3 seconds
        self.running = False
        self.show_cutscene()

    def show_cutscene(self):
        instructions = Instructions2(self.screen)
        instructions.run()  # Display the cutscene with Level 2 instructions
