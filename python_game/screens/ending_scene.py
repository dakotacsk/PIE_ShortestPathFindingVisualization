import pygame
import sys
from screens.scrolling_texts import ScrollingTextDisplay
from screens.leaderboard import Leaderboard

class EndingScene(ScrollingTextDisplay):
    def __init__(self, screen, retry_callback, user_score):
        explanation_text = [
            "Congratulations for finishing the game!",
            f"Your in-game score is: {user_score}",
            "",
            "Press Space to save your in-game score and go to the leaderboard!",
            "Press Enter to retry training the model."
        ]
        super().__init__(screen, "Ending Screen", explanation_text, font_size=16)
        self.retry_callback = retry_callback
        self.user_score = user_score
        self.leaderboard = Leaderboard(screen, retry_callback, csv_filename="../python_game/leaderboard/leaderboard.csv")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Retry when Enter is pressed
                    self.retry_callback()
                    return False  # Stop running
                elif event.key == pygame.K_SPACE:  # Save score and go to the leaderboard when Space is pressed
                    self.leaderboard.save_score(self.user_score)  # Save the score to the leaderboard
                    self.leaderboard.run(self.user_score)  # Display the leaderboard with the new score highlighted
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
