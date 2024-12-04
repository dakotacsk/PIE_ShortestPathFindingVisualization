import pygame
import sys
from screens.scrolling_texts import ScrollingTextDisplay  # Assuming the generic class is saved as suggested

class Instructions(ScrollingTextDisplay):
    def __init__(self, screen):
        instructions_content = [
            "Tutorial Level - Dijkstra's Maze:",
            "Objective: Sprite wants to move from the left corner of the grid to the right lowest corner.",
            "You are in charge of creating a ****for Sprite to walk through.",
            "You can place ****, which Sprite loves and will walk to, or",
            "you can place ****, which Sprite hates and refuse to walk on.",
            "Controls: Use arrow keys to move the black box. Click the green button once to place a **** (red block),",
            "click the green button again to place a **** (green block), ",
            "click the green button once more to revert it to normal. ",
            "Have fun!",
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
