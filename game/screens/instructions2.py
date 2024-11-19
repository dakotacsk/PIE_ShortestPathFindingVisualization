import pygame
import sys
from screens.scrolling_texts import ScrollingTextDisplay  # Assuming the generic class is defined as suggested

class Instructions2(ScrollingTextDisplay):
    def __init__(self, screen):
        instructions_content = [
            "Gameplay - Q-Learning Arena:",
            "Objective: Adapt to changing paths and maximize rewards using the Q-learning table.",
            "The Q-learning table is displayed with four numbers representing potential values for up, down, left, and right directions.",
            "Controls: Use arrow keys to move the Sprite through the grid.",
            "Mechanics: The more steps the Sprite takes, the more punishments it accumulates.",
            "Note: Sprite has a limited number of steps before it 'runs out of gas' (game over).",
            "Green blocks give negative points (punishments), while red blocks grant positive points (rewards).",
            "Your goal is to find the optimal path that minimizes punishment and maximizes reward.",
            ""
        ]
        super().__init__(screen, "Instructions Gameplay", instructions_content, font_size=20)

    def run(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))  # Clear the screen
            self.scroll_content()  # Handle scrolling behavior if needed
            self.render()  # Render the content

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Exit when Enter is pressed
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
