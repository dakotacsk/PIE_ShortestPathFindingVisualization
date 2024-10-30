# game.py
import pygame
import sys
from grid import Grid
from sprite import Sprite

CELL_SIZE = 50
GRID_SIZE = 9
WHITE = (255, 255, 255)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((CELL_SIZE * GRID_SIZE, CELL_SIZE * GRID_SIZE))
        pygame.display.set_caption("Maze Creator")
        self.grid = Grid(GRID_SIZE, CELL_SIZE)
        self.sprite = Sprite([0, 0], CELL_SIZE)

        # Place initial rewards
        self.grid.place_rewards(5)  # Place 5 random reward blocks

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.grid.toggle_wall(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.sprite.move("up", self.grid)
                elif event.key == pygame.K_DOWN:
                    self.sprite.move("down", self.grid)
                elif event.key == pygame.K_LEFT:
                    self.sprite.move("left", self.grid)
                elif event.key == pygame.K_RIGHT:
                    self.sprite.move("right", self.grid)

    def update(self):
        pass  # Update game state if necessary

    def draw(self):
        self.screen.fill(WHITE)
        self.grid.draw(self.screen)
        self.sprite.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
