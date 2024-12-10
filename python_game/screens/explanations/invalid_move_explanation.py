import pygame
import sys
from screens.scrolling_texts import ScrollingTextDisplay  # Assuming the base class is defined

class InvalidMoveExplanation(ScrollingTextDisplay):
    def __init__(self, screen, retry_callback):
        explanation_text = [
            "An invalid move occurs when the hatchling tries to move outside the",
            "beach or into an area with a ghost crab.",
            "",
            "Possible reasons for invalid moves:",
            "- The Q-Learning policy suggests an action that leads out of bounds.",
            "- The hatchling hasn't learned the environment layout properly yet.",
            "",
            "Suggestions to avoid invalid moves:",
            "- Ensure the environment boundaries are clearly defined.",
            "- Provide penalties for invalid moves during training to discourage",
            "  such actions.",
            "- Increase training iterations to allow the hatchling to learn valid paths.",
            "",
            "Invalid moves result in wasted steps and can prevent the hatchling",
            "from reaching its goal efficiently.",
            "",
            "Press Enter to retry."
        ]
        super().__init__(screen, "Invalid Move Explanation", explanation_text, font_size=16)
        self.retry_callback = retry_callback

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Retry when Enter is pressed
                    self.retry_callback()
                    return False  # Stop running
                elif event.key == pygame.K_UP:
                    self.key_up_pressed = True  # Trigger scroll up
                elif event.key == pygame.K_DOWN:
                    self.key_down_pressed = True  # Trigger scroll down
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.key_up_pressed = False  # Stop scroll up
                elif event.key == pygame.K_DOWN:
                    self.key_down_pressed = False  # Stop scroll down
        return True

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.scroll_content()
            self.render()
