import pygame

red = (255, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)

NA = 0

SWIDTH = 1000
SHEIGHT = 700

LINEWIDTH = 6

ROWSPACING = 25

cx = SWIDTH / 2
cy = SHEIGHT / 2


def main():
    pygame.init()
    running = True

    font = pygame.font.Font("OpenDyslexic3-Regular.ttf", 15)

    view_pos = 0, 0
    y = ROWSPACING
    word = Text('Word:', font, center_x=cx, y=y)

    y += ROWSPACING + word.rect.height
    inword = BoxText('Word', font, center_x=cx, y=y)

    y += 2 * ROWSPACING + inword.get_height()
    origin_tree = Text('Origin Tree:', font, center_x=cx, y=y)

    # old
    y += ROWSPACING + origin_tree.rect.height
    b_space = branch_space(3)
    x = b_space
    orlatin = BoxText('Latin', font, center_x=x, y=y)

    x += b_space
    orgermanic = BoxText('Dutch', font, center_x=x, y=y)

    x += b_space
    orgerman = BoxText('German', font, center_x=x, y=y)

    x = cx
    y += ROWSPACING + max(orlatin.get_height(), orgermanic.get_height(), orgerman.get_height())
    length = 2*b_space
    branch_line_1 = Box(center_x=x, y=y, width=length, height=LINEWIDTH)
    
    obj = tree([[{"Language": "Latin", "Word": "sonus"}, {"Language": "", "Word": ""}],
                [{"Language": "Anglo-Norman French", "Word": "soun/suner"}, {"Language": "", "Word": ""}],
                [{"Language": "Middle English", "Word": "soun"},{"Language": "English", "Word": "-d"}],
                [{"Language": "", "Word": "sound"}, {"Language": "", "Word": "sound"}]], 20, font)

    while running:
        # main loop
        screen = def_screen(SWIDTH, SHEIGHT)
        clock = pygame.time.Clock()

        clock.tick(120)
        screen.fill(black)

        # Draw some words!
        """
        word.render(screen, view_pos)
        inword.render(screen, view_pos)
        origin_tree.render(screen, view_pos)
        orlatin.render(screen, view_pos)
        orgermanic.render(screen, view_pos)
        orgerman.render(screen, view_pos)
        branch_line_1.render(screen, view_pos)
        """
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
    def __init__(self, text: str, font: pygame.font.Font, border=15, bcolor=white, tcolor=black, **kwargs):
        self._color = bcolor

        self.text: Text = Text(text, font, tcolor, x=0, y=0)

        kwargs['width'] = self.text.rect.width + border * 2
        kwargs['height'] = self.text.rect.height + border *.5
        self.box = Box(bcolor, kwargs)

        self.text.rect.center = self.box.rect.move(0, -self.text.rect.height*.07).center

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
    The tree should be of the form [[{"Language": "Latin", "Word": "sonus"}, {"Language": "", "Word": ""}],
    [{"Language": "Anglo-Norman French", "Word": "soun/suner"}, {"Language": "", "Word": ""}],
    [{"Language": "Middle English", "Word": "soun"},{"English", "Word": "-d"}],
    [{"Language": "", "Word": "sound"}, {"Language": "", "Word": "sound"}]]  with
    "" representing empty space. Location of empty and non-empty space and the same dictionary indicate
    the tree branches. The list goes from top to bottom. The last word should not have language written down.
    """
    # [[language y], [word y]]
    columns = len(tree[0])
    print(columns)
    col_spacing = SWIDTH/(columns + 1)
    y_tot = y_lang = starting_y
    row = 0
    obj = []
    overlap = 2
    for row in tree:
        x_col = 0
        y_vals = [[0],[0],[0]]
        heights = [[0],[0],[0]]
        for col in row:
            y_lang = y_word = y_tot
            
            if col["Language"] != "":
                lang = BoxText(col["Language"], font, center_x=x_col, y=y_lang)
                
                y_cline = y_lang + lang.get_height() - overlap
                y_word = y_cline + ROWSPACING
                
                y_vals[0].append(y_lang)
                heights.append(lang.box.rect.height)
            
            if col["Word"] != "":
                word = BoxText(col["Word"], font, center_x=x_col, y=y_word)
                
                y_vals[1].append(y_word)
                heights.append(word.box.rect.height)
                
            if col["Language"] != "" and col["Word"] != "":
                len_cline = word.box.rect.centery - lang.box.rect.centery - lang.box.rect.height + overlap*2
                cline = Box(center_x=x_col, y=y_cline, width=LINEWIDTH, height=len_cline)
                
                y_vals[2].append(y_cline)
                heights.append(cline.rect.height)
                
        y_lang = max(y_vals[0])
        y_word = max(y_vals[1])
        y_cline = max(y_vals[2])
        y_tot += max(heights[0]) + max(heights[1]) + max(heights[2]) + 2*ROWSPACING
                
        for col in row:
            x_col += col_spacing
            if col["Language"] != "":
                lang = BoxText(col["Language"], font, center_x=x_col, y=y_lang)
                obj.append(lang)
            
            if col["Word"] != "":
                word = BoxText(col["Word"], font, center_x=x_col, y=y_word)
                obj.append(word)
                
            if col["Language"] != "" and col["Word"] != "":
                cline = Box(center_x=x_col, y=y_cline, width=LINEWIDTH, height=len_cline)
                obj.append(cline)
            
    return obj

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
