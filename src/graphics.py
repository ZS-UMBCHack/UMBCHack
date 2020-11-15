# -*- coding: utf-8 -*-
import pygame

black = (0, 0, 0)
white = (255, 255, 255)

class Box:
    def __init__(self, color=white, pass_args=None, **kwargs):
        self._color = color

        if pass_args is None:
            pass_args = kwargs
        else:
            pass_args.update(kwargs)
        self.rect = create_rect(pass_args)

    def render(self, screen: pygame.Surface, view_pos):
        round_rect(screen, self.rect.move(-view_pos[0], -view_pos[1]), self._color)


class BoxText:
    def __init__(self, text: str, font: pygame.font.Font, border=15, bcolor=white, tcolor=black, **kwargs):
        self._color = bcolor

        self.text: Text = Text(text, font, tcolor, x=0, y=0)

        kwargs['width'] = self.text.rect.width + border * 2
        kwargs['height'] = self.text.rect.height + border * .5
        self.box = Box(bcolor, kwargs)

        self.text.rect.center = self.box.rect.move(0, -self.text.rect.height * .07).center

    def get_height(self) -> int:
        return self.box.rect.height

    def render(self, screen: pygame.Surface, view_pos):
        self.box.render(screen, view_pos)
        self.text.render(screen, view_pos)


class Text:
    def __init__(self, text: str, font: pygame.font.Font, color=white, **kwargs):
        self._surface: pygame.Surface = font.render(text, True, color)
        self.rect = pygame.Rect(0, 0, self._surface.get_width(), self._surface.get_height())

        if 'x' in kwargs.keys():
            self.rect.x = kwargs['x']
        if 'y' in kwargs.keys():
            self.rect.y = kwargs['y']
        if 'center_x' in kwargs.keys():
            self.rect.centerx = kwargs['center_x']
        if 'center_y' in kwargs.keys():
            self.rect.centery = kwargs['center_y']

    def render(self, screen: pygame.Surface, view_pos):
        x, y = self.rect.topleft
        screen.blit(self._surface, (x - view_pos[0], y - view_pos[1]))


def create_rect(pass_args):
    rect = pygame.Rect(0, 0, 0, 0)
    if 'x' in pass_args.keys():
        rect.x = pass_args['x']
    if 'y' in pass_args.keys():
        rect.y = pass_args['y']
    if 'width' in pass_args.keys():
        rect.width = pass_args['width']
    if 'height' in pass_args.keys():
        rect.height = pass_args['height']
    if 'center_x' in pass_args.keys():
        rect.x = pass_args['center_x'] - rect.width / 2
    if 'center_y' in pass_args.keys():
        rect.y = pass_args['center_y'] - rect.height / 2
    return rect


def round_rect(surface, rect, color, radius=0.4):
    """
    surface : destination
    rect    : rectangle
    color   : rgb or rgba
    radius  : 0 <= radius <= 1
    """

    rect = pygame.Rect(rect)
    color = pygame.Color(*color)
    alpha = color.a
    color.a = 0
    pos = rect.topleft
    rect.topleft = 0, 0
    rectangle = pygame.Surface(rect.size, pygame.SRCALPHA)

    circle = pygame.Surface([min(rect.size) * 3] * 2, pygame.SRCALPHA)
    pygame.draw.ellipse(circle, (0, 0, 0), circle.get_rect(), 0)
    circle = pygame.transform.smoothscale(circle, [int(min(rect.size) * radius)] * 2)

    radius = rectangle.blit(circle, (0, 0))
    radius.bottomright = rect.bottomright
    rectangle.blit(circle, radius)
    radius.topright = rect.topright
    rectangle.blit(circle, radius)
    radius.bottomleft = rect.bottomleft
    rectangle.blit(circle, radius)

    rectangle.fill((0, 0, 0), rect.inflate(-radius.w, 0))
    rectangle.fill((0, 0, 0), rect.inflate(0, -radius.h))

    rectangle.fill(color, special_flags=pygame.BLEND_RGBA_MAX)
    rectangle.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MIN)

    return surface.blit(rectangle, pos)
