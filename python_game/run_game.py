import pygame
from utils import resource_path  # Import the resource_path function
from screens.main_menu import MainMenu
from screens.intro_cutscene import IntroCutscene
from screens.instructions.instructions import Instructions
from screens.game1 import Game1
from screens.game2 import Game2

def run_game(screen):
    choice = MainMenu(screen).run()  # Get user choice from main menu

    if choice == "start":
        # If the user pressed "Start Game", run the rest:
        # Intro cutscene
        cutscene = IntroCutscene(screen)
        cutscene.run()

        # Instructions
        instructions = Instructions(screen)
        instructions.run()

        # Game 1 (Dijkstra)
        game1 = Game1(screen)
        game1.run()

        # Game 2 (Q-Learning)
        game2 = Game2(screen)
        game2.run()

    elif choice == "exit":
        # If the user selected "Exit Game", do nothing and let `main` handle quitting
        pass

def main():
    # Initialize Pygame
    pygame.init()

    # Load icon dynamically
    icon = pygame.image.load(resource_path("images/logo.png"))
    pygame.display.set_icon(icon)

    # Set up the game window
    screen = pygame.display.set_mode((1360, 768))
    pygame.display.set_caption("Hatchling's Quest: Pathfinding Trials")
    
    running = True
    while running:
        run_game(screen)  # run_game now has logic to decide if we continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                break  # Press "R" to replay everything

    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()
