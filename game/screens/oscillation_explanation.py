import pygame
import sys
from screens.scrolling_texts import ScrollingTextDisplay  # Assuming the base class is defined

class OscillationExplanation(ScrollingTextDisplay):
    def __init__(self, screen, retry_callback):
        explanation_text = [
            "Oscillation in Q-Learning occurs when an agent repeatedly revisits",
            "the same states without making meaningful progress towards a goal.",
            "",
            "This behavior can result from:",
            "- High exploration rates (epsilon) causing random moves.",
            "- Local maxima in the Q-value function leading to suboptimal loops.",
            "- Insufficient discount factor (gamma), failing to prioritize",
            "  long-term goals.",
            "- Lack of exploration leading to suboptimal path found.",
            "",
            "In Q-learning, oscillation is problematic as it prevents convergence",
            "to an optimal policy. Careful tuning of parameters and mechanisms",
            "like decay schedules or penalties for revisiting states can mitigate",
            "oscillation.",
            "",
            "Press any key to retry training the model."
        ]
        super().__init__(screen, "Q-Learning Oscillation Explanation", explanation_text, font_path='./fonts/PressStart2P-Regular.ttf', font_size=16)
        self.retry_callback = retry_callback

    def run(self):
        running = True
        while running:
            running = self.handle_events(self.retry_callback)
            self.scroll_content()
            self.render()
