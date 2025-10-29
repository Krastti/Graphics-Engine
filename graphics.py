import pygame
import numpy as np
from math_utils import bresenham_algorithm, calculate_face_normal, apply_lambert_lighting, is_face_visible
from parameters import WIDTH, HEIGHT, WHITE


def render_scene(screen, rotated_vertices, faces, face_colors, camera_distance, fov, ambient_intensity, light_direction, back_face_culling):
    # Шаг 1: Проецирование 3D точек в 2D
    projected_points = []
    for i in range(len(rotated_vertices)):
        x, y, z = rotated_vertices[i]

        factor = fov / (camera_distance + z)
        x_proj = x * factor + WIDTH // 2
        y_proj = y * factor + HEIGHT // 2
        projected_points.append([x_proj, y_proj])

    # Шаг 2: Расчёт расстояния от камеры до центра каждой грани
    faces_with_depth = []
    camera_position = np.array([0, 0, -camera_distance])
    for i, face in enumerate(faces):
        face_vertices_3d = [rotated_vertices[idx] for idx in face]
        face_center = np.mean(face_vertices_3d, axis=0)
        # Вычисляем истинное расстояние от камеры до центра грани
        distance_to_camera = np.linalg.norm(camera_position - face_center)
        # Сохраняем грань, истинное расстояние и цвет
        faces_with_depth.append((face, distance_to_camera, face_colors[i]))

    # Шаг 3: Сортировка граней по расстоянию (от дальнего к ближнему)
    faces_with_depth.sort(key=lambda x: x[1])

    # Шаг 4: Проверка видимости граней и применение освещения
    visible_faces = []
    visible_face_count = 0

    for face, distance_to_camera, color in faces_with_depth:
        # Получаем 3D координаты вершин грани
        face_vertices_3d = [rotated_vertices[idx] for idx in face]

        face_normal = calculate_face_normal(face_vertices_3d)

        face_center = np.mean(face_vertices_3d, axis=0)

        # Проверяем видимость грани с помощью Back Face Culling
        if back_face_culling and not is_face_visible(face_normal, face_center, camera_position):
            continue  # Пропускаем невидимую грань

        # Применяем модель освещения Ламберта
        lighted_color = apply_lambert_lighting(color, face_normal, light_direction, ambient_intensity)
        visible_faces.append((face, distance_to_camera, lighted_color))
        visible_face_count += 1  # Увеличиваем счётчик видимых граней

    # Шаг 5: Отрисовка видимых граней
    for face, distance_to_camera, color in visible_faces:
        # Получаем 2D координаты вершин грани
        face_points = [projected_points[idx] for idx in face]

        # Заливка грани с освещением
        pygame.draw.polygon(screen, color, face_points)

        # Рисуем контур через алгоритм Брезенхэма
        for i in range(len(face_points)):
            x0, y0 = face_points[i]
            x1, y1 = face_points[(i + 1) % len(face_points)]
            x0, y0, x1, y1 = map(int, [x0, y0, x1, y1])
            line_points = bresenham_algorithm(x0, y0, x1, y1)
            for px, py in line_points:
                if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                    screen.set_at((px, py), WHITE)

    return visible_face_count


def render_ui(screen, current_shape, camera_distance, rotation_mode, back_face_culling, visible_face_count,
              fov_value, ambient_value, buttons, fov_slider, ambient_slider, clock, faces):
    # Отрисовка кнопок
    for button in buttons:
        button.draw(screen)

    # Отрисовка ползунков
    fov_slider.draw(screen)
    ambient_slider.draw(screen)

    # Создание шрифта
    font = pygame.font.SysFont("Arial", 24)

    # Отображение текущей фигуры
    shape_text = f"Фигура: {current_shape.capitalize()}"
    shape_surf = font.render(shape_text, True, WHITE)
    screen.blit(shape_surf, (50, 250))

    # Отображение расстояния камеры
    distance_text = f"Дистанция камеры: {camera_distance:.1f}"
    distance_surf = font.render(distance_text, True, WHITE)
    screen.blit(distance_surf, (50, 300))

    # Отображение режима вращения
    mode_text = ""
    if rotation_mode == "x":
        mode_text = "Вращение: X Ось"
    elif rotation_mode == "y":
        mode_text = "Вращение: Y Ось"
    elif rotation_mode == "z":
        mode_text = "Вращение: Z Ось"
    elif rotation_mode == "xy":
        mode_text = "Вращение: X + Y Оси"
    elif rotation_mode == "stop":
        mode_text = "Вращение: Остановлено"
    text_surf = font.render(mode_text, True, WHITE)
    screen.blit(text_surf, (50, 350))

    # Отображение статуса Back Face Culling
    culling_status = "ON" if back_face_culling else "OFF"
    culling_text = f"Back Face Culling: {culling_status}"
    culling_surf = font.render(culling_text, True, WHITE)
    screen.blit(culling_surf, (50, 400))

    # Отображение счётчика видимых граней
    visible_faces_text = f"Видимые грани: {visible_face_count}/{len(faces)}"
    visible_faces_surf = font.render(visible_faces_text, True, WHITE)
    screen.blit(visible_faces_surf, (50, 450))

    # Отображение FPS
    fps = clock.get_fps()
    fps_text = f"FPS: {int(fps)}"
    fps_surf = font.render(fps_text, True, WHITE)
    screen.blit(fps_surf, (50, 500))

    # Отображение текущего значения FOV (над ползунком)
    fov_text = f"FOV: {int(fov_value)}"
    fov_surf = font.render(fov_text, True, WHITE)
    screen.blit(fov_surf, (950, 525))

    # Отображение текущей интенсивности света (над ползунком)
    ambient_text = f"Яркость: {ambient_value:.2f}"
    ambient_surf = font.render(ambient_text, True, WHITE)
    screen.blit(ambient_surf, (950, 575))