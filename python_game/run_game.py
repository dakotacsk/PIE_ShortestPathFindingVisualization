import pygame
from screens.main_menu import MainMenu
from screens.intro_cutscene import IntroCutscene
from screens.instructions.instructions import Instructions
from screens.game1 import Game1
from screens.game2 import Game2

def main():
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))  # Adjust screen size as needed
    pygame.display.set_caption("Hatchling's Quest: Pathfinding Trials")
    
    # Main menu screen
    menu = MainMenu(screen)
    menu.run()

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

    pygame.quit()

if __name__ == "__main__":
    main()
