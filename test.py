import pygame

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
    inword = BoxText('Word', font, center_x=cx, y=y)

    y += 2 * spacing + inword.get_height()
    origin_tree = Text('Origin Tree:', font, center_x=cx, y=y)

    # old
    y += spacing + origin_tree.rect.height
    b_space = branch_space(3)
    x = b_space
    orlatin = BoxText('Latin', font, center_x=x, y=y)

    x += b_space
    orgermanic = BoxText('Dutch', font, center_x=x, y=y)

    x += b_space
    orgerman = BoxText('German', font, center_x=x, y=y)

    x = cx
    y += 1.25 * spacing + max(orlatin.get_height(), orgermanic.get_height(), orgerman.get_height())
    length = 2 * b_space
    branch_line_1 = Box(center_x=x, y=y, width=length, height=LINEWIDTH)

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
        orlatin.render(screen, view_pos)
        orgermanic.render(screen, view_pos)
        orgerman.render(screen, view_pos)
        branch_line_1.render(screen, view_pos)

        pygame.display.flip()

        running = check_for_quit()


class Box:
    def __init__(self, color=white, pass_args=None, **kwargs):
        self._color = color

        if pass_args is None:
            pass_args = kwargs
        else:
            pass_args.update(kwargs)

        self.rect = pygame.Rect(0, 0, 0, 0)
        if 'x' in pass_args.keys():
            self.rect.x = pass_args['x']
        if 'y' in pass_args.keys():
            self.rect.y = pass_args['y']
        if 'width' in pass_args.keys():
            self.rect.width = pass_args['width']
        if 'height' in pass_args.keys():
            self.rect.height = pass_args['height']
        if 'center_x' in pass_args.keys():
            self.rect.x = pass_args['center_x'] - self.rect.width / 2
        if 'center_y' in pass_args.keys():
            self.rect.y = pass_args['center_y'] - self.rect.height / 2

    def render(self, screen: pygame.Surface, view_pos):
        round_rect(screen, self.rect.move(view_pos), self._color)


class BoxText:
    def __init__(self, text: str, font: pygame.font.Font, border=0.5, bcolor=white, tcolor=black, **kwargs):
        self._color = bcolor

        self.text: Text = Text(text, font, tcolor, x=0, y=0)

        kwargs['width'] = self.text.rect.width + border * 2
        kwargs['height'] = self.text.rect.height + border * 2
        self.box = Box(bcolor, kwargs)

        self.text.rect.center = self.box.rect.center

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
        screen.blit(self._surface, self.rect.topleft + view_pos)


def branch_space(branches):
    return SWIDTH / (branches + 1)


def check_for_quit():
    boolean = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            boolean = False
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
