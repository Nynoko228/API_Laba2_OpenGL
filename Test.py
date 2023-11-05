import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *
import random

# Размер окна
width, height = 800, 600

# Количество капель дождя
num_drops = 100

# Координаты и скорость каждой капли дождя
raindrops = [{'x': random.uniform(0, width), 'y': random.uniform(0, height), 'speed': random.uniform(50, 200)} for _ in
             range(num_drops)]


def draw_raindrop(x, y):
    glBegin(GL_LINES)
    glVertex2f(x, y)
    glVertex2f(x, y + 10)
    glEnd()


def draw_rain():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0.0, 0.0, 1.0)  # Цвет капель (синий)

    for drop in raindrops:
        draw_raindrop(drop['x'], drop['y'])

    glfw.swap_buffers(window)


def update_rain():
    global raindrops
    for drop in raindrops:
        drop['y'] -= drop['speed'] * glfw.get_time()
        if drop['y'] < 0:
            drop['y'] = height
            drop['x'] = random.uniform(0, width)


def main():
    global window

    if not glfw.init():
        return

    window = glfw.create_window(width, height, "Rain Animation", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glOrtho(0, width, height, 0, 0, 1)

    glfw.set_key_callback(window, key_callback)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        update_rain()
        draw_rain()

    glfw.terminate()


def key_callback(window, key, scancode, action, mods):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)


if __name__ == "__main__":
    main()