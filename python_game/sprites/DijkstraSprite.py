import pygame
import heapq
import time

BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

class DijkstraSprite:
    def __init__(self, start_pos, cell_size, grid):
        self.position = start_pos
        self.cell_size = cell_size
        self.path = []
        self.grid = grid
        self.reached_goal = False  # Track when the goal is reached

    def set_path(self, start, final_goal):
        # Collect all green reward positions on the grid
        rewards = self.get_green_rewards()
        waypoints = [tuple(start)] + rewards + [tuple(final_goal)]
        self.path = self.compute_path_through_waypoints(waypoints)

    def get_green_rewards(self):
        # Find all green cells in the grid and treat them as rewards
        rewards = []
        for row in range(self.grid.rows):
            for col in range(self.grid.cols):
                if self.grid.maze[row][col] == GREEN:
                    rewards.append((row, col))
        return rewards

    def compute_path_through_waypoints(self, waypoints):
        # Compute a complete path visiting each waypoint in order
        full_path = []
        for i in range(len(waypoints) - 1):
            path_segment = self.dijkstra(waypoints[i], waypoints[i + 1])
            if path_segment:
                full_path.extend(path_segment[:-1])  # Avoid duplicating positions
        full_path.append(waypoints[-1])  # Add the final destination
        return full_path

    def dijkstra(self, start, end):
        distances = {start: 0}
        previous_nodes = {start: None}
        queue = [(0, start)]

        while queue:
            current_distance, current_position = heapq.heappop(queue)
            if current_position == end:
                break

            row, col = current_position
            neighbors = [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]
            for neighbor in neighbors:
                n_row, n_col = neighbor
                if (0 <= n_row < self.grid.rows and 0 <= n_col < self.grid.cols 
                    and not self.grid.is_wall(n_row, n_col)):  # Skip walls
                    distance = current_distance + 1
                    if neighbor not in distances or distance < distances[neighbor]:
                        distances[neighbor] = distance
                        previous_nodes[neighbor] = current_position
                        heapq.heappush(queue, (distance, neighbor))

        path = []
        current = end
        while current is not None:
            path.insert(0, list(current))  # Convert back to list if needed
            current = previous_nodes.get(current)
        return path

    def follow_path(self):
        if self.path:
            self.position = self.path.pop(0)
            if not self.path:
                self.reached_goal = True  # Set flag when reaching the final position
            time.sleep(0.3)

    def draw(self, screen):
        x, y = self.position[1] * self.cell_size + self.cell_size // 2, self.position[0] * self.cell_size + self.cell_size // 2
        color = YELLOW if self.reached_goal else BLACK  # Change color to yellow if goal is reached
        # Load the image
        image = pygame.image.load('./images/cuteturtle.png')

        # Optionally, scale the image to match the circle's radius
        image = pygame.transform.scale(image, (self.cell_size // 3 * 2, self.cell_size // 3 * 2))

        # Draw the image at position (x, y)
        screen.blit(image, (x - image.get_width() // 2, y - image.get_height() // 2))