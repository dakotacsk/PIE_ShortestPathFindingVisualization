import pygame
import csv
import os
import sys

# Fallback resource_path function
def resource_path(relative_path):
    """ Get absolute path to resource, compatible with PyInstaller and normal runs """
    if getattr(sys, 'frozen', False):  # PyInstaller bundle
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")  # Current directory for normal runs
    return os.path.join(base_path, relative_path)

class Leaderboard:
    def __init__(self, screen, restart_callback, csv_filename=resource_path("leaderboard/leaderboard.csv"),
                 font_path=resource_path("fonts/PressStart2P-Regular.ttf")):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.restart_callback = restart_callback
        self.csv_filename = csv_filename

        # Debug print to check path resolution
        print(f"[DEBUG] CSV File Path: {self.csv_filename}")

        # Fonts
        self.title_font = pygame.font.Font(font_path, 42)  # Reduced font size for title
        self.score_font = pygame.font.Font(font_path, 20)  # Slightly smaller for scores
        self.instruction_font = pygame.font.Font(font_path, 16)  # Reduced instructions font

        # Screen dimensions
        self.screen_width = 1360
        self.screen_height = 768

        # Scrolling
        self.scroll_offset = 0
        self.key_up_pressed = False
        self.key_down_pressed = False

        # Leaderboard data
        self.scores = self.load_scores()

        # UI constants
        self.title_y = 30
        self.score_y_start = 100
        self.line_height = 40  # Space between rows
        self.max_display = 10  # Max scores displayed at a time

    def load_scores(self):
        """Load scores from a CSV file."""
        if not os.path.exists(self.csv_filename):
            os.makedirs(os.path.dirname(self.csv_filename), exist_ok=True)
            open(self.csv_filename, 'w').close()
            return []

        loaded_scores = []
        with open(self.csv_filename, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                try:
                    if row:
                        loaded_scores.append(float(row[0]))
                except ValueError:
                    print(f"[DEBUG] Skipping invalid row: {row}")
        return sorted(loaded_scores, reverse=True)

    def save_score(self, user_score):
        """Save a new score to the leaderboard."""
        with open(self.csv_filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([user_score])
        self.scores.append(user_score)
        self.scores.sort(reverse=True)

    def scroll_content(self):
        """Handle scrolling logic with one row at a time."""
        max_scroll = max(0, len(self.scores) - self.max_display)  # Allow scrolling up to hidden rows
        if self.key_up_pressed:
            self.scroll_offset = max(0, self.scroll_offset - 1)  # Scroll up by one row
            self.key_up_pressed = False  # Reset key press to avoid rapid scroll
        elif self.key_down_pressed:
            self.scroll_offset = min(max_scroll, self.scroll_offset + 1)  # Scroll down by one row
            self.key_down_pressed = False  # Reset key press to avoid rapid scroll

    def render(self, user_score):
        """Render the leaderboard screen."""
        self.screen.fill((0, 0, 0))  # Black background

        # Title
        title_surface = self.title_font.render("Leaderboard", True, (255, 255, 0))
        self.screen.blit(title_surface, (self.screen_width // 2 - title_surface.get_width() // 2, self.title_y))

        # Render scores
        y_start = self.score_y_start
        for i in range(self.scroll_offset, min(len(self.scores), self.scroll_offset + self.max_display)):
            rank = i + 1
            score = self.scores[i]
            score_text = f"{rank}. {score:.2f}"
            color = (0, 255, 0) if score == user_score else (255, 255, 255)
            score_surface = self.score_font.render(score_text, True, color)
            self.screen.blit(score_surface, (100, y_start + (i - self.scroll_offset) * self.line_height))

        # Instructions
        instruction_y = self.screen_height - 120
        instructions = [
            "Press SPACE to restart.",
            "Press ENTER for main menu.",
            "Use UP/DOWN to scroll."
        ]
        for idx, line in enumerate(instructions):
            instruction_surface = self.instruction_font.render(line, True, (255, 255, 255))
            self.screen.blit(instruction_surface, (100, instruction_y + idx * 25))

        # Final user score
        user_rank = self.scores.index(user_score) + 1 if user_score in self.scores else len(self.scores) + 1
        user_score_text = f"Your Score: {user_score:.2f} (Rank: {user_rank})"
        user_score_surface = self.instruction_font.render(user_score_text, True, (255, 255, 0))  # Smaller font
        self.screen.blit(
            user_score_surface,
            (self.screen_width // 2 - user_score_surface.get_width() // 2, self.screen_height - 50)
        )

        pygame.display.flip()

    def handle_events(self):
        """Handle user input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Restart game
                    self.restart_callback()
                    return False
                elif event.key == pygame.K_RETURN:  # Return to main menu
                    from run_game import run_game
                    run_game(self.screen)
                    return False
                elif event.key == pygame.K_UP:
                    self.key_up_pressed = True  # Single upward scroll
                elif event.key == pygame.K_DOWN:
                    self.key_down_pressed = True  # Single downward scroll
        return True

    def run(self, user_score):
        """Main loop for the leaderboard."""
        running = True
        while running:
            self.scroll_content()
            running = self.handle_events()
            self.render(user_score)
            self.clock.tick(60)
