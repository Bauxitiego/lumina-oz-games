import pygame
import sys

class PacManGame:
    def __init__(self, map_data):
        self.cell_size = 30  # Adjust this value to fit the maze
        self.width = len(map_data[0]) * self.cell_size
        self.height = len(map_data) * self.cell_size
        self.grid = [[cell for cell in row] for row in map_data]
        self.pacman_x, self.pacman_y = self.find_pacman()
        self.direction = {'up': False, 'down': False, 'left': False, 'right': False}
        self.game_over = False
        self.clock = pygame.time.Clock()

    def find_pacman(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] == 'P':
                    return x, y
        return -1, -1  # Return a valid position even if Pac-Man is not found

    def draw_grid(self, screen):
        screen.fill((0, 0, 0))  # Clear the screen before drawing the grid
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] == '#':
                    pygame.draw.rect(screen, (0, 0, 255), (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
                elif self.grid[y][x] == '.':
                    pygame.draw.circle(screen, (255, 255, 0), (x * self.cell_size + self.cell_size // 2, y * self.cell_size + self.cell_size // 2), 4)
                elif self.grid[y][x] == 'P':
                    pygame.draw.rect(screen, (0, 255, 0), (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
        pygame.display.update()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.game_over = True
                elif event.key == pygame.K_UP:
                    self.direction['up'] = True
                elif event.key == pygame.K_DOWN:
                    self.direction['down'] = True
                elif event.key == pygame.K_LEFT:
                    self.direction['left'] = True
                elif event.key == pygame.K_RIGHT:
                    self.direction['right'] = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.direction['up'] = False
                elif event.key == pygame.K_DOWN:
                    self.direction['down'] = False
                elif event.key == pygame.K_LEFT:
                    self.direction['left'] = False
                elif event.key == pygame.K_RIGHT:
                    self.direction['right'] = False

    def move_pacman(self):
        dx, dy = 0, 0
        if self.direction['up']:
            dy = -1
        elif self.direction['down']:
            dy = 1
        elif self.direction['left']:
            dx = -1
        elif self.direction['right']:
            dx = 1

        new_x = (self.pacman_x + dx) % len(self.grid[0])
        new_y = self.pacman_y + dy

        # Wrap Pac-Man around vertically
        if new_y < 0:
            new_y = len(self.grid) - 1
        elif new_y >= len(self.grid):
            new_y = 0

        # Adjust Pac-Man position to wrap around horizontally
        if new_x < 0:
            new_x = len(self.grid[0]) - 1
        elif new_x >= len(self.grid[0]):
            new_x = 0

        # Check for collisions with coins and collect them
        if self.grid[new_y][new_x] == '.':
            self.grid[new_y][new_x] = ' '  # Set the cell to empty space when a coin is collected

        # Check for wall collisions
        if self.grid[new_y][new_x] != '#':
            # Update Pac-Man's current position
            self.grid[self.pacman_y][self.pacman_x] = ' '
            self.pacman_x, self.pacman_y = new_x, new_y

        # Set the current position to Pac-Man
        self.grid[self.pacman_y][self.pacman_x] = 'P'

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Pac-Man Game")

        while not self.game_over:
            self.handle_input()
            self.move_pacman()
            self.draw_grid(screen)
            self.clock.tick(10)  # Controls the game's frame rate

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    # Your map data here
    custom_map = [
        "#################################",
        "#...............................#",
        "#.#########.#####.#####.#########",
        "#.#.......#.#..........#.......#",
        "#.#.#####.#.#.#####.#####.#####.#",
        "#.#.#...#.#.#.#..........#...#.#",
        "#.#.#.#.#.#.#.#####.#####.#.#.#.#",
        "#.#.#.#.#.#.......#.......#.#.#.#",
        "#.#.#.#.#.#####.#####.#####.#.#.#",
        "#.#.#.#.#......#...........#.#.#",
        "#.#.#.#.#####.#########.#####.#.#",
        "#.#.#.#........#...........#.#.#",
        "#.#.########.#########.###.#.#.#",
        "#.#.#..........................#",
        "#.#.#########.###.###.########.#",
        "#.#.#.......#.....#.....#.....#.#",
        "#.#.#####.#.#####.#####.#.#####.#",
        "#.#...#...#.....#.#.....#...#...#",
        "#.###.#.#######.#.#.#######.#.###",
        "#.....#..........P...............#",
        "#################################",
    ]
    game = PacManGame(custom_map)
    game.run()
