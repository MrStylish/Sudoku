"""
Eindopdracht Sudoku, Oktay Beyaz ID1G1A
Sudoku met vier verschillende levels
Datum begonnen: 22-10-2020, Datum afgerond: 26-10-2020
"""

from os import sys
import requests
import pygame
from bs4 import BeautifulSoup
from settings import *
from buttons_class import *

__author__ = "Oktay Beyaz"
__copyright__ = "Copyright 2020, Oktay Beyaz"
__credits__ = "Oktay Beyaz, Marnix J.F. Lourens"
__license__ = "GNU General Public License v3.0"
__version__ = "Final"
__maintainer__ = "Oktay Beyaz"
__email__ = "Oktay.Beyaz@hva.nl"
__status__ = "Production"

class App:
    """Creates UI and initiates the game."""
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True
        self.grid = FINISHED_BOARD
        self.selected = None
        self.mouse_pos = None
        self.state = "playing"
        self.finished = False
        self.cell_changed = False
        self.playing_buttons = []
        self.locked_cells = []
        self.incorrect_cells = []
        self.font = pygame.font.SysFont("arial", CELL_SIZE//2)
        self.grid = []
        self.get_puzzle("4")
        self.load()

    def run(self):
        """Starts the pygame window."""
        while self.running:
            if self.state == "playing":
                self.playing_events()
                self.playing_update()
                self.playing_draw()
        pygame.quit()
        sys.exit()

###### PLAYING STATE FUNCTIONS #####

    def playing_events(self):
        """Defines the playable actions."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # User clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                selected = self.mouse_on_grid()
                if selected:
                    self.selected = selected
                else:
                    self.selected = None
                    for button in self.playing_buttons:
                        if button.highlighted:
                            button.click()

            # User types a key
            if event.type == pygame.KEYDOWN:
                if self.selected != 0 and self.selected not in self.locked_cells:
                    if self.is_int(event.unicode):
                        # cell changed
                        self.grid[self.selected[1]][self.selected[0]] = int(event.unicode)
                        self.cell_changed = True

    def playing_update(self):
        """Defines position of mouse."""
        self.mouse_pos = pygame.mouse.get_pos()
        for button in self.playing_buttons:
            button.update(self.mouse_pos)

    def cell_changed(self):
        """If cell changes correct means finished.
           If cell changes incorrect means board not done. """
        if self.cell_changed:
            self.incorrect_cells = []
            if self.all_cells_done():
                # Check if board is correct
                self.check_all_cells()
                if len(self.incorrect_cells) == 0:
                    self.finished = True


    def playing_draw(self):
        """Colour of cell changes after input."""
        self.window.fill(WHITE)

        for button in self.playing_buttons:
            button.draw(self.window)

        if self.selected:
            self.draw_selection(self.window, self.selected)

        self.shadelocked_cells(self.window, self.locked_cells)
        self.shadeincorrect_cells(self.window, self.incorrect_cells)

        self.draw_numbers(self.window)

        self.draw_grid(self.window)
        pygame.display.update()
        self.cell_changed = False

##### BOARD CHECKING FUNCTIONS #####
    def all_cells_done(self):
        """Clears cells after completion."""
        for row in self.grid:
            for number in row:
                if number == 0:
                    return False
        return True

    def check_all_cells(self):
        """"Checks the cells."""
        self.check_rows()
        self.check_cols()
        self.check_small_grid()

    def check_small_grid(self):
        """Checks 3x3 area."""
        for x in range(3):
            for y in range(3):
                possibles = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                # print("re-setting possibles")
                for i in range(3):
                    for j in range(3):
                        # print(x*3+i, y*3+j)
                        xidx = x*3+i
                        yidx = y*3+j
                        if self.grid[yidx][xidx] in possibles:
                            possibles.remove(self.grid[yidx][xidx])
                        else:
                            if [xidx, yidx] not in self.locked_cells and [xidx, yidx] not in self.incorrect_cells:
                                self.incorrect_cells.append([xidx, yidx])
                            if [xidx, yidx] in self.locked_cells:
                                for k in range(3):
                                    for l in range(3):
                                        xidx2 = x*3+k
                                        yidx2 = y*3+l
                                        if self.grid[yidx2][xidx2] == self.grid[yidx][xidx] and [xidx2, yidx2] not in self.locked_cells:
                                            self.incorrect_cells.append([xidx2, yidx2])

    def check_rows(self):
        """Checks if row are correct."""
        for yidx, row in enumerate(self.grid):
            possibles = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            for xidx in range(9):
                if self.grid[yidx][xidx] in possibles:
                    possibles.remove(self.grid[yidx][xidx])
                else:
                    if [xidx, yidx] not in self.locked_cells and [xidx, yidx] not in self.incorrect_cells:
                        self.incorrect_cells.append([xidx, yidx])
                    if [xidx, yidx] in self.locked_cells:
                        for k in range(9):
                            if self.grid[yidx][k] == self.grid[yidx][xidx] and [k, yidx] not in self.locked_cells:
                                self.incorrect_cells.append([k, yidx])


    def check_cols(self):
        """Checks if cols are correct."""
        for xidx in range(9):
            possibles = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            for yidx, row in enumerate(self.grid):
                if self.grid[yidx][xidx] in possibles:
                    possibles.remove(self.grid[yidx][xidx])
                else:
                    if [xidx, yidx] not in self.locked_cells and [xidx, yidx] not in self.incorrect_cells:
                        self.incorrect_cells.append([xidx, yidx])
                    if [xidx, yidx] in self.locked_cells:
                        for k, row in enumerate(self.grid):
                            if self.grid[k][xidx] == self.grid[yidx][xidx] and [xidx, k] not in self.locked_cells:
                                self.incorrect_cells.append([xidx, k])

##### HELPER FUNCTIONS #####
    def get_puzzle(self, difficulty):
        """Sets difficulty level"""
        html_doc = requests.get("https://nine.websudoku.com/?level={}".format(difficulty)).content
        soup = BeautifulSoup(html_doc)
        ids = ['f00', 'f01', 'f02', 'f03', 'f04', 'f05', 'f06', 'f07', 'f08', 'f10', 'f11',
               'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f20', 'f21', 'f22', 'f23',
               'f24', 'f25', 'f26', 'f27', 'f28', 'f30', 'f31', 'f32', 'f33', 'f34', 'f35',
               'f36', 'f37', 'f38', 'f40', 'f41', 'f42', 'f43', 'f44', 'f45', 'f46', 'f47',
               'f48', 'f50', 'f51', 'f52', 'f53', 'f54', 'f55', 'f56', 'f57', 'f58', 'f60',
               'f61', 'f62', 'f63', 'f64', 'f65', 'f66', 'f67', 'f68', 'f70', 'f71', 'f72',
               'f73', 'f74', 'f75', 'f76', 'f77', 'f78', 'f80', 'f81', 'f82', 'f83', 'f84',
               'f85', 'f86', 'f87', 'f88']
        data = []
        for cid in ids:
            data.append(soup.find('input', id=cid))
        board = [[0 for x in range(9)] for x in range(9)]
        for index, cell in enumerate(data):
            try:
                board[index//9][index%9] = int(cell['value'])
            except:
                pass
        self.grid = board
        self.load()

    def shadeincorrect_cells(self, window, incorrect):
        """Changes colour for wrong answer."""
        for cell in incorrect:
            pygame.draw.rect(window, INCORRECT_CELL_COLOUR, (cell[0]*CELL_SIZE+GRID_POS[0], cell[1]*CELL_SIZE+GRID_POS[1], CELL_SIZE, CELL_SIZE))

    def shadelocked_cells(self, window, locked):
        """Changes colour for locked numbers."""
        for cell in locked:
            pygame.draw.rect(window, LOCKED_CELL_COLOUR, (cell[0]*CELL_SIZE+GRID_POS[0], cell[1]*CELL_SIZE+GRID_POS[1], CELL_SIZE, CELL_SIZE))

    def draw_numbers(self, window):
        """Puts starting numbers on board."""
        for yidx, row in enumerate(self.grid):
            for xidx, num in enumerate(row):
                if num != 0:
                    pos = [(xidx*CELL_SIZE)+GRID_POS[0], (yidx*CELL_SIZE)+GRID_POS[1]]
                    self.text_to_screen(window, str(num), pos)

    def draw_selection(self, window, pos):
        """Selected cell turns LIGHT_BLUE."""
        pygame.draw.rect(window, LIGHT_BLUE, ((pos[0]*CELL_SIZE)+GRID_POS[0], (pos[1]*CELL_SIZE)+GRID_POS[1], CELL_SIZE, CELL_SIZE))

    def draw_grid(self, window):
        """Makes a 9x9 area grid."""
        pygame.draw.rect(window, BLACK, (GRID_POS[0], GRID_POS[1], WIDTH-150, HEIGHT-150), 2)
        for x in range(9):
            pygame.draw.line(window, BLACK, (GRID_POS[0]+(x*CELL_SIZE), GRID_POS[1]), (GRID_POS[0]+(x*CELL_SIZE), GRID_POS[1]+450), 2 if x % 3 == 0 else 1)
            pygame.draw.line(window, BLACK, (GRID_POS[0], GRID_POS[1]+(x*CELL_SIZE)), (GRID_POS[0]+450, GRID_POS[1]++(x*CELL_SIZE)), 2 if x % 3 == 0 else 1)

    def mouse_on_grid(self):
        """Disables mouseclicks outside of the board."""
        if self.mouse_pos[0] < GRID_POS[0] or self.mouse_pos[1] < GRID_POS[1]:
            return False
        if self.mouse_pos[0] > GRID_POS[0]+GRID_SIZE or self.mouse_pos[1] > GRID_POS[1]+GRID_SIZE:
            return False
        return ((self.mouse_pos[0]-GRID_POS[0])//CELL_SIZE, (self.mouse_pos[1]-GRID_POS[1])//CELL_SIZE)

    def load_buttons(self):
        """Renders the buttons."""
        self.playing_buttons.append(Button(20, 40, WIDTH//7, 40,
                                           function=self.check_all_cells,
                                           colour=(27, 142, 207),
                                           text="Check"))
        self.playing_buttons.append(Button(140, 40, WIDTH//7, 40,
                                           colour=(117, 172, 112),
                                           function=self.get_puzzle,
                                           params="1",
                                           text="Easy"))
        self.playing_buttons.append(Button(WIDTH//2-(WIDTH//7)//2, 40, WIDTH//7, 40,
                                           colour=(204, 197, 110),
                                           function=self.get_puzzle,
                                           params="2",
                                           text="Medium"))
        self.playing_buttons.append(Button(380, 40, WIDTH//7, 40,
                                           colour=(199, 129, 48),
                                           function=self.get_puzzle,
                                           params="3",
                                           text="Hard"))
        self.playing_buttons.append(Button(500, 40, WIDTH//7, 40,
                                           colour=(207, 68, 68),
                                           function=self.get_puzzle,
                                           params="4",
                                           text="Evil"))

    def text_to_screen(self, window, text, pos):
        """Adds text to buttons."""
        font = self.font.render(text, False, BLACK)
        font_width = font.get_width()
        font_height = font.get_height()
        pos[0] += (CELL_SIZE-font_width)//2
        pos[1] += (CELL_SIZE-font_height)//2
        window.blit(font, pos)

    def load(self):
        """Loads buttons"""
        self.playing_buttons = []
        self.load_buttons()
        self.locked_cells = []
        self.incorrect_cells = []
        self.finished = False

        # Setting locked cells from original board
        for yidx, row in enumerate(self.grid):
            for xidx, num in enumerate(row):
                if num != 0:
                    self.locked_cells.append([xidx, yidx])

    def is_int(self, string):
        """Defines the scopes of input"""
        try:
            int(string)
            return True
        except:
            return False
