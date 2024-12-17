import pygame
import sys
from screens.scrolling_texts import ScrollingTextDisplay  # Assuming the generic class is saved as suggested

class Instructions(ScrollingTextDisplay):
    def __init__(self, screen):
        instructions_content = [
            "Tutorial Level - Dijkstra's Maze:",
            "Objective:",
            "Help the baby turtle hatchling safely reach the ocean (bottom-right square).",
            "You are in charge of designing a unique beach environment for the turtle to navigate.",
            "The hatchling will follow the safest path to the ocean, while actively avoiding obstacles and moving towards rewards.",
            "Help your hatchling find a path to safety!",
            "This level's hatchling is assumed to behave completely as you would expect.",
            "",
            "Mechanics:",
            "- Light Sources (Green Blocks): These mimic the light from the moon, creating safe areas the hatchling is incentivized to move toward.",
            "- Ghost Crabs (Red Blocks): These are predators that the hatchling will avoid as much as possible.",
            "",
            "How It Works:",
            "- The hatchling uses Dijkstra's algorithm to determine the shortest path to the ocean (bottom-right square).",
            "- Light sources guide the turtle by attracting it to safer areas.",
            "- Ghost crabs act as obstacles, increasing the hatchling's path distance as it tries to avoid them.",
            "",
            "Controls:",
            "- Use the ARROW KEYS to move the black box (cursor).",
            "- Click the GREEN BUTTON to place components:",
            "    - First Click: Place a Ghost Crab (red block).",
            "    - Second Click: Place a Light Source (green block).",
            "    - Third Click: Revert the square to an empty tile.",
            "",
            "Tips:",
            "- Place light sources (green blocks) to encourage the hatchling to move efficiently toward the ocean.",
            "- Use ghost crabs (red blocks) to create obstacles and force the hatchling to find alternate paths.",
            "- Experiment with different layouts to see how the hatchling adapts its path.",
            "",
            "Have fun designing the beach and guiding the hatchling to the ocean!"
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
