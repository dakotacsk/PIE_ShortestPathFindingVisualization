import pygame
import sys
from screens.scrolling_texts import ScrollingTextDisplay  # Assuming the base class is defined

class ManyStepsExplanation(ScrollingTextDisplay):
    def __init__(self, screen, retry_callback):
        explanation_text = [
            "Taking many steps in Q-Learning can indicate challenges in the",
            "learning process or environmental setup.",
            "",
            "Possible reasons include:",
            "- High exploration rates (epsilon) causing excessive random moves.",
            "- Insufficient training iterations leading to incomplete convergence.",
            "- Suboptimal reward design, making the deer fail to differentiate",
            "  between paths leading to the goal and other routes.",
            "- Sparse rewards where the deer struggles to associate actions",
            "  with progress towards the goal.",
            "- Highly dynamic or complex environments where the deer's policy",
            "  is yet to adapt effectively.",
            "",
            "To address these issues, consider:",
            "- Adjusting epsilon to balance exploration and exploitation.",
            "- Increasing training steps or episodes for better convergence.",
            "- Refining the reward structure to encourage direct paths.",
            "- Using mechanisms like shaping rewards or penalties for delays.",
            "",
            "Understanding these challenges can help improve the deer's",
            "efficiency and effectiveness.",
            "",
            "Press Enter to retry training the model."
        ]
        super().__init__(screen, "Q-Learning Steps Explanation", explanation_text, font_size=16)
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
