import pygame
from parameters import WHITE, GRAY, LIGHT_BLUE, DARK_GRAY, BLACK, RED

# Класс для кнопок
class Button:
    def __init__(self, x, y, width, height, text, color, active_color, text_color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.active_color = active_color
        self.text_color = text_color
        self.is_active = False

    def draw(self, surface):
        color = self.active_color if self.is_active else self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 2)

        font = pygame.font.SysFont('Arial', 24)
        text_surf = font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_click(self, pos):
        return self.rect.collidepoint(pos)


# Класс для ползунка
class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, initial_val, color, handle_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.color = color
        self.handle_color = handle_color
        self.handle_width = 10
        self.handle_height = height
        self.dragging = False

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        # Рассчитываем позицию ползунка
        handle_x = self.rect.x + (self.value - self.min_val) / (self.max_val - self.min_val) * (
                self.rect.width - self.handle_width)
        handle_rect = pygame.Rect(handle_x, self.rect.y, self.handle_width, self.handle_height)
        pygame.draw.rect(surface, self.handle_color, handle_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                # Рассчитываем значение по позиции мыши
                rel_x = event.pos[0] - self.rect.x
                rel_x = max(0, min(rel_x, self.rect.width))
                self.value = self.min_val + (rel_x / self.rect.width) * (self.max_val - self.min_val)

    def get_value(self):
        return self.value

# Создание кнопок
def create_buttons():
    return [
        Button(50, 700, 100, 40, "X Axis", pygame.Color('red'), DARK_GRAY),  # i=0
        Button(170, 700, 100, 40, "Y Axis", pygame.Color('green'), DARK_GRAY),  # i=1
        Button(290, 700, 100, 40, "Z Axis", pygame.Color('blue'), DARK_GRAY),  # i=2
        Button(410, 700, 100, 40, "X + Y", pygame.Color('yellow'), DARK_GRAY),  # i=3
        Button(530, 700, 100, 40, "Stop", GRAY, DARK_GRAY),  # i=4
        Button(650, 700, 120, 40, "Switch Shape", (100, 100, 200), DARK_GRAY),  # i=5
        Button(780, 700, 150, 40, "Toggle Culling", (100, 100, 200), DARK_GRAY),  # i=6
        Button(940, 700, 50, 40, "+", LIGHT_BLUE, DARK_GRAY, BLACK),  # i=7
        Button(1000, 700, 50, 40, "-", LIGHT_BLUE, DARK_GRAY, BLACK),  # i=8
        Button(1060, 700, 100, 40, "Exit", RED, DARK_GRAY, BLACK)
    ]