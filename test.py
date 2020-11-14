import pygame
import cairo
import math
import numpy

red = (255, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)

def main():
    pygame.init()
    running = True
    
    font = pygame.font.SysFont("comicsansms", 20)

    while running:
        # main loop
        screen = def_screen(400, 300)
        clock = pygame.time.Clock()
        
        clock.tick(120)
        screen.fill(black)
        
        button, text = draw_button(screen, 0, 30, "Hello, World", font)

        pygame.display.flip()

        running = check_for_quit(button)
 
def draw_button(surface, bx, by, text, font, bcolor=white, tcolor=black):
    T = def_text(text, font, tcolor)
    render_text(surface, T, -1000, -1000)
    twidth = T.get_width()
    theight = T.get_height()
    bwidth = twidth + twidth / 4
    bheight = theight + theight / 4
    
    B = pygame.Rect(bx, by, bwidth, bheight)
    round_rect(surface, B, bcolor)
    cx, cy = get_center(bx, by, bwidth, bheight)
    
    render_text(surface, T, cx, cy)
    
    return B, T
    
def get_center(x, y, width, height):
    return (x + width // 2, y + height // 2)
       
def move_button(button, text, dx=1, dy=0):
    return button.move(dx, dy)
    #text = text.move(dx, dy)

def render_text(surface, text, cx, cy):
    return surface.blit(text, (cx - text.get_width() // 2, cy - text.get_height() // 2))

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
