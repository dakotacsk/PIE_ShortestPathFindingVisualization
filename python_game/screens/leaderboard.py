import pygame
import csv
import os
from screens.main_menu import MainMenu
import sys

class Leaderboard:
    def __init__(self, screen, restart_callback, csv_filename="leaderboard.csv"):
        self.screen = screen
        self.restart_callback = restart_callback
        self.csv_filename = csv_filename
        self.scores = self.load_scores()
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 48)
        self.scroll_offset = 0  # Initial scroll offset
        self.max_display = 10  # Maximum scores displayed at once

    def load_scores(self):
        if not os.path.exists(self.csv_filename):
            return []

        with open(self.csv_filename, mode='r') as file:
            reader = csv.reader(file)
            scores = sorted([int(row[0]) for row in reader], reverse=True)  # Sort scores descending
        return scores

    def save_score(self, user_score):
        with open(self.csv_filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([user_score])
        self.scores.append(user_score)
        self.scores.sort(reverse=True)

    def render(self, user_score):
        self.screen.fill((0, 0, 0))  # Clear the screen with a black background

        title_surface = self.title_font.render("Leaderboard", True, (255, 255, 255))
        self.screen.blit(title_surface, (self.screen.get_width() // 2 - title_surface.get_width() // 2, 20))

        start_index = self.scroll_offset
        end_index = min(len(self.scores), start_index + self.max_display)

        for idx in range(start_index, end_index):
            rank = idx + 1
            score = self.scores[idx]
            score_text = f"{rank}th Score: {score}" if rank > 3 else ["1st", "2nd", "3rd"][rank - 1] + f" Score: {score}"
            score_surface = self.font.render(score_text, True, (255, 0, 0) if score == user_score else (255, 255, 255))

            y_pos = 70 + (idx - start_index) * 30
            if score == user_score:
                pygame.draw.rect(self.screen, (0, 255, 0), (40, y_pos - 5, 300, 30), 2)  # Highlight the user's score
            self.screen.blit(score_surface, (50, y_pos))

        instructions = [
            "Press R to restart the game.",
            "Press M to go back to the main menu.",
            "Use UP/DOWN to scroll."
        ]
        for idx, text in enumerate(instructions):
            instruction_surface = self.font.render(text, True, (255, 255, 255))
            self.screen.blit(instruction_surface, (50, self.screen.get_height() - 120 + idx * 30))

        # Display the user's score and rank at the bottom
        user_rank = self.scores.index(user_score) + 1
        user_score_text = f"Your Score: {user_score} (Rank: {user_rank})"
        user_score_surface = self.font.render(user_score_text, True, (255, 255, 0))
        self.screen.blit(user_score_surface, (self.screen.get_width() // 2 - user_score_surface.get_width() // 2,
                                             self.screen.get_height() - 60))

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart the game
                    self.restart_callback()
                    return False  # Stop running
                elif event.key == pygame.K_m:  # Go back to main menu
                    MainMenu(self.screen).run()
                    return False  # Stop running
                elif event.key == pygame.K_UP:  # Scroll up
                    self.scroll_offset = max(0, self.scroll_offset - 1)
                elif event.key == pygame.K_DOWN:  # Scroll down
                    self.scroll_offset = min(len(self.scores) - self.max_display, self.scroll_offset + 1)
        return True

    def run(self, user_score):
        running = True
        while running:
            running = self.handle_events()
            self.render(user_score)
