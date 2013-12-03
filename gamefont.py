"""
Author: Mike McMahon

"""
import pygame

from gamecolors import BLACK


def init(size=15):
    pygame.font.init()
    font_renderer = pygame.font.SysFont("monospace", size)
    font_renderer.set_bold(True)

    return "monospace", font_renderer


def create_label(font_renderer, label, color=BLACK):
    return font_renderer.render(label, 1, color)


def blit_font(label, surface, *pos):
    return surface.blit(label, pos)