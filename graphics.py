import pygame
import numpy as np
from math_utils import bresenham_algorithm, calculate_face_normal, apply_lambert_lighting, is_face_visible
from parameters import WIDTH, HEIGHT, WHITE

def render_scene(screen, rotated_vertices, faces, face_colors, camera_distance, fov, ambient_intensity, light_direction, back_face_culling):
    # Создаем Z-буфер (глубинный буфер) и заполняем его бесконечностью
    z_buffer = np.full((HEIGHT, WIDTH), np.inf)

    # Шаг 1: Проецирование 3D точек в 2D
    projected_points = []
    for i in range(len(rotated_vertices)):
        x, y, z = rotated_vertices[i]
        factor = fov / (camera_distance + z)
        x_proj = x * factor + WIDTH // 2
        y_proj = y * factor + HEIGHT // 2
        projected_points.append([x_proj, y_proj])

    # Шаг 2: Отрисовка каждой грани с использованием Z-буфера
    visible_face_count = 0
    camera_position = np.array([0, 0, -camera_distance])

    for i, face in enumerate(faces):
        face_vertices_3d = [rotated_vertices[idx] for idx in face]

        # Проверяем видимость грани с помощью Back Face Culling
        face_normal = calculate_face_normal(face_vertices_3d)
        face_center = np.mean(face_vertices_3d, axis=0)
        if back_face_culling and not is_face_visible(face_normal, face_center, camera_position):
            continue  # Пропускаем невидимую грань

        # Вычисляем расстояние от камеры до центра грани
        face_distance = np.linalg.norm(camera_position - face_center)

        # Применяем модель освещения Ламберта
        color = face_colors[i]
        lighted_color = apply_lambert_lighting(color, face_normal, light_direction, ambient_intensity)

        # Получаем 2D координаты вершин грани
        face_points = [projected_points[idx] for idx in face]
        # Преобразуем в целочисленные координаты для Pygame
        face_points_int = [(int(x), int(y)) for x, y in face_points]

        # --- Ключевое изменение: Используем pygame.Surface и PixelArray для быстрой заливки ---
        # Получаем ограничивающий прямоугольник (bounding box) для грани
        if not face_points_int: continue # Проверка на пустую грань
        min_x = max(0, int(min(p[0] for p in face_points_int)))
        max_x = min(WIDTH - 1, int(max(p[0] for p in face_points_int)))
        min_y = max(0, int(min(p[1] for p in face_points_int)))
        max_y = min(HEIGHT - 1, int(max(p[1] for p in face_points_int)))

        # Создаем временный Surface для этой грани
        temp_surface = pygame.Surface((max_x - min_x + 1, max_y - min_y + 1), pygame.SRCALPHA)
        temp_surface.fill((0, 0, 0, 0))  # Прозрачный фон

        # Заливаем грань на временном Surface
        # Смещаем точки для отрисовки на temp_surface
        offset_points = [(x - min_x, y - min_y) for x, y in face_points_int]
        pygame.draw.polygon(temp_surface, lighted_color, offset_points)

        # Получаем массив пикселей из временного Surface
        pixel_array = pygame.PixelArray(temp_surface)

        # Перебираем только те пиксели, которые были залиты (не прозрачные)
        for local_y in range(temp_surface.get_height()):
            for local_x in range(temp_surface.get_width()):
                # Получаем цвет пикселя
                pixel_color = pixel_array[local_x, local_y]
                if pixel_color != 0:  # Если пиксель не прозрачный
                    # Вычисляем глобальные координаты пикселя
                    global_x = min_x + local_x
                    global_y = min_y + local_y

                    # Проверяем, не выходит ли пиксель за пределы экрана
                    if 0 <= global_x < WIDTH and 0 <= global_y < HEIGHT:
                        # Сравниваем расстояние центра грани с Z-буфером
                        # Если центр грани ближе, чем то, что в буфере, рисуем пиксель
                        if face_distance < z_buffer[global_y, global_x]:
                            # Обновляем цвет и Z-буфер
                            screen.set_at((global_x, global_y), lighted_color)
                            z_buffer[global_y, global_x] = face_distance

        # Увеличиваем счётчик видимых граней
        visible_face_count += 1

    # Шаг 3: Рисуем контур для всех видимых граней (для наглядности)
    # Это делается отдельно, чтобы контуры не затирались заливкой
    for i, face in enumerate(faces):
        face_vertices_3d = [rotated_vertices[idx] for idx in face]
        face_normal = calculate_face_normal(face_vertices_3d)
        face_center = np.mean(face_vertices_3d, axis=0)
        if back_face_culling and not is_face_visible(face_normal, face_center, camera_position):
            continue  # Пропускаем невидимую грань

        face_points = [projected_points[idx] for idx in face]
        for j in range(len(face_points)):
            x0, y0 = face_points[j]
            x1, y1 = face_points[(j + 1) % len(face_points)]
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