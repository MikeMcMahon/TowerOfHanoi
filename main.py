"""
Author: Mike McMahon

"""

import sys
from decimal import Decimal
import math

import pygame
from pygame.locals import *

import gamefont
from gamecolors import *
from sprite import GameButton, TowerDisk


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

tower_platform = pygame.sprite.Sprite()
tower_platform.image = pygame.Surface([700, 40])
tower_platform.rect = tower_platform.image.get_rect()
tower_platform.rect.x = 50
tower_platform.rect.y = 500
fill_gradient(tower_platform.image, GOLDENROD, DARK_GOLDENROD, None, False, False)

tower_size = tower_width, tower_height = [20, 350]
tower_y = tower_platform.rect.y - tower_height

tower_a = pygame.sprite.Sprite()
tower_a.image = pygame.Surface(tower_size)
tower_a.rect = tower_a.image.get_rect()
tower_a.rect.x, tower_a.rect.y = tower_platform.rect.x + 116, tower_y
fill_gradient(tower_a.image, GOLDENROD, DARK_GOLDENROD, None, False)

tower_b = pygame.sprite.Sprite()
tower_b.image = pygame.Surface(tower_size)
tower_b.rect = tower_b.image.get_rect()
tower_b.rect.x, tower_b.rect.y = tower_a.rect.x + 233, tower_y
fill_gradient(tower_b.image, GOLDENROD, DARK_GOLDENROD, None, False)

tower_c = pygame.sprite.Sprite()
tower_c.image = pygame.Surface(tower_size)
tower_c.rect = tower_c.image.get_rect()
tower_c.rect.x, tower_c.rect.y = tower_b.rect.x + 233, tower_y
fill_gradient(tower_c.image, GOLDENROD, DARK_GOLDENROD, None, False)

rod_sprites = pygame.sprite.OrderedUpdates(
    tower_a,
    tower_b,
    tower_c,
    tower_platform
)

disk_sprites = pygame.sprite.OrderedUpdates()


def add_disk():
    if len(disk_sprites) == 0:
        mod = 1
    else:
        mod = math.log(len(disk_sprites) + 1) / len(disk_sprites)
    disk = TowerDisk((200 * mod))
    disk.set_pos(
        (tower_a.rect.x + (tower_a.rect.width / 2)) - (disk.get_rect().width / 2),
        (tower_a.rect.y + tower_a.rect.height - disk.get_rect().height) - ((disk.get_rect().height * len(disk_sprites)))
    )
    disk_sprites.add(
        disk
    )
    return add_disk
add_disk_button.on_clicked(add_disk)


def main():
    interval = Decimal(1000) / Decimal(32)
    current_time = pygame.time.get_ticks()
    next_update = current_time

    solve_button.set_pos(5, 5)
    add_disk_button.set_pos(solve_button.get_pos()[0] + solve_button.get_width() + 5, 5)
    remove_disk_button.set_pos(add_disk_button.get_pos()[0] + add_disk_button.get_width() + 5, 5)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                button_sprites.update(pygame.mouse.get_pos(), pygame.mouse.get_pressed())

        # Input in reaaal time
        button_sprites.update(pygame.mouse.get_pos(), (0, 0, 0, 0))

        # Update logic goes here
        if current_time >= next_update:

            disk_sprites.update()
            next_update += interval

        # Show me the money - rendering
        fill_gradient(screen, WHITE, LIGHT_BLUE, None, True, False)
        rod_sprites.draw(screen)
        disk_sprites.draw(screen)
        button_sprites.draw(screen)
        current_time = pygame.time.get_ticks()
        pygame.display.flip()


pygame.init()
main()