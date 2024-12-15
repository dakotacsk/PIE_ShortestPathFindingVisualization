import pygame
import sys
from screens.instructions.credits_instructions import show_instructions

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.options = ["Start Game", "Instruction & Credits", "Exit Game"]
        self.selected_index = 0
        self.font = pygame.font.Font('./fonts/PressStart2P-Regular.ttf', 28)  # Pac-Man-style font
        self.blinking_logo_timer = 0
        self.blinking_logo_visible = True

        # Load logo
        self.logo = pygame.image.load('./images/logo.png')
        self.logo = pygame.transform.scale(self.logo, (500, 200))  # Resize as needed

    def run(self):
        running = True
        clock = pygame.time.Clock()
        user_choice = None  # Default

        while running:
            self.screen.fill((0, 0, 0))
            self.display_logo()
            self.display_menu()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.selected_index = (self.selected_index + 1) % len(self.options)
                    elif event.key == pygame.K_UP:
                        self.selected_index = (self.selected_index - 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        chosen_option = self.options[self.selected_index]
                        if chosen_option == "Start Game":
                            user_choice = "start"
                            running = False
                        elif chosen_option == "Instruction & Credits":
                            show_instructions(self.screen, self.run)
                        elif chosen_option == "Exit Game":
                            user_choice = "exit"
                            pygame.quit()
                            sys.exit()

            self.blinking_logo_timer += clock.tick(60)
            if self.blinking_logo_timer > 500:
                self.blinking_logo_visible = not self.blinking_logo_visible
                self.blinking_logo_timer = 0

        return user_choice  # Return the user's choice


    def display_logo(self):
        if self.blinking_logo_visible:
            # Center logo horizontally and vertically (with some adjustments)
            logo_x = self.screen.get_width() // 2 - self.logo.get_width() // 2
            logo_y = self.screen.get_height() // 3 - self.logo.get_height() // 2  # Placing in the upper-middle section
            self.screen.blit(self.logo, (logo_x, logo_y))

    def display_menu(self):
        menu_y_start = self.screen.get_height() * 2 // 3  # Start lower on the screen
        for i, option in enumerate(self.options):
            if i == self.selected_index:
                # Highlighted option
                color = (255, 255, 0)  # Pac-Man yellow color
                text = self.font.render(f"> {option} <", True, color)  # Add brackets to highlight
                # Add a pulsating effect to the highlighted option
                scale_factor = 1.1
                text = pygame.transform.scale(
                    text,
                    (int(text.get_width() * scale_factor), int(text.get_height() * scale_factor))
                )
            else:
                color = (200, 200, 200)  # Gray color for non-selected options
                text = self.font.render(option, True, color)

            # Center text horizontally
            self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, menu_y_start + i * 60))
