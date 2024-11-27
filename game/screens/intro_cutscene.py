import pygame
import sys
from screens.scrolling_texts import ScrollingTextDisplay  # Assuming a base scrolling text class exists

class IntroCutscene(ScrollingTextDisplay):
    def __init__(self, screen):
        cutscene_content = [
            "Welcome to PathFinder!",
        ]
        super().__init__(screen, "IntroCutscene", cutscene_content, font_size=40)

    def run(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))  # Clear the screen
            self.render()  # Render the content

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    running = False  # Exit on any key press
