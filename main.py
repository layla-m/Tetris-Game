import pygame, sys
from game import Game
from colours import Colours

pygame.init()

# Setting default font
title_font = pygame.font.Font(None, 40)
score_surface = title_font.render("Score", True, Colours.white_purple)
next_surface = title_font.render("Next", True, Colours.white_purple)
game_over_surface = title_font.render("GAME OVER", True, Colours.white_purple)

# Area for score and next block image
score_rect = pygame.Rect(320, 55, 170, 60)
next_rect = pygame.Rect(320, 215, 170, 180)

# Game background
purple_background = Colours.purple_background

screen = pygame.display.set_mode((500, 620))
pygame.display.set_caption("Python Tetris")

game_over_sound = pygame.mixer.Sound("Sounds//Game Over Sound.mp3")

clock = pygame.time.Clock()

game = Game()

# Variables to control the continuous movement speed
move_down_delay = 200  # milliseconds
last_move_down_time = pygame.time.get_ticks()

GAME_UPDATE = pygame.USEREVENT
# Determines speed at which blocks fall down
pygame.time.set_timer(GAME_UPDATE, 450)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Checks for which key the player presses
        if not game.game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move_left()
                if event.key == pygame.K_RIGHT:
                    game.move_right()
                if event.key == pygame.K_DOWN:
                    game.move_down()
                    game.update_score(0, 1)
                if event.key == pygame.K_UP:
                    game.rotate()
        # Resets the game
        elif game.waiting_for_restart and event.type == pygame.KEYDOWN:
            game.game_over = False
            game.waiting_for_restart = False
            game.reset()

        # Allows blocks to move down on their own
        if event.type == GAME_UPDATE and not game.game_over:
            game.move_down()
            game.update_score(0, 1)

    # Verifies game isn't lost yet
    if not game.game_over:
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
    
        # Checks if the down key is held down and if enough time has passed since the last move
        if keys[pygame.K_DOWN]:
            if current_time - last_move_down_time > move_down_delay:
                game.move_down()
                last_move_down_time = current_time
                game.update_score(0, 1)
    
    # Drawing
    score_value_surface = title_font.render(str(game.score), True, Colours.white_purple)

    screen.fill(purple_background)
    screen.blit(score_surface, (365, 20, 50, 50))
    pygame.draw.rect(screen, Colours.purple_empty_cell, score_rect, 0, 10)
    screen.blit(score_value_surface, score_value_surface.get_rect(centerx = score_rect.centerx, centery = score_rect.centery))
    screen.blit(next_surface, (375, 180, 50, 50))
    pygame.draw.rect(screen, Colours.purple_empty_cell, next_rect, 0, 10)
    
    # Verifies that game is lost
    if game.game_over:
        # Makes sure to play game over sound only once upon losing the game
        if not game.game_over_sound_played:
            game_over_sound.play()
            game.game_over_sound_played = True
        screen.blit(game_over_surface, (320, 450, 50, 50))
        game.waiting_for_restart = True

    game.draw(screen)

    pygame.display.update()
    clock.tick(60)