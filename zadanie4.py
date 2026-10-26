#!/usr/bin/env python3
"""Zadanie 4: dywan Sierpińskiego z rekurencyjnym wycinaniem środka.

Sterowanie:
- strzałki góra/dół - zmieniają poziom rekurencji,
- ESC - wyjście z programu.
"""

import sys
import glfw
from OpenGL.GL import *
level = 3
def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)
def shutdown():
    pass
def draw_rectangle(x, y, a, b):
    """Rysuje prostokąt z dwóch trójkątów."""
    p1 = (x, y)
    p2 = (x + a, y)
    p3 = (x + a, y + b)
    p4 = (x, y + b)
    glBegin(GL_TRIANGLES)
    glVertex2f(*p1); glVertex2f(*p2); glVertex2f(*p3)
    glVertex2f(*p1); glVertex2f(*p3); glVertex2f(*p4)
    glEnd()
def sierpinski_carpet(x, y, a, b, n):
    """Dzieli prostokąt na 3 × 3 i rekurencyjnie pomija środek."""
    if n == 0:
        draw_rectangle(x, y, a, b)
        return
    a3, b3 = a / 3.0, b / 3.0
    for i in range(3):
        for j in range(3):
            if i == 1 and j == 1:
                continue
            sierpinski_carpet(x + i * a3, y + j * b3, a3, b3, n - 1)
def render(time):
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0.6, 0.2, 0.0)
    sierpinski_carpet(-90.0, -90.0, 180.0, 180.0, level)
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
def keyboard_key_callback(window, key, scancode, action, mods):
    global level
    if action not in (glfw.PRESS, glfw.REPEAT):
        return
    if key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, glfw.TRUE)
    elif key == glfw.KEY_UP:
        level = min(level + 1, 6)
    elif key == glfw.KEY_DOWN:
        level = max(level - 1, 0)
def main():
    if not glfw.init():
        sys.exit(-1)
    window = glfw.create_window(600, 600, "Grafika komputerowa", None, None)
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