from grid import Grid
from blocks import *
import random
import pygame

class Game:
    def __init__(self):
        self.grid = Grid()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), ZBlock(), TBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.game_over = False
        self.waiting_for_restart = False
        self.game_over_sound_played = False
        self.score = 0
        self.rotate_sound = pygame.mixer.Sound("Sounds//Click Sound.mp3")
        self.clear_sound = pygame.mixer.Sound("Sounds//Extra Point Sound.mp3")
        self.tetris_clear_sound = pygame.mixer.Sound("Sounds//Tetris Sound.mp3")

        pygame.mixer.music.load("Sounds//Tetris Theme Sound.mp3")
        pygame.mixer.music.play(-1)

    # Updates score based on how many rows were cleared
    def update_score(self, rows_cleared, move_down_points):
        if rows_cleared == 1:
            self.score += 100
        elif rows_cleared == 2:
            self.score += 300
        elif rows_cleared == 3:
            self.score += 500
        elif rows_cleared == 4:
            self.score += 1000
        self.score += move_down_points

    # Picks random block from list of 7 possible tetris blocks
    def get_random_block(self):
        if len(self.blocks) == 0:
            self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), ZBlock(), TBlock()]
        block = random.choice(self.blocks)
        self.blocks.remove(block)
        return block

    # Moves block 1 to the left
    def move_left(self):
        self.current_block.move(0, -1)

        # Verifies that it moves within the bounds of the grid
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, 1)

    # Moves block 1 to the right
    def move_right(self):
        self.current_block.move(0, 1)

        # Verifies that it moves within the bounds of the grid
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, -1)

    # Moves block 1 down
    def move_down(self):
        self.current_block.move(1, 0)

        # Verifies that it moves within the bounds of the grid
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(-1, 0)
            self.lock_block()

    # Locks the current block in place, checks for row clears, and handles game over condition
    def lock_block(self):
        tiles = self.current_block.get_cell_positions()
        for position in tiles:
            self.grid.grid[position.row][position.column] = self.current_block.id
        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        rows_cleared = self.grid.clear_full_rows()

        if rows_cleared > 0 and rows_cleared < 4:
            self.clear_sound.play()
            self.update_score(rows_cleared, 0)
        elif rows_cleared == 4:
            self.tetris_clear_sound.play()
            self.update_score(rows_cleared, 0)

        # If current block overlaps with another block, game is over as the top of the grid has been reached
        if self.block_fits() == False:
            self.game_over = True
            self.waiting_for_restart = True
            self.game_over_sound_played = False
    
    # Resets game state for a new game
    def reset(self):
        self.grid.reset()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), ZBlock(), TBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.score = 0

    # Checks if the current block fits within the grid without overlapping existing blocks
    def block_fits(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_empty(tile.row, tile.column) == False:
                return False
        return True

    # Rotates block
    def rotate(self):
        self.current_block.rotate()

        # Verifies that it rotates within the bounds of the grid
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.undo_rotation()
        else:
            self.rotate_sound.play()

    # Verifies that block is within the bounds of the grid
    def block_inside(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_inside(tile.row, tile.column) == False:
                return False
        return True

    # Displays blocks and grid
    def draw(self, screen):
        self.grid.draw(screen)
        self.current_block.draw(screen, 11, 11)

        if self.next_block.id == 3:
            self.next_block.draw(screen, 255, 290)
        elif self.next_block.id == 4:
            self.next_block.draw(screen, 255, 280)
        else:
            self.next_block.draw(screen, 270, 270)