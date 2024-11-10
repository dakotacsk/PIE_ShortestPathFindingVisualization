import pygame
import sys

class IntroCutscene:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 40)

    def run(self):
        self.screen.fill((0, 0, 0))
        text = self.font.render("The Glitch Lord has stolen the Core of Light!", True, (255, 255, 255))
        self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, self.screen.get_height() // 2))
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
