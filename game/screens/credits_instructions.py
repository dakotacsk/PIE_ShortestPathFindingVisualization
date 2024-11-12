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
    scrolling_display.run(main_menu_callback)
