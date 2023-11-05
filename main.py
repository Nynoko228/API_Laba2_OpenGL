#import pygame as pg
import glfw
import glfw.GLFW as GLFW_CONSTANTS
from OpenGL.GL import *
import numpy as np
import ctypes
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr
from PIL import Image

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
RETURN_ACTION_CONTINUE = 0
RETURN_ACTION_END = 1

def init_glfw():
    glfw.init()
    glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(
        GLFW_CONSTANTS.GLFW_OPENGL_PROFILE,
        GLFW_CONSTANTS.GLFW_OPENGL_CORE_PROFILE
    )
    glfw.window_hint(
        GLFW_CONSTANTS.GLFW_OPENGL_FORWARD_COMPAT,
        GLFW_CONSTANTS.GLFW_TRUE
    )
    glfw.window_hint(GLFW_CONSTANTS.GLFW_DOUBLEBUFFER, GL_FALSE) # Поставить на GL_TRUE ради 60 ФПС

    window = glfw.create_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Test", None, None)
    glfw.make_context_current(window)
    glfw.set_input_mode(
        window,
        GLFW_CONSTANTS.GLFW_CURSOR,
        GLFW_CONSTANTS.GLFW_CURSOR_HIDDEN
    )

    return window

class App:
    def __init__(self, window):
        self.window = window
        self.render = graphicsEngine()
        self.scene = Scene()

        self.lastTime = glfw.get_time()
        self.currentTime = 0
        self.numFrames = 0
        self.frameTime = 0


        # pg.init()
        # pg.display.set_mode((640, 480), pg.OPENGL | pg.DOUBLEBUF)
        # self.clock = pg.time.Clock()
        # glClearColor(0.1, 0.2, 0.2, 1)
        # glEnable(GL_BLEND)
        # glEnable(GL_DEPTH_TEST)
        # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        # self.shader = self.createShader()
        # glUseProgram(self.shader)  # Устанавливаем шейдер
        # glUniform1i(glGetUniformLocation(self.shader, "imageTexture"), 0)  # 0 потому, что мы выбрали нулевую текстуру

        # self.cube_mesh = CubeMesh()

        # self.texture = Material("Xexe.png")

        # # Создаём переменную для проекции нашего объекта
        # projection_transform = pyrr.matrix44.create_perspective_projection(
        #     fovy=45, aspect=640 / 480,
        #     near=0.1, far=10, dtype=np.float32
        # )
        #
        # glUniformMatrix4fv(
        #     glGetUniformLocation(self.shader, "projection"),  # Местоположение объекта
        #     1, GL_FALSE, projection_transform  # Передаём 1 матрицу 4 на 4
        # )
        #
        # self.modelMatrixLocation = glGetUniformLocation(self.shader, "model")

        self.mainloop()

    # def createShader(self):
    #
    #     with open("vertex.txt", 'r') as f:
    #         vertex_src = f.readlines()
    #
    #     with open("fragment.txt", 'r') as f:
    #         fragment_src = f.readlines()
    #
    #     # Компилируем шейдеры
    #     shader = compileProgram(
    #         compileShader(vertex_src, GL_VERTEX_SHADER),
    #         compileShader(fragment_src, GL_FRAGMENT_SHADER)
    #     )
    #
    #     return shader

    # Игровой цикл программы
    def mainloop(self):

        running = True
        while (running):
            # Проверяем события
            if glfw.window_should_close(self.window) or glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_ESCAPE) == GLFW_CONSTANTS.GLFW_PRESS:
                running = False

            glfw.poll_events()


            # for event in pg.event.get():
            #     if event.type == pg.QUIT:
            #         running = False

            # # Обновление информации на экране
            # glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            #
            # glUseProgram(self.shader)  # Обновляем щейдер
            # self.texture.use()
            # model_transform = pyrr.matrix44.create_identity(dtype=np.float32)
            # model_transform = pyrr.matrix44.multiply(
            #     m1=model_transform,
            #     m2=pyrr.matrix44.create_from_eulers(
            #         eulers=np.radians(self.cube.eulers),
            #         dtype=np.float32
            #     )
            # )
            #
            # model_transform = pyrr.matrix44.multiply(
            #     m1=model_transform,
            #     m2=pyrr.matrix44.create_from_translation(
            #         vec=self.cube.position,
            #         dtype=np.float32
            #     )
            # )
            #
            # glUniformMatrix4fv(self.modelMatrixLocation, 1, GL_FALSE, model_transform)
            # glBindVertexArray(self.cube_mesh.vao)  # Получаем точки для рисования
            # glDrawArrays(GL_TRIANGLES, 0, self.cube_mesh.vertex_cnt)  # Рисуем треугольник
            #
            # pg.display.flip()

            # Частота кадров
            self.clock.tick(60)
        self.quit()

    # Выход
    # def quit(self):
    #
    #     self.cube_mesh.destroy()
    #     self.texture.destroy()
    #     glDeleteProgram(self.shader)
    #     pg.quit()


