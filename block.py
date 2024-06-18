from colours import Colours
from position import Position
import pygame

class Block:
    def __init__(self, id):
        self.id = id
        self.cells = {}
        self.cell_size = 30
        self.row_offset = 0
        self.column_offset = 0
        self.rotation_state = 0
        self.colours = Colours.get_cell_colours()

    # Moves blocks relative to where they are
    def move(self, rows, columns):
        self.row_offset += rows
        self.column_offset += columns

    # Verifies where each cell is in the grid
    def get_cell_positions(self):
        tiles = self.cells[self.rotation_state]
        moved_tiles = []
        for position in tiles:
            position = Position(position.row + self.row_offset, position.column + self.column_offset)
            moved_tiles.append(position)
        return moved_tiles

    # Rotates blocks based on rotation state
    def rotate(self):
        self.rotation_state += 1

        if self.rotation_state == len(self.cells):
            self.rotation_state = 0

    # Undoes rotation if block would be out of bounds
    def undo_rotation(self):
        self.rotation_state -= 1
        if self.rotation_state == -1:
            self.rotation_state = len(self.cells) - 1

    # Displays blocks and cells
    def draw(self, screen, offset_x, offset_y):
        tiles = self.get_cell_positions()
        for tile in tiles:
            tile_rect = pygame.Rect(offset_x + tile.column * self.cell_size, offset_y + tile.row * self.cell_size, self.cell_size - 1, self.cell_size - 1)
            pygame.draw.rect(screen, self.colours[self.id], tile_rect)