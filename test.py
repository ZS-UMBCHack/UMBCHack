import pygame
import cairo
import math
import numpy

red = (255, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)

NA = 0

SWIDTH = 1000
SHEIGHT = 500

LINEWIDTH = 3

spacing = 25

cx = SWIDTH / 2
cy = SHEIGHT / 2


def main():
    pygame.init()
    running = True

    font = pygame.font.Font("OpenDyslexic3-Regular.ttf", 20)

    view_pos = 0, 0
    y = spacing
    word = Text('Word:', font, center_x=cx, y=y)

    y += spacing + word.rect.height
    inword = TextBox('Word', font, center_x=cx, y=y)

    y += 2 * spacing + inword.rect.height
    origin_tree = Text('Origin Tree:', font, center_x=cx, y=y)

    while running:
        # main loop
        screen = def_screen(SWIDTH, SHEIGHT)
        clock = pygame.time.Clock()

        clock.tick(120)
        screen.fill(black)

        # Draw some words!
        word.render(screen, view_pos)
        inword.render(screen, view_pos)
        origin_tree.render(screen, view_pos)

        y += spacing + origin_tree.rect.height
        b_space = branch_space(3)
        x = b_space
        orlatin = draw_col_box_text(screen, x, y, "Latin", font)

        x += b_space
        orgermanic = draw_col_box_text(screen, x, y, "Dutch", font)

        x += b_space
        orgerman = draw_col_box_text(screen, x, y, "German", font)

        x = cx
        y += 1.25 * spacing + max(obj_space(orlatin), obj_space(orgermanic), obj_space(orgerman))
        length = 2 * b_space
        branch_line_1 = draw_col_box(screen, x, y, length, LINEWIDTH)

        pygame.display.flip()

        # running = check_for_quit(button)


class TextBox:
    def __init__(self, text: str, font: pygame.font.Font, border=0.5, bcolor=white, tcolor=black, **kwargs):
        self._color = bcolor

        self.rect = pygame.Rect(0, 0, 0, 0)
        self.text: Text = Text(text, font, tcolor, x=0, y=0)

        self.rect.width = self.text.rect.width + border * 2
        self.rect.height = self.text.rect.height + border * 2

        if 'x' in kwargs.keys():
            self.rect.x = kwargs['x']
        if 'y' in kwargs.keys():
            self.rect.y = kwargs['y']
        if 'center_x' in kwargs.keys():
            self.rect.centerx = kwargs['center_x']
        if 'center_y' in kwargs.keys():
            self.rect.centery = kwargs['center_y']

        self.text.rect.center = self.rect.center

    def render(self, screen: pygame.Surface, view_pos):
        round_rect(screen, self.rect, self._color)
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
        screen.blit(self._surface, self.rect.topleft + view_pos)


def branch_space(branches):
    return SWIDTH / (branches + 1)


def obj_space(obj):
    return obj[1] / 2


def obj_hspace(obj):
    return obj[0] / 2


def draw_text(surface, x, y, text, font, color=white):
    T = def_text(text, font, color)
    cx, cy = get_center(x, y, T.get_width(), T.get_height())
    render_text(surface, T, cx, cy)
    twidth = T.get_width()
    theight = T.get_height()

    return twidth, theight, T


def draw_ctext(surface, cx, cy, text, font, color=white):
    T = def_text(text, font, color)
    render_text(surface, T, -1000, -1000)
    twidth = T.get_width()
    theight = T.get_height()

    render_text(surface, T, cx, cy)

    return twidth, theight, T


def draw_col_text(surface, cx, y, text, font, color=white):
    T = def_text(text, font, color)
    render_text(surface, T, -1000, -1000)
    twidth = T.get_width()
    theight = T.get_height()
    NA = 0

    NA, cy = get_center(NA, y, NA, T.get_height())

    render_text(surface, T, cx, cy)

    return twidth, theight, T


def draw_box_text(surface, x, y, text, font, border=0.5, bcolor=white, tcolor=black):
    """
    Border: 0 <= border <= 1+, where 0 is no border, 1 is border same height as text.
    """
    T = def_text(text, font, tcolor)
    render_text(surface, T, -1000, -1000)
    twidth = T.get_width()
    theight = T.get_height()
    bwidth = twidth + theight * border
    bheight = theight + theight * border / 8

    B = pygame.Rect(x, y, bwidth, bheight)
    round_rect(surface, B, bcolor)

    render_text(surface, T, cx, cy)

    return bwidth, bheight, T, B


def draw_cbox_text(surface, cx, cy, text, font, border=0.5, bcolor=white, tcolor=black):
    """
    Border: 0 <= border <= 1+, where 0 is no border, 1 is border same height as text.
    """
    T = def_text(text, font, tcolor)
    render_text(surface, T, -1000, -1000)
    twidth = T.get_width()
    theight = T.get_height()
    bwidth = twidth + theight * border
    bheight = theight + theight * border / 8

    bx, by = get_corner(cx, cy, bwidth, bheight)

    B = pygame.Rect(bx, by, bwidth, bheight)
    round_rect(surface, B, bcolor)

    render_text(surface, T, cx, cy)

    return bwidth, bheight, T, B


def draw_col_box_text(surface, cx, y, text, font, border=0.5, bcolor=white, tcolor=black):
    """
    Border: 0 <= border <= 1+, where 0 is no border, 1 is border same height as text.
    """
    T = def_text(text, font, tcolor)
    render_text(surface, T, -1000, -1000)
    twidth = T.get_width()
    theight = T.get_height()
    bwidth = twidth + theight * border
    bheight = theight + theight * border / 8
    NA = 0

    bx, NA = get_corner(cx, NA, bwidth, NA)
    NA, cy = get_center(NA, y, NA, bheight)

    B = pygame.Rect(bx, y, bwidth, bheight)
    round_rect(surface, B, bcolor)

    render_text(surface, T, cx, cy)

    return bwidth, bheight, T, B


def draw_box(surface, x, y, width, height, color=white):
    B = pygame.Rect(x, y, width, height)
    round_rect(surface, B, color)

    return width, height, NA, B


def draw_cbox(surface, cx, cy, width, height, color=white):
    bx, by = get_corner(cx, cy, width, height)

    B = pygame.Rect(bx, by, width, height)
    round_rect(surface, B, color)

    return width, height, NA, B


def draw_col_box(surface, cx, y, width, height, color=white):
    NA = 0

    bx, NA = get_corner(cx, NA, width, NA)
    NA, cy = get_center(NA, y, NA, height)

    B = pygame.Rect(bx, y, width, height)
    round_rect(surface, B, color)

    return width, height, NA, B


def get_corner(cx, cy, width, height):
    return (cx - width // 2, cy - height // 2)


def get_center(x, y, width, height):
    return (x + width // 2, y + height // 2)


def move_button(button, text, dx=1, dy=0):
    return button.move(dx, dy)
    # text = text.move(dx, dy)


def render_text(surface, text, cx, cy):
    return surface.blit(text, (cx - text.get_width() // 2, cy - text.get_height() // 1.7))


def def_text(text, font, color):
    return font.render(text, True, color)


def check_for_quit(button):
    boolean = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            boolean = False
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # left click
            if button.collidepoint(pygame.mouse.get_pos()):
                print("click!")
    return boolean


def def_screen(width, height):
    return pygame.display.set_mode((width, height))


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


if __name__ == '__main__':
    main()
