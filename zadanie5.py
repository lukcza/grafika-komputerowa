#!/usr/bin/env python3
"""Zadanie 5: fraktal plazmowy z kontrolą klawiatury.

Sterowanie:
- SPACJA - wygenerowanie nowego fraktala,
- M - przełączenie trybu monochromatycznego / barwnego,
- strzałki góra/dół - zmiana rozmiaru siatki,
- strzałki lewo/prawo - zmiana parametru sigma,
- F - przełączenie funkcji wagowej,
- D - przełączenie rozkładu losowania koloru,
- ESC - wyjście z programu.
"""
import math
import random
import sys
import glfw
from OpenGL.GL import *
n = 7
mono = False
sigma = 100.0
weight_mode = 0
dist_mode = 0
grid = None
display_list = None
dirty = True
window = None
def random_value():
    if dist_mode == 0:
        return random.random()
    return min(1.0, max(0.0, random.gauss(0.5, 0.2)))
def random_color():
    if mono:
        v = random_value()
        return [v, v, v]
    return [random_value(), random_value(), random_value()]
def weight(x):
    if weight_mode == 0:
        return 0.5 * math.exp(-(x / sigma) ** 2)
    return 0.5 * max(0.0, 1.0 - x / (2.5 * sigma))
def weight_center(x):
    return weight(x) / 2.0
def side_color(ca, cb, w):
    """c = (1 - 2W) * c' + W * ca + W * cb  (srodek boku)"""
    cp = random_color()
    return [(1.0 - 2.0 * w) * cp[k] + w * ca[k] + w * cb[k] for k in range(3)]
def center_color(c1, c2, c3, c4, wc):
    """cc = (1 - 4Wc) * c' + Wc * (c1 + c2 + c3 + c4)  (srodek kwadratu)"""
    cp = random_color()
    return [(1.0 - 4.0 * wc) * cp[k] + wc * (c1[k] + c2[k] + c3[k] + c4[k])
            for k in range(3)]
def generate_plasma():
    size = 2 ** n + 1
    g = [[None] * size for _ in range(size)]

    for i in (0, size - 1):
        for j in (0, size - 1):
            g[i][j] = random_color()

    step = size - 1
    while step >= 2:
        half = step // 2
        x = step / (size - 1) * 250.0
        w = weight(x)
        wc = weight_center(x)

        for i in range(0, size - 1, step):
            for j in range(0, size - 1, step):
                c1 = g[i][j]
                c2 = g[i + step][j]
                c3 = g[i][j + step]
                c4 = g[i + step][j + step]

                if g[i + half][j] is None:
                    g[i + half][j] = side_color(c1, c2, w)
                if g[i + half][j + step] is None:
                    g[i + half][j + step] = side_color(c3, c4, w)
                if g[i][j + half] is None:
                    g[i][j + half] = side_color(c1, c3, w)
                if g[i + step][j + half] is None:
                    g[i + step][j + half] = side_color(c2, c4, w)

                g[i + half][j + half] = center_color(c1, c2, c3, c4, wc)
        step = half

    return g
def build_display_list():
    global display_list
    if display_list is not None:
        glDeleteLists(display_list, 1)

    size = len(grid)
    cell = 180.0 / (size - 1)

    display_list = glGenLists(1)
    glNewList(display_list, GL_COMPILE)
    glBegin(GL_QUADS)
    for i in range(size - 1):
        for j in range(size - 1):
            x0 = -90.0 + i * cell
            y0 = -90.0 + j * cell
            for di, dj in ((0, 0), (1, 0), (1, 1), (0, 1)):
                glColor3f(*grid[i + di][j + dj])
                glVertex2f(x0 + di * cell, y0 + dj * cell)
    glEnd()
    glEndList()
def update_title():
    if window is None:
        return
    size = 2 ** n + 1
    glfw.set_window_title(
        window,
        "Fraktal plazmowy | siatka %dx%d | %s | sigma=%d | W: %s | rozklad: %s"
        % (size, size,
           "mono" if mono else "kolor",
           sigma,
           "gauss" if weight_mode == 0 else "liniowa",
           "rownomierny" if dist_mode == 0 else "normalny"))

def startup():
    update_viewport(None, 600, 600)
    glClearColor(0.5, 0.5, 0.5, 1.0)

def shutdown():
    pass
def render(time):
    global grid, dirty
    if dirty:
        grid = generate_plasma()
        build_display_list()
        update_title()
        dirty = False

    glClear(GL_COLOR_BUFFER_BIT)
    glCallList(display_list)
    glFlush()


def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-100.0, 100.0, -100.0 / aspect, 100.0 / aspect, 1.0, -1.0)
    else:
        glOrtho(-100.0 * aspect, 100.0 * aspect, -100.0, 100.0, 1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def keyboard_key_callback(win, key, scancode, action, mods):
    global n, mono, sigma, weight_mode, dist_mode, dirty
    if action not in (glfw.PRESS, glfw.REPEAT):
        return

    if key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(win, glfw.TRUE)
    elif key == glfw.KEY_SPACE:
        dirty = True
    elif key == glfw.KEY_M:
        mono = not mono
        dirty = True
    elif key == glfw.KEY_F:
        weight_mode = 1 - weight_mode
        dirty = True
    elif key == glfw.KEY_D:
        dist_mode = 1 - dist_mode
        dirty = True
    elif key == glfw.KEY_UP:
        n = min(n + 1, 8)
        dirty = True
    elif key == glfw.KEY_DOWN:
        n = max(n - 1, 2)
        dirty = True
    elif key == glfw.KEY_RIGHT:
        sigma = min(sigma + 10.0, 300.0)
        dirty = True
    elif key == glfw.KEY_LEFT:
        sigma = max(sigma - 10.0, 10.0)
        dirty = True


def main():
    global window
    if not glfw.init():
        sys.exit(-1)

    window = glfw.create_window(600, 600, "Fraktal plazmowy", None, None)
    if not window:
        glfw.terminate()
        sys.exit(-1)

    glfw.make_context_current(window)
    glfw.set_framebuffer_size_callback(window, update_viewport)
    glfw.set_key_callback(window, keyboard_key_callback)
    glfw.swap_interval(1)

    startup()
    while not glfw.window_should_close(window):
        render(glfw.get_time())
        glfw.swap_buffers(window)
        glfw.poll_events()
    shutdown()

    glfw.terminate()
if __name__ == "__main__":
    main()