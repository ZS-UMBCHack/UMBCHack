import pygame, graphics, math, ast
from graphics import Box, BoxText, Text

NA = 0

SWIDTH = 1000
SHEIGHT = 700

LINEWIDTH = 6
ARROWLENGTH = 30

ROWSPACING = 25

cx = SWIDTH / 2
cy = SHEIGHT / 2

yi = 20


def main():
    with open('assets/examples.txt') as f:
        example_data = f.readlines()
    examples = create_file_list(example_data)
    print("Possible word options:")
    print_list(examples)
    word_of_interest = "'" + input("Input a word of interest: ") + "'"
    
    tree = create_tree_file(example_data, word_of_interest)
    tree = ast.literal_eval(tree)
        
    """
    tree = [[{"Language":"English","Word":"'God be with you!'"},{"Language":"English","Word":"'good'"},
            {"Language":"English","Word":"'good morning'"}],
           [{"Language":"","Word":"'goodbye'"},{"Language":"","Word":"'goodbye'"},
            {"Language":"","Word":"'goodbye'"}]]
    """
    
    pygame.init()

    screen = def_screen(SWIDTH, SHEIGHT)
    clock = pygame.time.Clock()
    running = True
    screen_dragging = False
    obj = []

    fontr = pygame.font.Font("assets/OpenDyslexic3-Regular.ttf", 20)
    fontb = pygame.font.Font("assets/OpenDyslexic3-Bold.ttf", 20)
    view_pos = 0, 0

    y = yi
    y, words = create_word(word_of_interest, fontr, fontb, yi)
    y += 2 * ROWSPACING
    y, branches = create_tree(tree, y, fontr, fontb)
    
    obj += branches
    obj += words

    obj += branches
    obj += words

    prev_mouse_pos = 0, 0

    while running:
        # main loop
        clock.tick(120)
        screen.fill(graphics.black)

        for el in obj:
            el.render(screen, view_pos)

        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                screen_dragging = True
                prev_mouse_pos = event.pos

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                screen_dragging = False

            elif event.type == pygame.MOUSEMOTION and screen_dragging:
                view_pos = view_pos[0] + prev_mouse_pos[0] - event.pos[0], \
                           view_pos[1] + prev_mouse_pos[1] - event.pos[1]
                prev_mouse_pos = event.pos

        pygame.display.flip()
        
def print_list(array):
    for el in array:
        print(el)

def create_file_list(file):
    array = []
    append = False
    for line in file:
        word = ""
        for char in line:
            if char == "/":
                break
            elif char != "-" and (char != '"'):
                word += char
                append = True
            elif char == "-":
                break
        if append:
            array.append(word)
            append = False
    return array

def create_tree_file(file, word):
    add_char = False
    search = False
    tree = ""
    for line in file:
        if search:
            if "/" in line:
                for char in line:
                    if char != "/":
                        tree += char
            else:
                break
        elif word in line:
            search = True
            for char in line:
                if add_char == True:
                    tree += char
                elif char == "-":
                    add_char = True
    return tree
            

def create_word(word, font_text, font_title, yi):
    words = []
    # create object "Word:"
    word_txt = Text("Word:", font_title, center_x=cx, y=yi)
    words.append(word_txt)
    # create object for the chosen word.
    y = yi + word_txt.rect.height + ROWSPACING * (3 / 4)
    word = BoxText(word, font_text, center_x=cx, y=y)
    words.append(word)

    yf = y + word.box.rect.height

    return yf, words


