import pygame
import sys
from screens.scrolling_texts import ScrollingTextDisplay  # Assuming the generic class is defined as suggested

class Instructions2(ScrollingTextDisplay):
    def __init__(self, screen):
        instructions_content = [
            "Level 2 - Q-Learning Arena:",
            "Objective: Adapt to changing paths and maximize rewards.",
            "Controls: Use arrow keys to move."
        ]
        super().__init__(screen, "Instructions Level 2", instructions_content, font_path='./fonts/PressStart2P-Regular.ttf', font_size=20)

    def run(self):
        super().run(self.wait_for_key)

    def wait_for_key(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    waiting = False
