import numpy as np
from parameters import BLUE, RED, GREEN, YELLOW, ORANGE, LIGHT_BLUE
import random

def get_shapes():
    shapes = {
        "cube": {
            "vertices": [
                [-1, -1, -1],  # 0 - задний левый нижний
                [1, -1, -1],  # 1 - задний правый нижний
                [1, 1, -1],  # 2 - задний правый верхний
                [-1, 1, -1],  # 3 - задний левый верхний
                [-1, -1, 1],  # 4 - передний левый нижний
                [1, -1, 1],  # 5 - передний правый нижний
                [1, 1, 1],  # 6 - передний правый верхний
                [-1, 1, 1]  # 7 - передний левый верхний
            ],
            "faces": [
                [0, 3, 2, 1],  # задняя грань (против часовой стрелки)
                [4, 5, 6, 7],  # передняя грань (против часовой стрелки)
                [0, 1, 5, 4],  # нижняя грань (против часовой стрелки)
                [3, 7, 6, 2],  # верхняя грань (против часовой стрелки)
                [0, 4, 7, 3],  # левая грань (против часовой стрелки)
                [1, 2, 6, 5]  # правая грань (против часовой стрелки)
            ],
            "colors": [
                BLUE,  # задняя грань
                RED,  # передняя грань
                GREEN,  # нижняя грань
                YELLOW,  # верхняя грань
                (255, 100, 235),  # левая грань (пурпурный)
                (0, 255, 255)  # правая грань (голубой)
            ]
        },
        "pyramid": {
            "vertices": [
                [-1, -1, -1],  # 0 - основание левый нижний
                [1, -1, -1],  # 1 - основание правый нижний
                [1, 1, -1],  # 2 - основание правый верхний
                [-1, 1, -1],  # 3 - основание левый верхний
                [0, 0, 1]  # 4 - вершина
            ],
            "faces": [
                [0, 1, 4],  # передняя грань
                [1, 2, 4],  # правая грань
                [2, 3, 4],  # задняя грань
                [3, 0, 4],  # левая грань
                [0, 3, 2, 1]  # основание (против часовой стрелки)
            ],
            "colors": [
                RED,  # передняя грань
                GREEN,  # правая грань
                BLUE,  # задняя грань
                YELLOW,  # левая грань
                ORANGE  # основание
            ]
        },
        "sphere": {
            "vertices": [],
            "faces": [],
            "colors": []
        },
        "thor": {
            "vertices": [],
            "faces": [],
            "colors": []
        },
        "mobius_strip": {
            "vertices": [],
            "faces": [],
            "colors": []
        }
    }

    # Параметризация сферы
    r_sphere = 1.0
    num_theta = 15  # Количество точек по долготе
    num_phi = 9  # Количество точек по широте

    theta = np.linspace(0, 2 * np.pi, num_theta, endpoint=False)
    phi = np.linspace(0, np.pi, num_phi)
    phi_grid, theta_grid = np.meshgrid(phi, theta, indexing="ij")

    x = r_sphere * np.sin(phi_grid) * np.cos(theta_grid)
    y = r_sphere * np.sin(phi_grid) * np.sin(theta_grid)
    z = r_sphere * np.cos(phi_grid)

    # Собираем вершины в список списков (для совместимости с остальным кодом)
    vertices = np.stack([x, y, z], axis=-1).reshape(-1, 3)  # shape: (num_lat * num_lon, 3)
    shapes["sphere"]["vertices"] = vertices.tolist()

    # Генерация граней
    faces = []

    # Северный полюс → треугольники к первой параллели (i=1)
    for j in range(num_theta):
        pole = 0  # i=0, любая j — все одинаковые
        v1 = 1 * num_theta + j
        v2 = 1 * num_theta + (j + 1) % num_theta
        faces.append([pole, v2, v1])

    # Основная часть: quads между i=1 и i=num_phi-2
    for i in range(1, num_phi - 2):
        for j in range(num_theta):
            a = i * num_theta + j
            b = i * num_theta + (j + 1) % num_theta
            c = (i + 1) * num_theta + (j + 1) % num_theta
            d = (i + 1) * num_theta + j
            faces.append([a, b, c, d])

    # Южный полюс → треугольники от последней параллели (i=num_phi-2)
    south_pole = (num_phi - 1) * num_theta  # i=num_phi-1, j=0
    for j in range(num_theta):
        v1 = (num_phi - 2) * num_theta + j
        v2 = (num_phi - 2) * num_theta + (j + 1) % num_theta
        faces.append([v2, south_pole, v1])

    shapes["sphere"]["faces"] = faces

    col_blue = int(len(faces) * 0.7)
    col_green = len(faces) - col_blue

    colors_sphere = [LIGHT_BLUE] * col_blue + [GREEN] * col_green
    random.shuffle(colors_sphere)
    shapes["sphere"]["colors"] = colors_sphere


    # Параметризация Тора
    R_thor = 1.2
    r_thor = 0.6
    num_theta_tor = 20
    num_phi_tor = 10

    theta = np.linspace(0, 2 * np.pi, num_theta_tor, endpoint=False)
    phi = np.linspace(0, 2 * np.pi, num_phi_tor, endpoint=False)
    phi_grid_t, theta_grid_t = np.meshgrid(phi, theta, indexing="ij")

    x_t = (R_thor + r_thor * np.cos(phi_grid_t)) * np.cos(theta_grid_t)
    y_t = (R_thor + r_thor * np.cos(phi_grid_t)) * np.sin(theta_grid_t)
    z_t = r_thor * np.sin(phi_grid_t)

    vertices_thor = np.stack([x_t, y_t, z_t], axis=-1).reshape(-1, 3)
    shapes["thor"]["vertices"] = vertices_thor.tolist()

    faces_thor = []
    for i in range(num_phi_tor):
        for j in range(num_theta_tor):
            a = i * num_theta_tor + j
            b = i * num_theta_tor + (j + 1) % num_theta_tor
            c = ((i + 1) % num_phi_tor) * num_theta_tor + (j + 1) % num_theta_tor
            d = ((i + 1) % num_phi_tor) * num_theta_tor + j
            faces_thor.append([a, b, c, d])

    shapes["thor"]["faces"] = faces_thor
    shapes["thor"]["colors"] = [ORANGE] * len(faces_thor)

    # --- Параметризация Ленты Мёбиуса ---
    # Независимые параметры u и v
    R_mobius = 1.5  # Радиус ленты (расстояние от центра до средней линии)
    w_mobius = 0.6  # Половина ширины ленты (v изменяется от -w до +w)
    num_u = 30  # Количество точек по длине ленты (u от 0 до 2pi)
    num_v = 10  # Количество точек по ширине ленты (v от -w до +w)

    # Параметры u и v
    u = np.linspace(0, 2 * np.pi, num_u, endpoint=False)  # endpoint=False помогает избежать дублирования края
    v = np.linspace(-w_mobius, w_mobius, num_v)

    # Создание сетки параметров
    u_grid, v_grid = np.meshgrid(u, v, indexing="ij")  # shape: (num_u, num_v)

    # Вычисление координат по параметрическому уравнению
    cos_u_half = np.cos(u_grid / 2)
    sin_u_half = np.sin(u_grid / 2)
    cos_u = np.cos(u_grid)
    sin_u = np.sin(u_grid)

    x_m = (R_mobius + (v_grid / 2) * cos_u_half) * cos_u
    y_m = (R_mobius + (v_grid / 2) * cos_u_half) * sin_u
    z_m = (v_grid / 2) * sin_u_half

    # Собираем вершины
    vertices_mobius = np.stack([x_m, y_m, z_m], axis=-1).reshape(-1, 3)
    shapes["mobius_strip"]["vertices"] = vertices_mobius.tolist()

    # Генерация граней (четырехугольников)
    faces_mobius = []
    for i in range(num_v - 1):
        for j in range(num_u):
            # Индексы вершин текущего четырехугольника
            a = i * num_u + j
            b = i * num_u + (j + 1) % num_u  # Обеспечиваем цикличность по u
            c = (i + 1) * num_u + (j + 1) % num_u
            d = (i + 1) * num_u + j
            faces_mobius.append([a, b, c, d])
    shapes["mobius_strip"]["faces"] = faces_mobius

    # Цвета для ленты Мёбиуса
    shapes["mobius_strip"]["colors"] = [YELLOW] * len(faces_mobius)

    return shapes