# import pygame
# import sys
# import RPi.GPIO as GPIO  # Import RPi.GPIO library
# from screens.credits_instructions import show_instructions

# class MainMenu:
#     def __init__(self, screen):
#         self.screen = screen
#         self.options = ["Start Game", "Instruction & Credits", "Exit Game"]
#         self.selected_index = 0
#         self.font = pygame.font.Font('./fonts/PressStart2P-Regular.ttf', 28)  # Pac-Man-style font
#         self.blinking_logo_timer = 0
#         self.blinking_logo_visible = True

#         # Load logo
#         self.logo = pygame.image.load('./images/logo.png')
#         self.logo = pygame.transform.scale(self.logo, (500, 200))  # Resize as needed

#         # GPIO setup
#         GPIO.setmode(GPIO.BCM)  # Use Broadcom pin numbering
#         self.up_button_channel = 6
#         self.down_button_channel = 22
#         GPIO.setup(self.up_button_channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#         GPIO.setup(self.down_button_channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#     def run(self):
#         running = True
#         clock = pygame.time.Clock()
#         while running:
#             self.screen.fill((0, 0, 0))  # Black background
#             self.display_logo()
#             self.display_menu()
#             pygame.display.flip()

#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     pygame.quit()
#                     GPIO.cleanup()  # Clean up GPIO pins before exiting
#                     sys.exit()
#                 if event.type == pygame.KEYDOWN:
#                     if event.key == pygame.K_DOWN:
#                         self.selected_index = (self.selected_index + 1) % len(self.options)
#                     elif event.key == pygame.K_UP:
#                         self.selected_index = (self.selected_index - 1) % len(self.options)
#                     elif event.key == pygame.K_RETURN:
#                         if self.options[self.selected_index] == "Start Game":
#                             running = False  # Proceed to next screen
#                         elif self.options[self.selected_index] == "Instruction & Credits":
#                             show_instructions(self.screen, self.run)  # Pass self.run as the callback to return to menu
#                         elif self.options[self.selected_index] == "Exit Game":
#                             pygame.quit()
#                             GPIO.cleanup()  # Clean up GPIO pins before exiting
#                             sys.exit()

#             # Handle GPIO button input (in addition to keyboard input)
#             if not GPIO.input(self.down_button_channel):  # Button pressed (active low)
#                 self.selected_index = (self.selected_index + 1) % len(self.options)
#                 pygame.time.wait(150)  # Debounce delay

#             if not GPIO.input(self.up_button_channel):  # Button pressed (active low)
#                 self.selected_index = (self.selected_index - 1) % len(self.options)
#                 pygame.time.wait(150)  # Debounce delay

#             # Update the blinking logo timer
#             self.blinking_logo_timer += clock.tick(60)
#             if self.blinking_logo_timer > 500:  # Toggle visibility every 500 ms
#                 self.blinking_logo_visible = not self.blinking_logo_visible
#                 self.blinking_logo_timer = 0

#     def display_logo(self):
#         if self.blinking_logo_visible:
#             # Center logo horizontally and vertically (with some adjustments)
#             logo_x = self.screen.get_width() // 2 - self.logo.get_width() // 2
#             logo_y = self.screen.get_height() // 3 - self.logo.get_height() // 2  # Placing in the upper-middle section
#             self.screen.blit(self.logo, (logo_x, logo_y))

#     def display_menu(self):
#         menu_y_start = self.screen.get_height() * 2 // 3  # Start lower on the screen
#         for i, option in enumerate(self.options):
#             if i == self.selected_index:
#                 # Highlighted option
#                 color = (255, 255, 0)  # Pac-Man yellow color
#                 text = self.font.render(f"> {option} <", True, color)  # Add brackets to highlight
#                 # Add a pulsating effect to the highlighted option
#                 scale_factor = 1.1
#                 text = pygame.transform.scale(
#                     text,
#                     (int(text.get_width() * scale_factor), int(text.get_height() * scale_factor))
#                 )
#             else:
#                 color = (200, 200, 200)  # Gray color for non-selected options
#                 text = self.font.render(option, True, color)

#             # Center text horizontally
#             self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, menu_y_start + i * 60))

# # Remember to clean up GPIO when you're done
# if __name__ == "__main__":
#     pygame.init()
#     screen = pygame.display.set_mode((800, 600))  # Set your screen dimensions
#     menu = MainMenu(screen)
#     menu.run()
#     GPIO.cleanup()  # Clean up GPIO pins after exiting


import pygame
import sys
from screens.credits_instructions import show_instructions

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
        while running:
            self.screen.fill((0, 0, 0))  # Black background
            self.display_logo()
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
                        elif self.options[self.selected_index] == "Instruction & Credits":
                            show_instructions(self.screen, self.run)  # Pass self.run as the callback to return to menu
                        elif self.options[self.selected_index] == "Exit Game":
                            pygame.quit()
                            sys.exit()

            # Update the blinking logo timer
            self.blinking_logo_timer += clock.tick(60)
            if self.blinking_logo_timer > 500:  # Toggle visibility every 500 ms
                self.blinking_logo_visible = not self.blinking_logo_visible
                self.blinking_logo_timer = 0

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
