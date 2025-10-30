import pygame
import math
from parameters import *
from shapes import get_shapes
from math_utils import *
from ui import create_buttons, Slider
from graphics import render_scene, render_ui

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Визуальный движок по Python")

# Получение фигур
shapes = get_shapes()
# Текущая фигура
current_shape = "cube"
vertices = shapes[current_shape]["vertices"]
vertices_np = np.array(vertices)
faces = shapes[current_shape]["faces"]
face_colors = shapes[current_shape]["colors"]

# Углы вращения
angle_x = 0
angle_y = 0
angle_z = 0
# Текущий режим вращения
rotation_mode = "y"

# Параметры камеры
camera_distance = 4.0


# Back Face Culling
back_face_culling = True

# Создание кнопок
buttons = create_buttons()
# Активируем кнопку по умолчанию
buttons[1].is_active = True

# Создание ползунков
fov_slider = Slider(950, 550, 200, 25, FOV_MIN, FOV_MAX, FOV_DEFAULT, GRAY, LIGHT_BLUE)
ambient_slider = Slider(950, 605, 200, 25, AMBIENT_INTENSITY_MIN, AMBIENT_INTENSITY_MAX, AMBIENT_DEFAULT, GRAY, LIGHT_BLUE)

# Функции обработки действий
def global_set_rotation(mode):
    global rotation_mode
    rotation_mode = mode


def switch_shape():
    global current_shape, vertices, vertices_np, faces, face_colors
    if current_shape == "cube":
        current_shape = "pyramid"
    elif current_shape == "pyramid":
        current_shape = "sphere"
    elif current_shape == "sphere":
        current_shape = "thor"
    elif current_shape == "thor":
        current_shape = "mobius_strip"
    else:
        current_shape = "cube"

    vertices = shapes[current_shape]["vertices"]
    vertices_np = np.array(vertices)
    faces = shapes[current_shape]["faces"]
    face_colors = shapes[current_shape]["colors"]


def toggle_back_face_culling():
    global back_face_culling
    back_face_culling = not back_face_culling


def global_zoom_in():
    global camera_distance
    camera_distance = zoom_in(camera_distance, MIN_DISTANCE, ZOOM_SPEED)


def global_zoom_out():
    global camera_distance
    camera_distance = zoom_out(camera_distance, MAX_DISTANCE, ZOOM_SPEED)


def exit_code():
    global running
    running = False

# Создаем словарь для обработки кликов по кнопкам
button_actions = {
    0: lambda: global_set_rotation("x"),
    1: lambda: global_set_rotation("y"),
    2: lambda: global_set_rotation("z"),
    3: lambda: global_set_rotation("xy"),
    4: lambda: global_set_rotation("stop"),
    5: switch_shape,
    6: toggle_back_face_culling,
    7: lambda: global_zoom_in(),
    8: lambda: global_zoom_out(),
    9: exit_code
}

# Основной цикл
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, button in enumerate(buttons):
                if button.check_click(event.pos):
                    for btn in buttons:
                        btn.is_active = False
                    button.is_active = True

                    # Вызываем действие для нажатой кнопки
                    if i in button_actions:
                        button_actions[i]()

            # Обработка ползунков
            fov_slider.handle_event(event)
            ambient_slider.handle_event(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            fov_slider.handle_event(event)
            ambient_slider.handle_event(event)
        elif event.type == pygame.MOUSEMOTION:
            fov_slider.handle_event(event)
            ambient_slider.handle_event(event)

    screen.fill(BLACK)

    # Обновление углов вращения
    if rotation_mode == "x":
        angle_x += 0.01
    elif rotation_mode == "y":
        angle_y += 0.01
    elif rotation_mode == "z":
        angle_z += 0.01
    elif rotation_mode == "xy":
        angle_x += 0.01
        angle_y += 0.008

    # Значения для матрицы поворота
    cos_x, sin_x = math.cos(angle_x), math.sin(angle_x)
    cos_y, sin_y = math.cos(angle_y), math.sin(angle_y)
    cos_z, sin_z = math.cos(angle_z), math.sin(angle_z)

    # Матрица поворота
    Ry = np.array([[cos_y, 0, sin_y],
                   [0, 1, 0],
                   [-sin_y, 0, cos_y]])
    Rx = np.array([[1, 0, 0],
                   [0, cos_x, -sin_x],
                   [0, sin_x, cos_x]])
    Rz = np.array([[cos_z, -sin_z, 0],
                   [sin_z, cos_z, 0],
                   [0, 0, 1]])
    R = Rz @ Rx @ Ry

    # Список для повернутых вершин
    rotated_vertices = vertices_np @ R.T

    # Рендеринг сцены
    visible_face_count = render_scene(screen, current_shape, rotated_vertices, faces, face_colors,
                camera_distance, fov_slider.get_value(), ambient_slider.get_value(), LIGHT_DIRECTION, back_face_culling)

    # Рендеринг UI
    render_ui(screen, current_shape, camera_distance, rotation_mode, back_face_culling, visible_face_count,
              fov_slider.get_value(), ambient_slider.get_value(), buttons, fov_slider, ambient_slider, clock, faces)

    # Обновление экрана
    pygame.display.flip()
    clock.tick(240)

pygame.quit()