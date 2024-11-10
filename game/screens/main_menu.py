import pygame
import sys

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.options = ["Start Game", "Instructions", "Exit Game"]
        self.selected_index = 0
        self.font = pygame.font.Font(None, 50)

    def run(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))  # Black background
            self.display_menu()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.selected_index = (self.selected_index + 1) % len(self.options)
                    elif event.key == pygame.K_UP:
                        self.selected_index = (self.selected_index - 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        if self.options[self.selected_index] == "Start Game":
                            running = False  # Proceed to next screen
                        elif self.options[self.selected_index] == "Exit Game":
                            pygame.quit()
                            sys.exit()

    def display_menu(self):
        for i, option in enumerate(self.options):
            color = (255, 0, 0) if i == self.selected_index else (255, 255, 255)
            text = self.font.render(option, True, color)
            self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, 150 + i * 60))
