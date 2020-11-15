import pygame

red = (255, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)

NA = 0

SWIDTH = 1000
SHEIGHT = 700

LINEWIDTH = 6
ARROWLENGTH = 30

ROWSPACING = 25

cx = SWIDTH / 2
cy = SHEIGHT / 2


def main():
    pygame.init()
    running = True

    font = pygame.font.Font("assets/OpenDyslexic3-Regular.ttf", 15)

    view_pos = 0, 0

    obj = tree([[{"Language": "Latin", "Word": "sonus"}, {"Language": "", "Word": ""}],
                [{"Language": "Anglo-Norman French", "Word": "soun/suner"}, {"Language": "", "Word": ""}],
                [{"Language": "Middle English", "Word": "soun"}, {"Language": "English", "Word": "-d"}],
                [{"Language": "", "Word": "sound"}, {"Language": "", "Word": "sound"}]], 20, font)

    while running:
        # main loop
        screen = def_screen(SWIDTH, SHEIGHT)
        clock = pygame.time.Clock()

        clock.tick(120)
        screen.fill(black)

        for el in obj:
            el.render(screen, view_pos)

        pygame.display.flip()

        running = check_for_quit()


class Box:
    def __init__(self, color=white, pass_args=None, **kwargs):
        self._color = color

        if pass_args is None:
            pass_args = kwargs
        else:
            pass_args.update(kwargs)
        self.rect = create_rect(pass_args)

    def render(self, screen: pygame.Surface, view_pos):
        round_rect(screen, self.rect.move(view_pos), self._color)


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
        screen.blit(self._surface, self.rect.topleft + view_pos)


def tree(tree, starting_y, font):
    """
    The tree should be of the form
    [[{"Language": "Latin", "Word": "sonus"}, {"Language": "", "Word": ""}],
     [{"Language": "Anglo-Norman French", "Word": "soun/suner"}, {"Language": "", "Word": ""}],
     [{"Language": "Middle English", "Word": "soun"},{"Language": "English", "Word": "-d"}],
     [{"Language": "", "Word": "sound"}, {"Language": "", "Word": "sound"}]]
    with "" representing empty space. Location of empty and non-empty space and the same dictionary (combined branches)
    indicate the tree branches. The list goes from top to bottom. The last word should not have language written down.
    Put repeating elements next to one another, in the columns where they step from.
    """
    # [[language y], [word y]]
    columns = len(tree[0])
    col_spacing = SWIDTH / (columns + 1)
    prevcols = None
    y_tot = starting_y - (ARROWLENGTH + 2 * ROWSPACING)
    y_larrow = 0
    row = 0
    obj = []
    overlap = 2
    for row in tree:
        y_vals = [[0], [0], [0]]
        heights = [[0], [0], [0]]
        y_tot += ARROWLENGTH + 2 * ROWSPACING

        elements = []
        count = 1
        prev_el = None
        for col in range(len(row)):
            if prev_el is not None and row[col]['Word'] == prev_el['Word']:
                count += 1
                if col == len(row) - 1:
                    elements.append({"Language": row[col]["Language"], "Word": row[col]["Word"], "Count": count})
            else:
                if prev_el is not None:
                    elements.append({"Language": prev_el["Language"], "Word": prev_el["Word"], "Count": count})
                    if col == len(row) - 1:
                        elements.append({"Language": row[col]["Language"], "Word": row[col]["Word"], "Count": count})
                count = 1

            prev_el = row[col]

        print("elements:", elements)

        if prevcols is not None:
            print("ran1")
            y_hline = y_larrow
            for el in elements:
                el_count = el["Count"]
                print("number of repeats of el", el["Count"])
                if el_count > 1:
                    print("ran2")
                    x_hline = (elements.index(el) + 1) * col_spacing - LINEWIDTH / 2
                    len_hline = col_spacing * (el_count - 1)
                    hline = Box(x=x_hline, y=y_hline, width=len_hline, height=LINEWIDTH)
                    obj.append(hline)

        columns = len(elements)
        print("number of columns:", columns)
        col_spacing = SWIDTH / (columns + 1)

        for el in elements:
            y_lang = y_word = y_tot

            if el["Language"] != "":
                lang = BoxText(el["Language"], font, center_x=0, y=y_lang)

                y_cline = y_lang + lang.box.rect.height - overlap
                y_word = y_lang + lang.box.rect.height + ROWSPACING

                y_vals[0].append(y_lang)
                heights[0].append(lang.box.rect.height)

            if el["Word"] != "":
                word = BoxText(el["Word"], font, center_x=0, y=y_word)

                y_vals[1].append(y_word)
                heights[1].append(word.box.rect.height)

                prevcols = 0

            if el["Language"] != "" and el["Word"] != "":
                len_cline = abs(word.box.rect.centery - lang.box.rect.centery - lang.box.rect.height + overlap * 2)
                cline = Box(center_x=0, y=y_cline, width=LINEWIDTH, height=len_cline)

                y_vals[2].append(y_cline)
                heights[2].append(cline.rect.height)

        print("el of elements:", el, "\ny_lang:", y_lang, "y_word:", y_word, "y_cline:", y_cline, "\n")

        y_lang = max(y_vals[0])
        y_word = max(y_vals[1] + y_vals[0])
        y_cline = max(y_vals[2])
        y_tot += max(heights[0]) + max(heights[1]) + max(heights[2]) - 2 * overlap

        print("row:", row, "\ny_lang:", y_lang, "y_word:", y_word, "y_cline:", y_cline, "\n")

        x_col = 0
        for el in elements:
            x_col += col_spacing
            if el["Language"] != "":
                lang = BoxText(el["Language"], font, center_x=x_col, y=y_lang)
                obj.append(lang)

            if el["Word"] != "":
                word = BoxText(el["Word"], font, center_x=x_col, y=y_word)
                obj.append(word)

            if el["Language"] != "" and el["Word"] != "":
                cline = Box(center_x=x_col, y=y_cline, width=LINEWIDTH, height=len_cline)
                obj.append(cline)

                y_larrow = y_tot + ROWSPACING
                larrow = Box(center_x=x_col, y=y_larrow, width=LINEWIDTH, height=ARROWLENGTH)
                obj.append(larrow)

        prevcols = columns

    return obj


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
