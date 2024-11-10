import pygame
import sys

class Instructions2:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 30)

    def run(self):
        self.screen.fill((0, 0, 0))
        instructions = [
            "Level 2 - Q-Learning Arena:",
            "Objective: Adapt to changing paths and maximize rewards.",
            "Controls: Use arrow keys to move."
        ]
        y_offset = 100
        for line in instructions:
            text = self.font.render(line, True, (255, 255, 255))
            self.screen.blit(text, (50, y_offset))
            y_offset += 40
        pygame.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    waiting = False
