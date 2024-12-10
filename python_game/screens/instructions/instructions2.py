import pygame
import sys
from screens.scrolling_texts import ScrollingTextDisplay  # Assuming the generic class is defined as suggested

class Instructions2(ScrollingTextDisplay):
    def __init__(self, screen):
        instructions_content = [
            "Gameplay - Q-Learning Arena:",
            "Objective: Create an environment on this beach that gets the hatchling to the end in the least ammount of moves.",
            "Bonus points are awarded for using fewer rewards and obstacles to guide the turtle to the ocean (bottom right square).",
            "The Q-learning table is displayed with four numbers representing potential values for up, down, left, and right directions.",
            "",
            "Controls: Use arrow buttons to navigate the beach and use the green button to create rewards and punishments.",
            "Once you are happy with the beach you created, press the red button.",
            "",
            "Mechanics: The hatchling has a limited number of steps before it runs out of motivation.",
            "Everytime the hatchling reaches a light source on the way to the ocean, its spirits get lifted and the number of steps it can take increases."
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
