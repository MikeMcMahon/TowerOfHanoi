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
import gamestate
from sprite import GameButton, TowerDisk


window = width, height = 800, 600
screen = pygame.display.set_mode(window)
pygame.display.set_caption("Tower of Hanoi")

default_font, font_renderer = gamefont.init()

solve_button = GameButton(font_renderer, "Solve")
reset_button = GameButton(font_renderer, "Reset")
add_disk_button = GameButton(font_renderer, "Add Disk")
remove_disk_button = GameButton(font_renderer, "Remove Disk")

tower_a_disks = []
tower_b_disks = []
tower_c_disks = []
total_disks = gamefont.create_label(font_renderer, "Total Disks {}  ".format(0))

button_sprites = pygame.sprite.RenderPlain(
    solve_button,
    add_disk_button,
    remove_disk_button,
    reset_button)

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


def reset_total():
    """
    Resets the label and updates it with the proper number of disks
    """
    total_disks.fill((0, 0, 0, 0))
    total_disks.blit(gamefont.create_label(font_renderer, "Total Disks {}".format(len(disk_sprites))), (0, 0))


def remove_disk():
    """
    Removes a disk from the stack
    """
    if len(disk_sprites) == 3 or game_state.is_solving or game_state.is_dirty:
        return remove_disk

    tower_a_disks[len(tower_a_disks)-1].kill()
    tower_a_disks.pop()

    reset_total()
    return remove_disk


def add_disk():
    """
    Adds a disk to the stack
    """
    if len(disk_sprites) == 13 or game_state.is_solving or game_state.is_dirty:
        return

    if len(disk_sprites) == 0:
        mod = 1
    else:
        mod = math.log(len(disk_sprites) + 1) / len(disk_sprites)

    disk = TowerDisk(200 * mod, len(tower_a_disks) + 1)
    disk.set_pos(
        (tower_a.rect.x + (tower_a.rect.width / 2)) - (disk.get_rect().width / 2),
        (tower_a.rect.y + tower_a.rect.height - disk.get_rect().height) - ((disk.get_rect().height * len(disk_sprites)))
    )
    disk_sprites.add(disk)
    tower_a_disks.append(disk)

    reset_total()
    return add_disk


def solve():
    """
    Starts and pauses the auto-solver mode
    """
    game_state.is_solving = ~game_state.is_solving

    if game_state.is_solving:
        solve_button.set_label("Pause")
    else:
        solve_button.set_label("Solve")

    game_state.is_dirty = True

    return solve


def reset():
    """
    Resets the state of the towers
    """
    if not game_state.is_solving:
        game_state.is_solving = False
        game_state.is_dirty = False

        del tower_a_disks[0:len(tower_a_disks)]
        del tower_b_disks[0:len(tower_b_disks)]
        del tower_c_disks[0:len(tower_c_disks)]

        disk_sprites.empty()

        [add_disk() for x in range(3)]

    return reset


def move_disk(tower, dest, direction="r", poles=1):
    """
    Moves the top most disk from the tower to the dest
    @param tower: the starting tower
    @param dest:  the ending tower
    @param direction: the direction (r = right, l = left)
    @param poles: move one pole or two poles at a time

    Returns either the disk and keyframes to move or none and an empty keyframe set
    """
    if len(tower) == 0:
        return None, ()

    disk = tower[-1]

    if disk.key_frames is not None:
        return disk, ()  # can't move a disk in motion

    if direction == "r":
        amount = 233
    elif direction == "l":
        amount = -233

    if poles > 1:
        amount *= 2

    key_frames = (
        (disk.get_rect().x, 100),
        (disk.get_rect().x + amount, 100),
        (disk.get_rect().x + amount, tower_platform.rect.y - ((len(dest) + 1) * disk.get_rect().height))
    )

    tower.remove(disk)
    dest.append(disk)

    disk.key_frames = key_frames

    return disk, key_frames


def disks_in_motion(tower):
    if len(tower) == 0:
        return False

    if tower[-1].key_frames is not None:
        return True


def generate_moves(disks, src, aux, dest, moves):
    if disks == 0:
        return
    else:
        generate_moves(disks - 1, src, dest, aux, moves)
        moves.append("{0}{1}".format(src, dest))
        generate_moves(disks - 1, aux, src, dest, moves)


def get_tower_move(src, dest):
    src_spot, src_tower = get_tower(src)
    dest_spot, dest_tower = get_tower(dest)

    return (src_spot - dest_spot), src_tower, dest_tower


def get_tower(pole):
    if pole == "A":
        return 1, tower_a_disks
    elif pole == "B":
        return 2, tower_b_disks
    elif pole == "C":
        return 3, tower_c_disks

    return None


add_disk_button.on_clicked(add_disk)
remove_disk_button.on_clicked(remove_disk)
solve_button.on_clicked(solve)
reset_button.on_clicked(reset)

game_state = gamestate.GameState()


def main():
    interval = Decimal(1000) / Decimal(32)
    current_time = pygame.time.get_ticks()
    next_update = current_time

    solve_button.set_pos(5, 5)
    add_disk_button.set_pos(solve_button.get_pos()[0] + solve_button.get_width() + 5, 5)
    remove_disk_button.set_pos(add_disk_button.get_pos()[0] + add_disk_button.get_width() + 5, 5)
    reset_button.set_pos(remove_disk_button.get_pos()[0] + remove_disk_button.get_width() + 5, 5)

    [add_disk() for x in range(3)]

    moves = []
    generate_move_list = False
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                button_sprites.update(pygame.mouse.get_pos(), pygame.mouse.get_pressed())

        # Input in reaaal time
        button_sprites.update(pygame.mouse.get_pos(), (0, 0, 0, 0))
        disk_sprites.update({"mousepos": pygame.mouse.get_pos()})

        # Update logic goes here
        if current_time >= next_update:
            if game_state.is_solving \
                    and (len(tower_a_disks) > 0 or len(tower_b_disks) > 0)\
                    and not (
                        disks_in_motion(tower_a_disks) or
                        disks_in_motion(tower_b_disks) or
                        disks_in_motion(tower_c_disks)
                    ):

                if not generate_move_list:
                    generate_moves(len(tower_a_disks), "A", "B", "C", moves)
                    generate_move_list = True

                move = moves[0]
                moves = moves[1:]

                src, dest = move[0], move[1]
                tower_move, tower_src, tower_dest = get_tower_move(src, dest)
                if src < dest:
                    direction = "r"
                    tower_move *= -1
                else:
                    direction = "l"

                move_disk(tower_src, tower_dest, direction, tower_move)

            if game_state.is_solving:
                disk_sprites.update()

            next_update += interval

        # Show me the money - rendering
        fill_gradient(screen, WHITE, LIGHT_BLUE, None, True, False)
        rod_sprites.draw(screen)
        disk_sprites.draw(screen)
        button_sprites.draw(screen)
        current_time = pygame.time.get_ticks()
        gamefont.blit_font(total_disks, screen, (5, solve_button.get_height() + 10))
        pygame.display.flip()


pygame.init()
main()