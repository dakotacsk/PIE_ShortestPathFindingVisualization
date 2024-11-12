import pygame
from screens.scrolling_texts import ScrollingTextDisplay  # Assuming you saved the class in a separate file

def show_instructions(screen, main_menu_callback):
    content = [
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
        "Enjoy the demonstration and feel free to explore!",
        "",
        "Press Enter to go back."
    ]
    title = "Instructions & Credits"
    scrolling_display = ScrollingTextDisplay(screen, title, content, logo_path='./images/logo.png')

    running = True
    while running:
        screen.fill((0, 0, 0))  # Clear the screen
        scrolling_display.scroll_content()  # Handle scrolling
        scrolling_display.render()  # Render content
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Return to the main menu when Enter is pressed
                    main_menu_callback()  # Call the main menu function
                    running = False  # Exit the loop
                elif event.key == pygame.K_UP:
                    scrolling_display.key_up_pressed = True  # Trigger scroll up
                elif event.key == pygame.K_DOWN:
                    scrolling_display.key_down_pressed = True  # Trigger scroll down
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    scrolling_display.key_up_pressed = False  # Stop scroll up
                elif event.key == pygame.K_DOWN:
                    scrolling_display.key_down_pressed = False  # Stop scroll down