def create_tree(tree, starting_y, font_text, font_title):
    """
    The tree should be of the form
    [[{"Language": "Latin", "Word": "'sonus'"}, {"Language": "", "Word": ""}],
     [{"Language": "Anglo-Norman French", "Word": "'soun/suner'"}, {"Language": "", "Word": ""}],
     [{"Language": "Middle English", "Word": "'soun'"},{"Language": "English", "Word": "'-d'"}],
     [{"Language": "", "Word": "'sound'"}, {"Language": "", "Word": "'sound'"}]]
    with "" representing empty space. Location of empty and non-empty space and the same dictionary (combined branches)
    indicate the tree branches. The list goes from top to bottom. The last word should not have language written down.
    Put repeating elements next to one another, in the columns where they step from. Please put the "Word"s in quotes for clarity.
    """
    # [[language y], [word y]]
    columns = len(tree[0])
    col_spacing = SWIDTH / (columns + 1)
    prevcols = None
    y_larrow = 0
    row = 0
    obj = []
    overlap = 2

    # create object "Origin Tree:"
    y_tot = starting_y
    origin_txt = Text("Origin Tree:", font_title, center_x=cx, y=y_tot)
    obj.append(origin_txt)

    y_tot += origin_txt.rect.height + ROWSPACING - (ARROWLENGTH + 2 * ROWSPACING)

    for row in tree:
        y_vals = [[0], [0], [0]]
        heights = [[0], [0], [0]]

        y_larrow = y_tot + ROWSPACING

        y_tot += ARROWLENGTH + 2 * ROWSPACING

        elements = []
        count = 1
        prev_el = None
        for col in range(len(row)):
            if prev_el is not None and row[col]['Word'] == prev_el['Word'] and row[col]['Language'] == prev_el['Language'] and not (row[col]['Word'] == "" and row[col]['Word'] == ""):
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
            y_hline = y_larrow
            for el in elements:
                el_count = el["Count"]
                if el_count > 1:
                    x_hline = (elements.index(el) + 1) * col_spacing - LINEWIDTH / 2
                    len_hline = col_spacing * (el_count - 1)
                    hline = Box(x=x_hline, y=y_hline, width=len_hline, height=LINEWIDTH)
                    obj.append(hline)

        columns = len(elements)
        col_spacing = SWIDTH / (columns + 1)

        for el in elements:
            y_lang = y_word = y_tot

            if el["Language"] != "":
                lang = BoxText(el["Language"], font_text, center_x=0, y=y_lang)

                y_cline = y_lang + lang.box.rect.height - overlap
                y_word = y_lang + lang.box.rect.height + ROWSPACING

                y_vals[0].append(y_lang)
                heights[0].append(lang.box.rect.height)

            if el["Word"] != "":
                word = BoxText(el["Word"], font_text, center_x=0, y=y_word)

                y_vals[1].append(y_word)
                heights[1].append(word.box.rect.height)

            if el["Language"] != "" and el["Word"] != "":
                len_cline = abs(word.box.rect.centery - lang.box.rect.centery - lang.box.rect.height + overlap * 2)
                cline = Box(center_x=0, y=y_cline, width=LINEWIDTH, height=len_cline)

                y_vals[2].append(y_cline)
                heights[2].append(cline.rect.height)

        y_lang = max(y_vals[0])
        y_word = max(y_vals[1] + y_vals[0])
        y_cline = max(y_vals[2])
        y_tot += max(heights[0]) + max(heights[1]) + max(heights[2]) - 2 * overlap

        x_col = 0
        for el in elements:
            x_col += col_spacing
            if el["Language"] != "":
                lang = BoxText(el["Language"], font_text, center_x=x_col, y=y_lang)
                obj.append(lang)

            if el["Word"] != "":
                word = BoxText(el["Word"], font_text, center_x=x_col, y=y_word)
                obj.append(word)

            if el["Language"] != "" and el["Word"] != "":
                cline = Box(center_x=x_col, y=y_cline, width=LINEWIDTH, height=len_cline)
                obj.append(cline)
            

        if prevcols != None:
            x_col = 0
            prevel = 0
            for el in row:
                x_col += col_spacing
                if prevel != el:
                    row_i = tree.index(row)
                    el_i = row.index(el)
                    row_up = tree[row_i - 1]
                    el_up = row_up[el_i]
                
                    if (el["Word"] != "" or el["Language"] != "") and (el_up["Word"] != "" or el_up["Language"] != ""):
                        larrow = Box(center_x=x_col, y=y_larrow, width=LINEWIDTH, height=ARROWLENGTH)
                        obj.append(larrow)
                prevel = el

        prevcols = columns

    return y_tot, obj

def drawTriangle(window, center, radius, width, color, rotation):
        dx = dy = 0

        pointlist = []

        for i in range(2):
            
            pointlist.append((radius+center[0]+dx, dy+center[1]))

            # Rotate the corner by 60 degrees
            dy += math.sin(math.pi / 3)
            dx += math.cos(math.pi / 3)
            
        return pygame.draw.polygon(window, color, pointlist, width)

def branch_space(branches):
    return SWIDTH / (branches + 1)


def def_screen(width, height):
    return pygame.display.set_mode((width, height))


if __name__ == '__main__':
    main()
