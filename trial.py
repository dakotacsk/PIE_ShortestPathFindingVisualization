import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen settings
cell_size = 50  # Size of each grid cell
grid_size = 9   # Number of rows and columns
screen_size = cell_size * grid_size
screen = pygame.display.set_mode((screen_size, screen_size))
pygame.display.set_caption("Maze Creator")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Maze grid and character position
maze = [[0] * grid_size for _ in range(grid_size)]  # 0 = empty, 1 = wall
character_pos = [0, 0]  # Starting position in grid (row, column)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Mouse click to toggle walls
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            row, col = mouse_y // cell_size, mouse_x // cell_size
            maze[row][col] = 1 if maze[row][col] == 0 else 0  # Toggle between wall (1) and empty (0)

        # Arrow key movement for the character
        if event.type == pygame.KEYDOWN:
            row, col = character_pos
            if event.key == pygame.K_UP and row > 0 and maze[row - 1][col] == 0:
                character_pos[0] -= 1
            elif event.key == pygame.K_DOWN and row < grid_size - 1 and maze[row + 1][col] == 0:
                character_pos[0] += 1
            elif event.key == pygame.K_LEFT and col > 0 and maze[row][col - 1] == 0:
                character_pos[1] -= 1
            elif event.key == pygame.K_RIGHT and col < grid_size - 1 and maze[row][col + 1] == 0:
                character_pos[1] += 1

    # Drawing the grid
    screen.fill(WHITE)
    for row in range(grid_size):
        for col in range(grid_size):
            rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, RED if maze[row][col] == 1 else WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)

    # Draw the character
    character_x = character_pos[1] * cell_size + cell_size // 2
    character_y = character_pos[0] * cell_size + cell_size // 2
    pygame.draw.circle(screen, BLACK, (character_x, character_y), cell_size // 3)

    pygame.display.flip()
