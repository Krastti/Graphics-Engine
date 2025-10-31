import numpy as np

# Алгоритм Брезенхэма для рисования линий
def bresenham_algorithm(x0, y0, x1, y1):
    points = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1

    if dx > dy:
        error = 2 * dy - dx
        y = y0
        for x in range(x0, x1 + sx, sx):
            points.append([x, y])
            if error >= 0:
                y += sy
                error -= 2 * dx
            error += 2 * dy
    else:
        error = 2 * dx - dy
        x = x0
        for y in range(y0, y1 + sy, sy):
            points.append([x, y])
            if error >= 0:
                x += sx
                error -= 2 * dy
            error += 2 * dx
    return points

# Функция для вычисления нормали к грани
def calculate_face_normal(face_vertices):
    v1 = np.array(face_vertices[1]) - np.array(face_vertices[0])
    v2 = np.array(face_vertices[2]) - np.array(face_vertices[0])

    # Вычисляем нормаль как векторное произведение
    normal = np.cross(v1, v2)
    norm = np.linalg.norm(normal)

    if norm == 0:
        return np.array([0, 0, 1])
    normal = (normal / norm).astype(np.float64)
    return  normal

# Функция для применения модели освещения Ламберта
def apply_lambert_lighting(base_color, normal, light_dir, ambient):

    normal = normal / np.linalg.norm(normal)
    light_dir = light_dir / np.linalg.norm(light_dir)

    diffuse = max(0.0, np.dot(normal, light_dir))

    intensity = min(1.0, (ambient + diffuse))

    lighted_color = tuple(int(c * intensity) for c in base_color)

    return lighted_color

# Функция для проверки видимости грани (Back Face Culling)
def is_face_visible(face_normal, face_center, camera_position):
    # Вектор от центра грани к камере
    to_camera = camera_position - face_center

    # Если нормаль направлена наружу, то для видимой грани скалярное произведение нормали и вектора к камере будет положительным
    return np.dot(face_normal, to_camera) > 0.0

# Функция для приближения камеры
def zoom_in(camera_distance, min_distance, zoom_speed):
    return max(min_distance, camera_distance - zoom_speed)

# Функция для отдаления камеры
def zoom_out(camera_distance, max_distance, zoom_speed):
    return min(max_distance, camera_distance + zoom_speed)