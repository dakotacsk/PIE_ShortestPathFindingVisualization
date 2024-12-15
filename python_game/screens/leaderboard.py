import pygame
import csv
import os
import sys
from screens.main_menu import MainMenu

class Leaderboard:
    def __init__(self, screen, restart_callback, csv_filename="../python_game/leaderboard/leaderboard.csv"):
        self.screen = screen
        self.restart_callback = restart_callback
        self.csv_filename = csv_filename
        
        # Load scores immediately
        self.scores = self.load_scores()
        
        # Larger fonts for 1920x1080
        self.font = pygame.font.Font(None, 64)       # For listing scores
        self.title_font = pygame.font.Font(None, 96) # For the "Leaderboard" title
        
        self.scroll_offset = 0
        self.max_display = 10

    def load_scores(self):
        if not os.path.exists(self.csv_filename):
            os.makedirs(os.path.dirname(self.csv_filename), exist_ok=True)
            open(self.csv_filename, 'w').close()
            return []

        loaded_scores = []
        try:
            with open(self.csv_filename, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row:  # Non-empty row
                        try:
                            # If you want to treat them as floats:
                            val = float(row[0])
                            # Or if you want int:
                            # val = int(float(row[0]))
                            loaded_scores.append(val)
                        except ValueError as ve:
                            print(f"[DEBUG] Skipping invalid row {row}: {ve}")

            loaded_scores.sort(reverse=True)
            return loaded_scores
        except (IndexError, OSError) as e:
            print(f"Error loading scores: {e}")
            return []

    def save_score(self, user_score):
        """Append new scores, then re-sort descending."""
        try:
            os.makedirs(os.path.dirname(self.csv_filename), exist_ok=True)
            with open(self.csv_filename, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([user_score])
            self.scores.append(user_score)
            self.scores.sort(reverse=True)
        except OSError as e:
            print(f"Error saving score: {e}")

    def render(self, user_score):
        """Merged approach: old code's logic + bigger fonts + adjusted spacing."""
        self.screen.fill((0, 0, 0))  # Black background

        # Render title with bigger font
        title_surface = self.title_font.render("Leaderboard", True, (255, 255, 255))
        self.screen.blit(
            title_surface,
            (self.screen.get_width() // 2 - title_surface.get_width() // 2, 50)
        )

        start_index = self.scroll_offset
        end_index = min(len(self.scores), start_index + self.max_display)

        y_start = 200
        line_height = 60  # spacing between lines

        for idx in range(start_index, end_index):
            rank = idx + 1
            score = self.scores[idx]
            score_text = (
                f"{rank}th Score: {score}" if rank > 3
                else ["1st", "2nd", "3rd"][rank - 1] + f" Score: {score}"
            )
            # Highlight the user's own score
            color = (0, 255, 0) if score == user_score else (255, 255, 255)
            score_surface = self.font.render(score_text, True, color)
            y_pos = y_start + (idx - start_index) * line_height
            self.screen.blit(score_surface, (100, y_pos))

        # Instructions with moderately bigger font, not as big as the title
        instructions_font = pygame.font.Font(None, 48)
        instructions = [
            "Press R to restart the game.",
            "Press M to go back to the main menu.",
            "Use UP/DOWN to scroll."
        ]

        instruction_y = self.screen.get_height() - 220  # a bit higher up from bottom
        for idx, text in enumerate(instructions):
            instruction_surface = instructions_font.render(text, True, (255, 255, 255))
            self.screen.blit(instruction_surface, (100, instruction_y + idx * 50))

        # Render the user's final score & rank near the bottom center
        user_rank = self.scores.index(user_score) + 1 if user_score in self.scores else len(self.scores) + 1
        user_score_text = f"Your Score: {user_score} (Rank: {user_rank})"
        user_score_surface = self.font.render(user_score_text, True, (255, 255, 0))
        self.screen.blit(
            user_score_surface,
            (
                self.screen.get_width() // 2 - user_score_surface.get_width() // 2,
                self.screen.get_height() - 100
            )
        )

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart
                    self.restart_callback()
                    return False
                elif event.key == pygame.K_m:  # Back to main menu
                    from run_game import run_game
                    run_game(self.screen)
                    return False
                elif event.key == pygame.K_UP:
                    self.scroll_offset = max(0, self.scroll_offset - 1)
                elif event.key == pygame.K_DOWN:
                    max_scroll = max(0, len(self.scores) - self.max_display)
                    self.scroll_offset = min(max_scroll, self.scroll_offset + 1)
        return True

    def run(self, user_score):
        self.scroll_offset = 0
        running = True
        while running:
            running = self.handle_events()
            self.render(user_score)
