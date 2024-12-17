import pygame
import sys
from screens.scrolling_texts import ScrollingTextDisplay  # Assuming the generic class is defined as suggested

class Instructions2(ScrollingTextDisplay):
    def __init__(self, screen):
        instructions_content = [
            "Gameplay - Q-Learning Arena:",
            "Objective:",
            "Create an environment that trains the turtle hatchling to navigate to the ocean (bottom-right square) efficiently.",
            "The hatchling uses Q-Learning to learn the best path based on the environment you create.",
            "",
            "Mechanics:",
            "- Resource Costs:",
            "    - Placing a Ghost Crab (Red Block): Costs 100 points.",
            "    - Placing a Light Source (Green Block): Costs 150 points.",
            "    - Your goal is to minimize the number of resources used while still guiding the hatchling to the ocean.",
            "",
            "- Life Experience (Max Steps):",
            "    - At the start of the game, you will choose a 'max steps' value, representing how much 'life experience' the hatchling has.",
            "    - More life experience (higher max steps) allows the hatchling to explore the environment longer, improving its understanding.",
            "",
            "- Rewards and Punishments:",
            "    - Light Sources (Green Blocks): These guide the turtle toward the safest areas.",
            "    - Ghost Crabs (Red Blocks): These act as obstacles the hatchling avoids.",
            "",
            "Final Score Calculation:",
            "Your score is determined by the total cost of resources (blocks) used:",
            "    - Each GREEN BLOCK (Light Source): -150 points.",
            "    - Each RED BLOCK (Ghost Crab): -100 points.",
            "    - The fewer resources you use, the higher your score!",
            "",
            "Formula for Final Score:",
            "   Final Score = 5000 - (Green Count * 150) - (Red Count * 100)",
            "",
            "Example:",
            "    Starting Score: 5000",
            "    3 Green Blocks: 3 * 150 = 450 points deducted.",
            "    2 Red Blocks: 2 * 100 = 200 points deducted.",
            "    Final Score = 5000 - 450 - 200 = 4350 points.",
            "",
            "Controls:",
            "- Use the ARROW KEYS to move the black box (cursor).",
            "- Click the GREEN BUTTON to place components:",
            "    - First Click: Place a Ghost Crab (Red Block).",
            "    - Second Click: Place a Light Source (Green Block).",
            "    - Third Click: Revert the square to an empty tile.",
            "- Press the RED BUTTON when you are satisfied with the beach layout and ready to train the hatchling.",
            "",
            "Final Steps:",
            "- Once training is complete, the hatchling will follow its learned path (policy) to the ocean.",
            "- At the end, check your **final score** based on how efficiently you used resources.",
            "",
            "Tips:",
            "- Use as few blocks as possible to guide the hatchling efficiently while keeping costs low.",
            "- Experiment with placing rewards (green blocks) in key positions to guide the hatchling without overusing resources.",
            "- Strategically place obstacles (red blocks) to challenge the hatchling without increasing costs unnecessarily.",
            "",
            "Have fun designing, training, and optimizing the hatchling's journey to the ocean!"
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