class graphicsEngine:
    def __init__(self):
        self.cube_mesh = CubeMesh()
        self.texture = Material("Xexe.png")

        # Инициализируем OpenGL
        glClearColor(0.1, 0.2, 0.2, 1)
        glEnable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.shader = self.createShader()
        glUseProgram(self.shader)  # Устанавливаем шейдер
        glUniform1i(glGetUniformLocation(self.shader, "imageTexture"), 0)  # 0 потому, что мы выбрали нулевую текстуру

        # Создаём переменную для проекции нашего объекта
        projection_transform = pyrr.matrix44.create_perspective_projection(
            fovy=45, aspect=640 / 480,
            near=0.1, far=10, dtype=np.float32
        )

        glUniformMatrix4fv(
            glGetUniformLocation(self.shader, "projection"),  # Местоположение объекта
            1, GL_FALSE, projection_transform  # Передаём 1 матрицу 4 на 4
        )

        self.modelMatrixLocation = glGetUniformLocation(self.shader, "model")
        self.viewMatrixLocation = glGetUniformLocation(self.shader, "view")

    def createShader(self):
        with open("vertex.txt", 'r') as f:
            vertex_src = f.readlines()

        with open("fragment.txt", 'r') as f:
            fragment_src = f.readlines()

        # Компилируем шейдеры
        shader = compileProgram(
            compileShader(vertex_src, GL_VERTEX_SHADER),
            compileShader(fragment_src, GL_FRAGMENT_SHADER)
        )

        return shader

    def render(self, scene):
        # Обновление информации на экране
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUseProgram(self.shader)  # Обновляем щейдер
        self.texture.use()
        view_transform = pyrr.matrix44.create_look_at(
            eye=scene.player.position,
            target=scene.player.position + scene.player.forwards,
            up=scene.player.up,
            dtype=np.float32
        )
        glUniformMatrix4fv(self.viewMatrixLocation, 1, GL_FALSE, view_transform)

        self.texture.use()
        glBindVertexArray(self.cube_mesh.vao)  # Получаем точки для рисования
        for cube in scene.cubes:
            model_transform = pyrr.matrix44.create_identity(dtype=np.float32)
            model_transform = pyrr.matrix44.multiply(
                m1=model_transform,
                m2=pyrr.matrix44.create_from_eulers(
                    eulers=np.radians(self.cube.eulers),
                    dtype=np.float32
                )
            )

            model_transform = pyrr.matrix44.multiply(
                m1=model_transform,
                m2=pyrr.matrix44.create_from_translation(
                    vec=self.cube.position,
                    dtype=np.float32
                )
            )
            glUniformMatrix4fv(self.modelMatrixLocation, 1, GL_FALSE, model_transform)
            # glBindVertexArray(self.cube_mesh.vao)  # Получаем точки для рисования
            glDrawArrays(GL_TRIANGLES, 0, self.cube_mesh.vertex_cnt)  # Рисуем треугольник

        glFlush()

    # Выход
    def quit(self):
        self.cube_mesh.destroy()
        self.texture.destroy()
        glDeleteProgram(self.shader)



