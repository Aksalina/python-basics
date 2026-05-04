import pygame
import sys
import math
from datetime import datetime

pygame.init()

# экран
WIDTH, HEIGHT = 1200, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS2 Paint")

clock = pygame.time.Clock()

# цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

color = BLACK
tool = "pen"
brush_size = 5

drawing = False
start_pos = None
last_pos = None

# текст
font = pygame.font.SysFont(None, 32)
text_input = ""
text_pos = None
typing = False

# холст
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)

# кнопки размера
brush_buttons = [
    {"rect": pygame.Rect(10, 10, 40, 40), "size": 2},
    {"rect": pygame.Rect(60, 10, 40, 40), "size": 5},
    {"rect": pygame.Rect(110, 10, 40, 40), "size": 10},
]

# UI
def draw_ui():
    for btn in brush_buttons:
        pygame.draw.rect(screen, BLACK, btn["rect"], 2)
        txt = font.render(str(btn["size"]), True, BLACK)
        screen.blit(txt, (btn["rect"].x + 10, btn["rect"].y + 5))

        if brush_size == btn["size"]:
            pygame.draw.rect(screen, RED, btn["rect"], 3)


# flood fill
def flood_fill(surface, x, y, new_color):
    target_color = surface.get_at((x, y))
    if target_color == new_color:
        return

    stack = [(x, y)]

    while stack:
        x, y = stack.pop()

        if surface.get_at((x, y)) != target_color:
            continue

        surface.set_at((x, y), new_color)

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < WIDTH and 0 <= ny < HEIGHT:
                stack.append((nx, ny))


running = True

while running:
    screen.fill(WHITE)
    screen.blit(canvas, (0, 0))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # клавиатура
        if event.type == pygame.KEYDOWN:

            # инструменты
            if event.key == pygame.K_1:
                tool = "pen"
            if event.key == pygame.K_2:
                tool = "rect"
            if event.key == pygame.K_3:
                tool = "circle"
            if event.key == pygame.K_4:
                tool = "eraser"
            if event.key == pygame.K_5:
                tool = "square"
            if event.key == pygame.K_6:
                tool = "r_triangle"
            if event.key == pygame.K_7:
                tool = "eq_triangle"
            if event.key == pygame.K_8:
                tool = "rhombus"
            if event.key == pygame.K_9:
                tool = "line"
            if event.key == pygame.K_f:
                tool = "fill"
            if event.key == pygame.K_t:
                tool = "text"

            # цвета
            if event.key == pygame.K_r:
                color = RED
            if event.key == pygame.K_g:
                color = GREEN
            if event.key == pygame.K_b:
                color = BLUE
            if event.key == pygame.K_k:
                color = BLACK

            if event.key == pygame.K_c:
                canvas.fill(WHITE)

            # сохранить
            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                filename = datetime.now().strftime("canvas_%Y%m%d_%H%M%S.png")
                pygame.image.save(canvas, filename)

            # текст
            if typing:
                if event.key == pygame.K_RETURN:
                    img = font.render(text_input, True, color)
                    canvas.blit(img, text_pos)
                    typing = False
                    text_input = ""
                elif event.key == pygame.K_ESCAPE:
                    typing = False
                    text_input = ""
                elif event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]
                else:
                    text_input += event.unicode

        # мышка
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos
            last_pos = event.pos

            # кнопки размера
            for btn in brush_buttons:
                if btn["rect"].collidepoint(event.pos):
                    brush_size = btn["size"]

            if tool == "fill":
                flood_fill(canvas, event.pos[0], event.pos[1], color)

            if tool == "text":
                typing = True
                text_pos = event.pos
                text_input = ""

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos

            # фигуры
            if tool == "rect":
                x = min(start_pos[0], end_pos[0])
                y = min(start_pos[1], end_pos[1])
                w = abs(start_pos[0] - end_pos[0])
                h = abs(start_pos[1] - end_pos[1])
                pygame.draw.rect(canvas, color, (x, y, w, h), brush_size)

            if tool == "circle":
                dx = end_pos[0] - start_pos[0]
                dy = end_pos[1] - start_pos[1]
                r = int((dx**2 + dy**2) ** 0.5)
                pygame.draw.circle(canvas, color, start_pos, r, brush_size)

            if tool == "square":
                dx = end_pos[0] - start_pos[0]
                dy = end_pos[1] - start_pos[1]
                size = min(abs(dx), abs(dy))
                x = start_pos[0] if dx >= 0 else start_pos[0] - size
                y = start_pos[1] if dy >= 0 else start_pos[1] - size
                pygame.draw.rect(canvas, color, (x, y, size, size), brush_size)

            if tool == "r_triangle":
                p1 = start_pos
                p2 = (start_pos[0], end_pos[1])
                p3 = (end_pos[0], end_pos[1])
                pygame.draw.polygon(canvas, color, [p1, p2, p3], brush_size)

            if tool == "eq_triangle":
                dx = end_pos[0] - start_pos[0]
                side = abs(dx)
                h = int((math.sqrt(3)/2)*side)

                if dx >= 0:
                    p1 = start_pos
                    p2 = (start_pos[0]+side, start_pos[1])
                    p3 = (start_pos[0]+side//2, start_pos[1]-h)
                else:
                    p1 = start_pos
                    p2 = (start_pos[0]-side, start_pos[1])
                    p3 = (start_pos[0]-side//2, start_pos[1]-h)

                pygame.draw.polygon(canvas, color, [p1, p2, p3], brush_size)

            if tool == "rhombus":
                cx = (start_pos[0]+end_pos[0])//2
                cy = (start_pos[1]+end_pos[1])//2
                dx = abs(end_pos[0]-start_pos[0])//2
                dy = abs(end_pos[1]-start_pos[1])//2

                p1 = (cx, cy-dy)
                p2 = (cx+dx, cy)
                p3 = (cx, cy+dy)
                p4 = (cx-dx, cy)

                pygame.draw.polygon(canvas, color, [p1,p2,p3,p4], brush_size)

            if tool == "line":
                pygame.draw.line(canvas, color, start_pos, end_pos, brush_size)

        if event.type == pygame.MOUSEMOTION:
            if drawing and tool == "pen":
                pygame.draw.line(canvas, color, last_pos, event.pos, brush_size)
                last_pos = event.pos

            if drawing and tool == "eraser":
                pygame.draw.circle(canvas, WHITE, event.pos, brush_size*2)

    # preview линии
    if drawing and tool == "line":
        pygame.draw.line(screen, color, start_pos, pygame.mouse.get_pos(), brush_size)

    # текст preview
    if typing:
        img = font.render(text_input, True, color)
        screen.blit(img, text_pos)

    draw_ui()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()