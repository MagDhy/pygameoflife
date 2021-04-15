import random
import sys
import pygame

# TODO package as pip package
# TODO push on github and pypi ?


class LifeGame:
    def __init__(self, screen_width=800, screen_height=600, cell_size=10, alive_color=(0, 255, 255), dead_color=(0, 0, 0),
                 max_fps=10):
        """
        Initialize grid, set default state, initialize screen.
        :param screen_width: game window width
        :param screen_height: game window height
        :param cell_size: diameter of circles
        :param alive_color: RGB tuple e.g. (255, 255, 255) for cells
        :param dead_color: RGB tuple e.g. (255, 255, 255)
        :param max_fps: frame rate cap to limit game speed
        """
        pygame.init()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.cell_size = cell_size
        self.alive_color = alive_color
        self.dead_color = dead_color
        self.max_fps = max_fps

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clear_screen()
        pygame.display.flip()  # flip() to push drawing into memory

        self.desired_milliseconds_between_updates = (1.0 / self.max_fps) * 1000.0
        self.last_update_cplt = 0

        self.active_grids = 0

        self.num_cols = self.screen_width // self.cell_size
        self.num_rows = self.screen_height // self.cell_size
        self.grids = []
        self.init_grids()
        self.set_grid()

        self.paused = False
        self.game_over = False

    def init_grids(self):
        """
        Create an stores the default active and inactive grid.
        :return: none
        """
        def create_grid():
            """
            Generate an empty (2?) grid
            :return: the grid
            """
            rows = []
            for row_num in range(self.num_rows):
                list_cols = [0] * self.num_cols
                rows.append(list_cols)
            return rows

        self.grids.append(create_grid())
        self.grids.append(create_grid())

    def set_grid(self, value=None, grid=0):
        """
        Set an entire grid at once, set to a single value or random 0/1.
        Examples:
            set_grid(0) == all dead,
            set_grid(1) == all alive and
            set_grid() == random == set_grid(None)

        :param value: value to set the cell to (0 or 1)
        :param grid: index of grid, for active/inactive (0/1)
        :return:
        """
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                if value is None:
                    cell_value = random.randint(0, 1)
                else:
                    cell_value = value
                self.grids[grid][r][c] = cell_value

    def draw_grid(self):
        """
        Given the grid and cell states, draw the cells on the screen
        :return:
        """
        # circle(Surface, color, pos, radius, width=0 [ou juste 0]) -> Rect
        self.clear_screen()
        for c in range(self.num_cols):
            for r in range(self.num_rows):
                if self.grids[self.active_grids][r][c] == 1:
                    color = self.alive_color
                else:
                    color = self.dead_color
                pygame.draw.circle(self.screen, color, (c * self.cell_size + (self.cell_size // 2),
                                                        r * self.cell_size + (self.cell_size // 2)),
                                   self.cell_size // 2, 0)
        pygame.display.flip()  # flip() to push drawing into memory

    def clear_screen(self):
        """
        Fill whole screen with dead color
        :return:
        """
        self.screen.fill(self.dead_color)

    def get_cell(self, row_num, col_num):
        """
        Get the alive/dead (0/1) state of a specific cell in active grid
        :param row_num:
        :param col_num:
        :return: 0 or 1 depending on state of cell, defaults to 0 (dead)
        """
        try:
            cell_value = self.grids[self.active_grids][row_num][col_num]
        except:
            cell_value = 0
        return cell_value

    def check_cell_neighbors(self, row_index, col_index):
        """
        Get the number of alive neighbor cells, and determine the state of the cell
        for next generation. Determine whether it lives, dies, survives, or is born.
        :param row_index: row number of the cell to check
        :param col_index: column number of the cell to check
        :return: the state the cell should be in next generation (0 or 1)
        """
        num_alive_neighbors = 0
        num_alive_neighbors += self.get_cell(row_index - 1, col_index - 1)
        num_alive_neighbors += self.get_cell(row_index - 1, col_index)
        num_alive_neighbors += self.get_cell(row_index - 1, col_index + 1)
        num_alive_neighbors += self.get_cell(row_index, col_index - 1)
        num_alive_neighbors += self.get_cell(row_index, col_index + 1)
        num_alive_neighbors += self.get_cell(row_index + 1, col_index - 1)
        num_alive_neighbors += self.get_cell(row_index + 1, col_index)
        num_alive_neighbors += self.get_cell(row_index + 1, col_index + 1)

        # rules for alive and dead cell
        if self.grids[self.active_grids][row_index][col_index] == 1:  # alive
            if num_alive_neighbors > 3:  # overpopulation
                return 0
            if num_alive_neighbors < 2:  # underpopulation
                return 0
            if num_alive_neighbors == 2 or num_alive_neighbors == 3:
                return 1
        elif self.grids[self.active_grids][row_index][col_index] == 0:  # dead
            if num_alive_neighbors == 3:  # come to life
                return 1
        return self.grids[self.active_grids][row_index][col_index]

    def update_generation(self):
        """
        Inspect current generation state, prepare next generation
        :return:
        """
        self.set_grid(0, self.inactive_grid())
        for r in range(self.num_rows - 1):
            for c in range(self.num_cols - 1):
                next_gen_state = self.check_cell_neighbors(r, c)
                self.grids[self.inactive_grid()][r][c] = next_gen_state
        self.active_grids = self.inactive_grid()

    def inactive_grid(self):
        """
        Simple helper function to get the index of the inactive grid.
        :return: If active grid is 0 return 1 if active grid is 1 return 0
        """
        return (self.active_grids + 1) % 2

    def handle_events(self):
        """
        Handle any key pressed
        s - start/stop (pause) the game
        r - randomize the grid
        q - exit the game
        :return:
        """
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.unicode == 's':
                    print("Toggling pause")
                    if self.paused:
                        self.paused = False
                    else:
                        self.paused = True
                elif event.unicode == 'r':
                    print("Randomizing the grid")
                    self.active_grids = 0
                    self.set_grid(None, self.active_grids)  # randomize
                    self.set_grid(0, self.inactive_grid())  # set to 0
                    self.draw_grid()
                elif event.unicode == 'q':
                    print("Exit the game")
                    self.game_over = True

            if event.type == pygame.QUIT:
                sys.exit()

    def run(self):
        """
        Kick off the game and loop forever until quit state
        :return:
        """
        while True:
            if self.game_over:
                return
            self.handle_events()
            if self.paused:
                continue
            self.update_generation()
            self.draw_grid()
            self.cap_frame_rate()

    def cap_frame_rate(self):
        """
        If the game is running too fast and updating frames too frequently,
        just wait to maintain stable framerate
        :return:
        """
        now = pygame.time.get_ticks()
        milliseconds_since_last_update = now - self.last_update_cplt
        time_to_sleep = self.desired_milliseconds_between_updates - milliseconds_since_last_update
        if time_to_sleep > 0:
            pygame.time.delay(int(time_to_sleep))
        self.last_update_cplt = now


if __name__ == "__main__":
    """
    Launch a game of life
    """
    game = LifeGame()
    game.run()
