import pygame
import numpy as np
from math_utils import bresenham_algorithm, calculate_face_normal, apply_lambert_lighting, is_face_visible
from parameters import WIDTH, HEIGHT, WHITE

def render_scene(screen, current_shape, rotated_vertices, faces, face_colors, camera_distance, fov, ambient_intensity, light_direction, back_face_culling):
    # Шаг 1: Проецирование 3D точек в 2D
    projected_points = []
    for i in range(len(rotated_vertices)):
        x, y, z = rotated_vertices[i]
        factor = fov / (camera_distance + z)
        x_proj = x * factor + WIDTH // 2
        y_proj = y * factor + HEIGHT // 2
        projected_points.append([x_proj, y_proj])

    # Шаг 2: Расчёт средней Z-координаты (z_avg) для каждой грани
    needs_sorting = current_shape != "mobius_strip"
    needs_bfc = back_face_culling and current_shape != "mobius_strip"

    if needs_sorting:
        faces_with_depth = []
        for i, face in enumerate(faces):
            face_vertices_3d = [rotated_vertices[idx] for idx in face]
            # Вычисляем среднюю Z-координату вершин грани
            z_cords = [vertex[2] for vertex in face_vertices_3d]
            z_avg = sum(z_cords) / len(z_cords)

            faces_with_depth.append((face, z_avg, face_colors[i]))

        # Шаг 3: Сортировка всех граней по z_avg
        if current_shape == "thor":
            faces_with_depth.sort(key=lambda x: x[1], reverse=True)
        else:
            faces_with_depth.sort(key=lambda x: x[1])
    else:
        faces_with_depth = [(faces[i], 0, face_colors[i]) for i in range(len(faces))]

    # Шаг 4: Проверка видимости после сортировки
    visible_face_count = 0
    for face, z_avg, color in faces_with_depth:
        face_vertices_3d = [rotated_vertices[idx] for idx in face]
        face_normal = calculate_face_normal(face_vertices_3d)
        face_center = np.mean(face_vertices_3d, axis=0)

        # Проверяем видимость грани с помощью Back Face Culling
        if needs_bfc and not is_face_visible(face_normal, face_center, camera_position=np.array([0, 0, -camera_distance])):
            continue  # Пропускаем невидимую грань

        # Применяем модель освещения Ламберта
        lighted_color = apply_lambert_lighting(color, face_normal, light_direction, ambient_intensity)

        # Шаг 5: Отрисовка текущей грани
        face_points = [projected_points[idx] for idx in face]
        # Проверка на валидность полигона (не все точки лежат на одной прямой)
        if len(face_points) >= 3 and not are_points_collinear(face_points):
            try:
                pygame.draw.polygon(screen, lighted_color, face_points)
            except TypeError:
                print(f"Предупреждение: Пропущена грань в точках: {face_points}")

        # Рисуем контур через алгоритм Брезенхэма
        for i in range(len(face_points)):
            x0, y0 = face_points[i]
            x1, y1 = face_points[(i + 1) % len(face_points)]
            x0, y0, x1, y1 = map(int, [x0, y0, x1, y1])
            line_points = bresenham_algorithm(x0, y0, x1, y1)
            for px, py in line_points:
                if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                    screen.set_at((px, py), WHITE)

        visible_face_count += 1

    return visible_face_count

def are_points_collinear(points, tolerance=1e-5):
    if len(points) < 3:
        return False
    p0, p1 = points[0], points[1]
    for i in range(2, len(points)):
        p2 = points[i]
        area = abs((p1[0] - p0[0]) * (p2[1] - p0[1]) - (p2[0] - p0[0]) * (p1[1] - p0[1]))
        if area > tolerance:
             return False
    return True

def render_ui(screen, current_shape, camera_distance, rotation_mode, back_face_culling, visible_face_count, fov_value, ambient_value, buttons, fov_slider, ambient_slider, clock, faces):
    # Создание шрифта
    font = pygame.font.SysFont("Arial", 24)

    # Отрисовка кнопок
    for button in buttons:
        button.draw(screen)

    # Отрисовка ползунков
    fov_slider.draw(screen)
    ambient_slider.draw(screen)

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

    # Отображение текущего значения FOV
    fov_text = f"FOV: {int(fov_value)}"
    fov_surf = font.render(fov_text, True, WHITE)
    screen.blit(fov_surf, (950, 525))

    # Отображение текущей интенсивности света
    ambient_text = f"Яркость: {ambient_value:.2f}"
    ambient_surf = font.render(ambient_text, True, WHITE)
    screen.blit(ambient_surf, (950, 575))

# Функция для отрисовки и обработки окна выбора фигуры
def render_shape_selection_window(screen, event, selection_window):
    result = selection_window.handle_event(event)
    selection_window.draw(screen)

    if result is not None:
        return result
    if event.type == pygame.QUIT:
        return False
    return None