class CubeMesh:
    def __init__(self):
        # x, y, z, s, t - все значения для точек/вершин
        self.vertices = (
            -0.5, -0.5, -0.5, 0, 0,
            0.5, -0.5, -0.5, 1, 0,
            0.5, 0.5, -0.5, 1, 1,

            0.5, 0.5, -0.5, 1, 1,
            -0.5, 0.5, -0.5, 0, 1,
            -0.5, -0.5, -0.5, 0, 0,

            -0.5, -0.5, 0.5, 0, 0,
            0.5, -0.5, 0.5, 1, 0,
            0.5, 0.5, 0.5, 1, 1,

            0.5, 0.5, 0.5, 1, 1,
            -0.5, 0.5, 0.5, 0, 1,
            -0.5, -0.5, 0.5, 0, 0,

            -0.5, 0.5, 0.5, 1, 0,
            -0.5, 0.5, -0.5, 1, 1,
            -0.5, -0.5, -0.5, 0, 1,

            -0.5, -0.5, -0.5, 0, 1,
            -0.5, -0.5, 0.5, 0, 0,
            -0.5, 0.5, 0.5, 1, 0,

            0.5, 0.5, 0.5, 1, 0,
            0.5, 0.5, -0.5, 1, 1,
            0.5, -0.5, -0.5, 0, 1,

            0.5, -0.5, -0.5, 0, 1,
            0.5, -0.5, 0.5, 0, 0,
            0.5, 0.5, 0.5, 1, 0,

            -0.5, -0.5, -0.5, 0, 1,
            0.5, -0.5, -0.5, 1, 1,
            0.5, -0.5, 0.5, 1, 0,

            0.5, -0.5, 0.5, 1, 0,
            -0.5, -0.5, 0.5, 0, 0,
            -0.5, -0.5, -0.5, 0, 1,

            -0.5, 0.5, -0.5, 0, 1,
            0.5, 0.5, -0.5, 1, 1,
            0.5, 0.5, 0.5, 1, 0,

            0.5, 0.5, 0.5, 1, 0,
            -0.5, 0.5, 0.5, 0, 0,
            -0.5, 0.5, -0.5, 0, 1
        )

        self.vertex_cnt = len(self.vertices) // 5
        self.vertices = np.array(self.vertices, dtype=np.float32)

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.vbo = glGenBuffers(1)  # Генерируем 1 буфер для точек/вершин
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)
        # В vertices дежат циферки каждая циферка по 4 байта. 32 - это некий вес 1 точки, а c_void_p - смещение для Положения/Цвета/Текстуры
        glEnableVertexAttribArray(0)  # Положение
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)  # Цвет
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(12))
        glEnableVertexAttribArray(2)  # Тестура
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(24))

    def destroy(self):
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1, (self.vbo,))


class Cube:

    def __init__(self, position, eulers):
        self.position = np.array(position, dtype=np.float32)  # Положение куба
        self.eulers = np.array(eulers, dtype=np.float32)  # Угол наклона куба


class Scene:

    def __init__(self):
        self.cubes = [
            Cube(
                position=[6, 0, 0],
                eulers=[0, 0, 0]
            )
        ]

        self.player = Player(position=[0, 0, 2])

    def update(self, rate):
        for cube in self.cubes:
            cube.eulers[1] += 0.25 * rate
            if cube.eulers[1] > 360:
                cube.eulers[1] -= 360

    def move_player(self, dPos):
        dPos = np.array(dPos, dtype=np.float32)
        self.player.position += dPos

    def spin_player(self, dTheta, dPhi):
        self.player.theta += dTheta
        if self.player.theta > 360:
            self.player.theta -= 360
        elif self.player.theta < 0:
            self.player.theta += 360

        self.player.phi = min(
            89, max(-89, self.player.phi + dPhi)
        )

        self.player.update_vectors()


class Player:

    def __init__(self, position):
        self.position = np.array(position, dtype=np.float32)
        self.theta = 0  # угол для горизонтали
        self.phi = 0  # угол для вертикали
        self.update_vectors()

    def update_vectors(self):
        self.forwards = np.array(
            [
                np.cos(np.deg2rad(self.theta)) * np.cos(np.deg2rad(self.phi)),
                np.sin(np.deg2rad(self.theta)) * np.cos(np.deg2rad(self.phi)),
                np.sin(np.deg2rad(self.phi))
            ]
        )

        globalUp = np.array([0, 0, 1], dtype=np.float32)

        self.right = np.cross(self.forwards, globalUp)

        self.up = np.cross(self.right, self.forwards)


class Material:

    def __init__(self, path_to_texture):
        self.texture = glGenTextures(1)  # 1 текстура
        glBindTexture(GL_TEXTURE_2D, self.texture)  # привязываем текстуру
        # Определяем расположение текстуры
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        # Некий ресайз текстуры
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        with Image.open(path_to_texture, mode='r') as image:
            # image = pg.image.load(
            #     path_to_texture).convert_alpha()  # Загружаем изображение и конвертируем его в удобный пиксельный формат
            image_width, image_height = image.size  # Получаем размер изображения
            image = image.convert("RGBA")
            image_data = bytes(image.tobytes())  # Получаем нужные данные в удобном формате
            # Загружаем нашу текстуру
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_width, image_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
        # Генерируем
        glGenerateMipmap(GL_TEXTURE_2D)

    def use(self):
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)

    def destroy(self):
        glDeleteTextures(1, (self.texture,))


if __name__ == "__main__":
    window = init_glfw()
    start = App(window)
