"""
Author: Mike McMahon

"""

import pygame
import gamefont
import sys
from pygame.locals import *
from gamecolors import *
from sprite import GameButton
from decimal import Decimal

window = width, height = 800, 600
screen = pygame.display.set_mode(window)

default_font, font_renderer = gamefont.init()

solve_button = GameButton(font_renderer, "Solve")
add_disk_button = GameButton(font_renderer, "Add Disk")
remove_disk_button = GameButton(font_renderer, "Remove Disk")

button_sprites = pygame.sprite.RenderPlain(
    solve_button,
    add_disk_button,
    remove_disk_button)

tower_a = pygame.sprite.Sprite()
tower_a.image = pygame.Surface([23, 400])
tower_a.rect = Rect(183, 180, 23, 400)
fill_gradient(tower_a.image, GOLDENROD, DARK_GOLDENROD, None, False)

tower_b = pygame.sprite.Sprite()
tower_b.image = pygame.Surface([23, 400])
tower_b.rect = Rect(tower_a.rect.x + 183, 180, 23, 400)
fill_gradient(tower_b.image, GOLDENROD, DARK_GOLDENROD, None, False)

tower_c = pygame.sprite.Sprite()
tower_c.image = pygame.Surface([23, 400])
tower_c.rect = Rect(tower_b.rect.x + 183, 180, 23, 400)
fill_gradient(tower_c.image, GOLDENROD, DARK_GOLDENROD, None, False)

#tower_platform

rod_sprites = pygame.sprite.RenderPlain(
    tower_a,
    tower_b,
    tower_c
)


def main():
    current_time = pygame.time.get_ticks()
    interval = Decimal(1000) / Decimal(32)
    next_update = pygame.time.get_ticks() + interval

    solve_button.set_pos(5, 5)
    add_disk_button.set_pos(solve_button.get_pos()[0] + solve_button.get_width() + 5, 5)
    remove_disk_button.set_pos(add_disk_button.get_pos()[0] + add_disk_button.get_width() + 5, 5)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()

        # Updates handled here - in real timeee
        button_sprites.update()

        # Rendering logic goes here
        if current_time - next_update >= interval:
            fill_gradient(screen, WHITE, LIGHT_BLUE, None, True, False)

            rod_sprites.draw(screen)
            button_sprites.draw(screen)

            next_update = pygame.time.get_ticks() + interval
        else:
            current_time = pygame.time.get_ticks()
        pygame.display.flip()


pygame.init()
main()