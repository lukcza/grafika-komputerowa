#!/usr/bin/env python3
"""Zadanie 1: trójkąt z trzema kolorami w wierzchołkach.

Sterowanie:
- ESC - wyjście z programu.
"""

import sys

import glfw
from OpenGL.GL import *


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass


def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(-50.0, -50.0)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(50.0, -50.0)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(0.0, 50.0)
    glEnd()

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
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, glfw.TRUE)


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