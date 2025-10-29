import numpy as np
# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GRAY = (150, 150, 150)
DARK_GRAY = (80, 80, 80)
LIGHT_BLUE = (100, 150, 255)
ORANGE = (255, 165, 0)

# Настройки окна
WIDTH, HEIGHT = 1200, 800

# Параметры камеры
MIN_DISTANCE = 1.0
MAX_DISTANCE = 10.0
ZOOM_SPEED = 0.2

# FOV параметры
FOV_MIN = 50
FOV_MAX = 300
FOV_DEFAULT = 200

# Освещение
AMBIENT_INTENSITY_MIN = 0.0
AMBIENT_INTENSITY_MAX = 1.0
AMBIENT_DEFAULT = 0.2

# Направление света
LIGHT_DIRECTION = np.array([0.0, 0.0, -1.0])