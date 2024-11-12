import pygame
import sys
from screens.scrolling_texts import ScrollingTextDisplay  # Assuming the generic class is saved as suggested

class Instructions(ScrollingTextDisplay):
    def __init__(self, screen):
        instructions_content = [
            "Level 1 - Dijkstra's Maze:",
            "Objective: Navigate through the maze and find the shortest path.",
            "Controls: Use arrow keys to move the walls and reward points.",
            "Click once for wall, click twice for reward.",
            ""
        ]
        super().__init__(screen, "Instructions", instructions_content, font_path='./fonts/PressStart2P-Regular.ttf', font_size=20)

    def run(self):
        # Call the base class's run method explicitly
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
