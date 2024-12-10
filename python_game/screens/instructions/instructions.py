import pygame
import sys
from screens.scrolling_texts import ScrollingTextDisplay  # Assuming the generic class is saved as suggested

class Instructions(ScrollingTextDisplay):
    def __init__(self, screen):
        instructions_content = [
            "Tutorial Level - Dijkstra's Maze:",
            "Objective: A baby turtle just hatched, and needs to get to the ocean and start a life for itself!",
            "You are in charge of creating a unique beach for a turtle hatchling to walk through on it's way to the ocean.",
            "You can place light sources, which mimic the light from the moon reflecting onto the surface of the ocean.",
            "Turtle hatchlings use the light from the moon as a natural compass that leads them to the Ocean.",
            "Artificial lights created by humans can confuse turtles, and cause them to walk in circles, or away from the "
            "ocean entirely when they first hatch.",
            "You can place ghost crabs, which are one of these hatchlings' natural predators.",
            "The hatchling will do everything in its power to avoid these pesky guys.",
            "",
            "Controls: Use arrow keys to move the black box. Click the green button once to place a ghost crab (red block), "
            "click the green button again to place a light source (green block), "
            "click the green button once more to revert it to an empty square. ",
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
