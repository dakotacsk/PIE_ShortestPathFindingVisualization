import pygame
import sys
from grid import Grid

# Settings for the grid
GRID_ROWS = 5
GRID_COLS = 8
CELL_SIZE = 100

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((int(CELL_SIZE * GRID_COLS), int(CELL_SIZE * GRID_ROWS) + 120))
        pygame.display.set_caption("Sprite's Quest: The Pathfinding Trials")
        self.clock = pygame.time.Clock()
        self.running = True
        self.level = 1
        self.grid = Grid(GRID_ROWS, GRID_COLS, CELL_SIZE)

    def show_screen(self, message):
        """Display a generic message screen."""
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 50)
        text = font.render(message, True, (255, 255, 255))
        self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, self.screen.get_height() // 2))
        pygame.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        """Wait for the player to press any key."""
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    waiting = False

    def run(self):
        """Main game loop."""
        self.show_screen("Welcome to Sprite's Quest!")  # Landing page
        self.show_screen("Instructions: Use arrow keys to move.")  # Instructions page

        while self.running:
            if self.level == 1:
                self.run_level_1()
            elif self.level == 2:
                self.run_level_2()
            else:
                self.running = False
            self.clock.tick(60)

        self.show_screen("Congratulations! You've completed the game!")  # Ending page
        pygame.quit()

    def run_level_1(self):
        sprite = DijkstraSprite(start_pos=[0, 0], cell_size=int(CELL_SIZE), grid=self.grid)
        self.level_loop(sprite, "Level 1: Dijkstra's Maze")

    def run_level_2(self):
        sprite = QLearningSprite(start_position=[0, 0], cell_size=int(CELL_SIZE), rows=GRID_ROWS, cols=GRID_COLS)
        self.level_loop(sprite, "Level 2: Q-Learning Arena")

    def level_loop(self, sprite, level_title):
        running = True
        while running:
            self.handle_events(sprite)
            self.screen.fill((0, 0, 0))
            self.grid.draw(self.screen)
            sprite.follow_path() if self.level == 1 else sprite.take_step(self.grid)
            sprite.draw(self.screen)
            pygame.display.flip()

            if self.check_level_completion(sprite):
                running = False
                self.level += 1

    def handle_events(self, sprite):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    sprite.move("left", (GRID_ROWS, GRID_COLS))
                elif event.key == pygame.K_RIGHT:
                    sprite.move("right", (GRID_ROWS, GRID_COLS))
                elif event.key == pygame.K_UP:
                    sprite.move("up", (GRID_ROWS, GRID_COLS))
                elif event.key == pygame.K_DOWN:
                    sprite.move("down", (GRID_ROWS, GRID_COLS))

    def check_level_completion(self, sprite):
        if self.level == 1:
            return len(sprite.path) == 0  # Completion condition for Level 1
        elif self.level == 2:
            return sprite.position == [GRID_ROWS - 1, GRID_COLS - 1]  # Completion condition for Level 2
        return False
