"""
Author: Mike McMahon

"""
import os
from random import randint
from pygame.locals import *
from pygame.sprite import DirtySprite
from gamecolors import *
from gamefont import create_label
from physics import collision_detection


class GameBase(DirtySprite):
    def __init__(self):
        DirtySprite.__init__(self)
        self._x, self._y, self._width, self._height = 0, 0, 0, 0
        self.rect = Rect(self._x, self._y, self._width, self._height)
        self.image = None
        self.pos = self._x, self._y

    def get_pos(self):
        return self.pos

    def set_pos(self, *point):
        self.pos = self._x, self._y = point
        self.set_rect(self._x, self._y, self._width, self._height)

    def get_rect(self):
        return self.rect

    def set_rect(self, x, y, width, height):
        self._x, self._y, self._width, self._height = x, y, width, height
        self.rect = Rect(self._x, self._y, self._width, self._height)


class TowerDisk(GameBase):
    def __init__(self, width=200, order=0):
        GameBase.__init__(self)
        self._fill_color = (randint(75, 255), randint(75, 255), randint(75, 255))
        self._fill_to_color = tuple(x - 75 for x in self._fill_color)
        self._width = width
        self._height = 25
        self.dirty = 1
        self.disk_order = order
        self._paint()

    def _paint(self):
        if self.image is None or self.dirty == 1:
            self.image = pygame.Surface([self._width, self._height])
            fill_gradient(self.image, self._fill_color, self._fill_to_color)
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = self._x, self._y

    def update(self, *args):
        self._paint()


class GameButton(GameBase):
    def __init__(self, font_renderer, label="", icon_path=""):
        GameBase.__init__(self)
        self.label = None
        self.icon_path = None
        self._show_icon = False
        self.pos = self._x, self._y = 0, 0
        self.font_renderer = font_renderer
        self._font_surface = None
        self._icon_surface = None
        self._show_label = True
        self.label_width, self.label_height = (0, 0)
        self._padding = 2

        self._label_dirty = False
        self._icon_dirty = False
        self.set_label(label)
        self.set_icon(icon_path)
        self._func = None
        self._fill_forward = True
        self._is_mouse_down = True
        self._paint()

    def set_label(self, label):
        self._label_dirty = True
        self.label = label
        self.label_width, self.label_height = self.font_renderer.size(self.label)

    def set_icon(self, icon):
        self._icon_dirty = True
        self.icon_path = icon
        # TODO - this is a terrible way to check if we should show the image
        self._show_icon = True if len(self.icon_path) > 0 else False

    def get_width(self):
        """
        Gets the width of this object (including the icon width if an icon is specified
        @return:
        """
        icon_width = (self.label_height + self._padding) if self._show_icon else 0
        return self._padding + icon_width + self.label_width + self._padding

    def get_height(self):
        """
        Gets the height of this object
        @return:
        """
        return self.label_height + self._padding

    def show_label(self):
        self._show_label = True

    def hide_label(self):
        self._show_label = False

    def _paint(self):
        if self._show_label and self._label_dirty:
            self._font_surface = create_label(self.font_renderer, self.label, BLACK)

        if self._show_icon and self._icon_dirty:
            image_path = os.path.join("assets", self.icon_path)
            image_width, image_height = \
                (self.label_height - (self._padding * 2)), \
                (self.label_height - (self._padding * 2))
            self._icon_surface = pygame.image.load(image_path)
            self._icon_surface = pygame.transform.smoothscale(self._icon_surface, (image_width, image_height))
        else:
            image_width = 0

        if self._label_dirty or self._icon_dirty:
            display_width = self.get_width()
            display_height = self.get_height()
            display_surface = pygame.Surface(
                (display_width,
                 display_height)
            )
            display_surface.fill(BLACK)
            fill_gradient(
                display_surface,
                WHITE,
                GREY,
                rect=Rect(
                    1,
                    1,
                    display_width - 3,
                    display_height - 2),
                forward=self._fill_forward
            )

            if self._show_icon:
                display_surface.blit(self._icon_surface, (self._padding, self._padding))
            display_surface.blit(self._font_surface,
                                 (self._padding + image_width, self._padding)) if self._show_label else None

            self.image = display_surface
            self.set_rect(self._x, self._y, self.image.get_width(), self.image.get_height())

    def update(self, *args):
        """
        On update checks if we're being moused over, or if we're being clicked
        @param args:
            unpacked it should be the following tuples
            (mouse_x,mouse_y)
            (mouse buttons pressed)
        @return:
        """
        if len(args) > 0:
            if collision_detection(self.get_rect(), args[0]):
                self._fill_forward = False
                if args[1][0] == 1 and not self._func is None and not self._is_mouse_down:
                    self._is_mouse_down = True
                    self._func()
                elif args[1][0] == 0:
                    self._is_mouse_down = False
            else:
                self._is_mouse_down = False
                self._fill_forward = True

        self._paint()

    def on_clicked(self, func):
        self._func = func
