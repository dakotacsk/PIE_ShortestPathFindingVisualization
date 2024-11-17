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
        super().__init__(screen, "Instructions", instructions_content, font_size=20)

    def run(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))  # Clear the screen
            self.scroll_content()  # Handle any scrolling behavior
            self.render()  # Render the content

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Exit on pressing Enter
                        running = False
                    elif event.key == pygame.K_UP:
                        self.key_up_pressed = True
                    elif event.key == pygame.K_DOWN:
                        self.key_down_pressed = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.key_up_pressed = False
                    elif event.key == pygame.K_DOWN:
                        self.key_down_pressed = False
