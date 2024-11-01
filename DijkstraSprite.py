import pygame
import heapq
BLACK = (0, 0, 0)

class DijkstraSprite:
    def __init__(self, start_pos, cell_size, grid):
        self.position = start_pos
        self.cell_size = cell_size
        self.path = []
        self.grid = grid

    def set_path(self, start, final_goal):
        # Ensure we visit all rewards and then reach the final goal
        waypoints = [start] + list(self.grid.rewards) + [final_goal]
        self.path = self.compute_path_through_waypoints(waypoints)

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
                if (0 <= n_row < self.grid.grid_size and 0 <= n_col < self.grid.grid_size 
                    and not self.grid.is_wall(n_row, n_col)):  # Skip walls
                    distance = current_distance + 1
                    if neighbor not in distances or distance < distances[neighbor]:
                        distances[neighbor] = distance
                        previous_nodes[neighbor] = current_position
                        heapq.heappush(queue, (distance, neighbor))

        path = []
        current = end
        while current is not None:
            path.insert(0, list(current))
            current = previous_nodes.get(current)
        return path

    def follow_path(self):
        if self.path:
            self.position = self.path.pop(0)

    def draw(self, screen):
        x, y = self.position[1] * self.cell_size + self.cell_size // 2, self.position[0] * self.cell_size + self.cell_size // 2
        pygame.draw.circle(screen, BLACK, (x, y), self.cell_size // 3)
