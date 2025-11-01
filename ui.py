import pygame
from parameters import *

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

# Класс меню выбора фигуры
class ShapeSelectionWindow:
    def __init__(self, available_shapes, current_shape):
        self.width = 300
        self.height = 350  # Увеличено для размещения списка и кнопок
        self.x = (WIDTH - self.width) // 2
        self.y = (HEIGHT - self.height) // 2
        self.available_shapes = available_shapes
        self.current_selection = current_shape
        self.font = pygame.font.SysFont("Arial", 20)
        self.small_font = pygame.font.SysFont("Arial", 18)
        self.scroll_offset = 0 # Для прокрутки списка
        self.max_visible_items = 10 # Максимальное количество видимых элементов в списке

        # Кнопки OK и Cancel
        button_width = 80
        button_height = 30
        self.ok_button = pygame.Rect(self.x + 30, self.y + self.height - 50, button_width, button_height)
        self.cancel_button = pygame.Rect(self.x + self.width - 30 - button_width, self.y + self.height - 50, button_width, button_height)

        # Кнопка загрузки файла
        self.load_obj_button = pygame.Rect(self.x + (self.width - 120) // 2, self.y + self.height - 90, 120, 30) # Центрирована по ширине окна

        # Кнопки прокрутки (если нужно)
        self.scroll_up_button = pygame.Rect(self.x + self.width - 25, self.y + 40, 20, 20)
        self.scroll_down_button = pygame.Rect(self.x + self.width - 25, self.y + 40 + (self.max_visible_items * 25), 20, 20)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Проверка нажатия на элемент списка
            list_start_y = self.y + 40
            for i in range(self.scroll_offset, min(self.scroll_offset + self.max_visible_items, len(self.available_shapes))):
                item_y = list_start_y + (i - self.scroll_offset) * 25
                item_rect = pygame.Rect(self.x + 10, item_y, self.width - 40, 25)
                if item_rect.collidepoint(event.pos):
                    self.current_selection = self.available_shapes[i]


            # Проверка нажатия на кнопки
            if self.ok_button.collidepoint(event.pos):
                return self.current_selection
            elif self.cancel_button.collidepoint(event.pos):
                return None # Отмена
            elif self.load_obj_button.collidepoint(event.pos):
                # Возвращаем специальный идентификатор для загрузки OBJ
                return "load_obj"
            elif self.scroll_up_button.collidepoint(event.pos) and self.scroll_offset > 0:
                self.scroll_offset -= 1
            elif self.scroll_down_button.collidepoint(event.pos) and (self.scroll_offset + self.max_visible_items) < len(self.available_shapes):
                self.scroll_offset += 1
        return None # Ни одна кнопка не нажата

    def draw(self, screen):
        # Фон окна
        pygame.draw.rect(screen, GRAY, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height), 2) # Обводка

        # Заголовок
        title_text = self.font.render("Выберите фигуру", True, WHITE)
        screen.blit(title_text, (self.x + 10, self.y + 10))

        # Список фигур с прокруткой
        list_start_y = self.y + 40
        for i in range(self.scroll_offset, min(self.scroll_offset + self.max_visible_items, len(self.available_shapes))):
            item_y = list_start_y + (i - self.scroll_offset) * 25
            item_text = self.small_font.render(self.available_shapes[i], True, WHITE)
            bg_color = LIGHT_BLUE if self.available_shapes[i] == self.current_selection else GRAY
            pygame.draw.rect(screen, bg_color, (self.x + 10, item_y, self.width - 40, 25))
            screen.blit(item_text, (self.x + 15, item_y + 2))

        # Кнопка загрузки OBJ
        pygame.draw.rect(screen, (150, 100, 200), self.load_obj_button)
        pygame.draw.rect(screen, WHITE, self.load_obj_button, 1)
        load_obj_text = self.small_font.render("Загрузить OBJ", True, WHITE)
        screen.blit(load_obj_text, (self.load_obj_button.centerx - load_obj_text.get_width() // 2, self.load_obj_button.centery - load_obj_text.get_height() // 2))

        # Кнопки ОК и Отмена
        pygame.draw.rect(screen, LIGHT_BLUE, self.ok_button)
        pygame.draw.rect(screen, LIGHT_BLUE, self.cancel_button)
        pygame.draw.rect(screen, WHITE, self.ok_button, 1)
        pygame.draw.rect(screen, WHITE, self.cancel_button, 1)

        ok_text = self.small_font.render("OK", True, BLACK)
        cancel_text = self.small_font.render("Отмена", True, BLACK)
        screen.blit(ok_text, (self.ok_button.centerx - ok_text.get_width() // 2, self.ok_button.centery - ok_text.get_height() // 2))
        screen.blit(cancel_text, (self.cancel_button.centerx - cancel_text.get_width() // 2, self.cancel_button.centery - cancel_text.get_height() // 2))