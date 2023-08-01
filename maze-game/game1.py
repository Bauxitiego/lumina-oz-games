import curses

class PacManGame:
    def __init__(self, map_data):
        self.width = len(map_data[0])
        self.height = len(map_data)
        self.grid = [[cell for cell in row] for row in map_data]
        self.pacman_x, self.pacman_y = self.find_pacman()
        self.game_over = False

    def find_pacman(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == 'P':
                    return x, y
        return None, None

    def draw_grid(self):
        self.window.clear()
        for row in self.grid:
            self.window.addstr(' '.join(row) + '\n')
        self.window.addstr("\nUse arrow keys to move Pac-Man. Press 'Q' to quit.")
        self.window.refresh()

    def handle_input(self):
        key = self.window.getch()
        if key == ord('q'):
            self.game_over = True
        elif key == curses.KEY_UP:
            self.move_pacman(0, -1)
        elif key == curses.KEY_DOWN:
            self.move_pacman(0, 1)
        elif key == curses.KEY_LEFT:
            self.move_pacman(-1, 0)
        elif key == curses.KEY_RIGHT:
            self.move_pacman(1, 0)

    def move_pacman(self, dx, dy):
        new_x = self.pacman_x + dx
        new_y = self.pacman_y + dy

        if (
            0 <= new_x < self.width
            and 0 <= new_y < self.height
            and self.grid[new_y][new_x] != '#'
        ):
            self.grid[self.pacman_y][self.pacman_x] = '.'
            self.pacman_x = new_x
            self.pacman_y = new_y
            self.grid[self.pacman_y][self.pacman_x] = 'P'

    def run(self):
        curses.wrapper(self._run)

    def _run(self, stdscr):
        self.window = stdscr
        curses.curs_set(0)
        while not self.game_over:
            self.draw_grid()
            self.handle_input()

if __name__ == "__main__":
    custom_map = [
        "###############",
        "#.............#",
        "#.#####.#####.#",
        "#.#...#.#...#.#",
        "#.#.###.###.#.#",
        "#.#.........#.#",
        "#.#####P#####.#",
        "#.............#",
        "###############",
    ]
    game = PacManGame(custom_map)
    game.run()
