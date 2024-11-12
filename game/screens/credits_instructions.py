import pygame
import sys

def show_instructions(screen, main_menu_callback):
    pygame.init()
    clock = pygame.time.Clock()

    # Load retro soundtrack
    # pygame.mixer.music.load('retro_soundtrack.ogg')
    # pygame.mixer.music.play(-1)  # Loop indefinitely

    # Load logo (if available)
    logo = pygame.image.load('./images/logo.png')  # Replace 'logo.png' with your actual logo file
    logo = pygame.transform.scale(logo, (300, 100))  # Adjust size as needed

    # Set up Pac-Man font (download and place in project directory)
    pacman_font = pygame.font.Font('./fonts/PressStart2P-Regular.ttf', 20)  # Adjust font size as needed
    credit_text = [
        "Welcome to the Q-Learning and Dijkstra's Algorithm Demonstration!",
        "",
        "Credits:",
        "Lead Developer: Dakota, Vishnu, Khoi, Chris",
        "Special Thanks: Olin College PIE Teaching Team",
        "",
        "About the Demonstration:",
        "Q-Learning is a reinforcement learning technique used to train agents through exploration and rewards.",
        "",
        "Dijkstra's Algorithm finds the shortest paths between nodes in a graph, often used in routing and pathfinding problems.",
        "",
        "Game Controls:",
        "- Use Arrow Keys to move",
        "- Press Enter to start",
        "- Press Space to select",
        "",
        "Enjoy the demonstration and feel free to explore!"
        "",
        "Press Enter to go back."
    ]

    # Word wrapping function
    def wrap_text(text, font, max_width):
        lines = []
        words = text.split(' ')
        while words:
            line = ''
            while words and font.size(line + words[0])[0] <= max_width:
                line += words.pop(0) + ' '
            lines.append(line.strip())
        return lines

    # Render text surfaces with word wrapping
    max_text_width = screen.get_width() - 40  # Add some padding
    wrapped_text = []
    for line in credit_text:
        wrapped_lines = wrap_text(line, pacman_font, max_text_width)
        wrapped_text.extend(wrapped_lines)

    rendered_text = [pacman_font.render(line, True, (255, 255, 0)) for line in wrapped_text]  # Pac-Man yellow color

    # Initial positions for scrolling
    scroll_y = screen.get_height() // 2
    scroll_speed = 5  # Speed of scrolling
    scroll_acceleration = 1  # Acceleration factor for continuous pressing

    running = True
    key_up_pressed = False
    key_down_pressed = False
    while running:
        screen.fill((0, 0, 0))  # Black background

        # Display logo at the top
        screen.blit(logo, (screen.get_width() // 2 - logo.get_width() // 2, 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Press Enter to return to main menu
                    pygame.mixer.music.stop()
                    main_menu_callback()  # Call the main menu function
                    return
                elif event.key == pygame.K_UP:  # Scroll up
                    key_up_pressed = True
                elif event.key == pygame.K_DOWN:  # Scroll down
                    key_down_pressed = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    key_up_pressed = False
                elif event.key == pygame.K_DOWN:
                    key_down_pressed = False

        # Handle continuous scrolling
        if key_up_pressed:
            scroll_y += scroll_speed
            scroll_speed += scroll_acceleration  # Accelerate scrolling speed
        elif key_down_pressed:
            scroll_y -= scroll_speed
            scroll_speed += scroll_acceleration  # Accelerate scrolling speed
        else:
            scroll_speed = 5  # Reset speed if no key is pressed

        # Display scrolling text
        y_offset = scroll_y + 150  # Offset below the logo
        for text_surface in rendered_text:
            screen.blit(text_surface, (20, y_offset))  # Slight padding on the left
            y_offset += 40  # Vertical spacing between lines

        pygame.display.flip()
        clock.tick(60)
