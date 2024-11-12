import pygame
import sys
from screens.credits_instructions import show_instructions  # Assuming this is used for credits reference

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def oscillation_explanation(screen, retry_callback):
    pygame.init()
    font = pygame.font.Font('./fonts/PressStart2P-Regular.ttf', 16)
    clock = pygame.time.Clock()
    scroll_y = 0  # For text scrolling (manual control if needed)

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

    running = True
    scroll_speed = 0  # Scroll speed set to 0 for no automatic scrolling

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Call the retry callback function to restart the game
                running = False  # Exit the loop before calling the callback
                retry_callback()
                return  # Exit the function to avoid re-running this loop

        # Draw the explanation text, scrolling it if needed
        y_offset = 50 + scroll_y
        for line in explanation_text:
            text_surface = font.render(line, True, WHITE)
            screen.blit(text_surface, (20, y_offset))
            y_offset += 30  # Line spacing

        pygame.display.flip()
        clock.tick(30)

        # Manual scrolling control (if needed)
        scroll_y += scroll_speed
