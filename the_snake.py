from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 5

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.

class GameObject():
    """Родительский класс для объектов рабочего поля."""

    def __init__(self):
        """
        Два атрибута:
            * начальная позиция - задается случайно,
            * цвет объекта - переопределяется внутри дочернего класса.
        """
        self.position = self.randomize_position()
        self.body_color = None

    def randomize_position(self):
        """Метод для определения начальной позиции объекта."""
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        return x, y

    def draw(self):
        """
        Метод для отображения объекта в рабочем пространстве,
        переопределяется в дочерних классах.
        """
        pass


class Apple(GameObject):
    """Класс-яблоко. Будем его искать и есть"""

    def __init__(self):
        """
        Оставляем атрибут родительского класса со случайным расположением.
        Переопределяем атрибут с цветом объекта.
        """
        super().__init__()
        self.body_color = APPLE_COLOR

    def draw(self):
        """Рисуем объект в рабочем пространстве."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс-змейка. Будет искать яблоко."""

    def __init__(self):
        """
        Атрибуты класса-змейка:
            * Не понимаю зачем нам тут super().__init__(),
                мы всё равно переопределяем все атрибуты родительского класса
            * length - длина объекта
            * positions - позиция объекта в пространстве,
                определяется списком заняты ячеек
            * direction - направление движения объекта
            * next_direction - изменение направления движения объекта
            * body_color - цвет
            * last - информация о последнем элементе объекта
        """
        super().__init__()
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = LEFT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def update_direction(self):
        """Изменяет направление движения"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """
        Определяет положение объекта с учетом направления движения.
        Учитываются особые ситуации,
        когда змейка достигает края рабочего пространства.
        """
        head_position = self.get_head_position()
        self.last = self.positions[-1]
        if (self.direction == RIGHT
                and head_position[0] == (SCREEN_WIDTH - GRID_SIZE)):
            new_head_position = (0, head_position[1])
        elif self.direction == LEFT and head_position[0] == 0:
            new_head_position = ((SCREEN_WIDTH - GRID_SIZE), head_position[1])
        elif self.direction == UP and head_position[1] == 0:
            new_head_position = (
                head_position[0],
                (SCREEN_HEIGHT - GRID_SIZE))
        elif (self.direction == DOWN
              and head_position[1] == (SCREEN_HEIGHT - GRID_SIZE)):
            new_head_position = (head_position[0], 0)
        else:
            new_head_position = (
                head_position[0] + self.direction[0] * GRID_SIZE,
                head_position[1] + self.direction[1] * GRID_SIZE
            )
        self.positions.insert(0, new_head_position)
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Отражение объекта на экране"""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Получает текущее положение головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сброс змейки к начальному состоянию."""
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Логика работы приложения"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    # apple = Apple()
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if apple.position in snake.positions:
            snake.length += 1
            apple = Apple()
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()


# Метод draw класса Apple
# def draw(self):
#     rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, rect)
#     pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

# # Метод draw класса Snake
# def draw(self):
#     for position in self.positions[:-1]:
#         rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
#         pygame.draw.rect(screen, self.body_color, rect)
#         pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
#     head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, head_rect)
#     pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
#         pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

# Функция обработки действий пользователя
# def handle_keys(game_object):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             raise SystemExit
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP and game_object.direction != DOWN:
#                 game_object.next_direction = UP
#             elif event.key == pygame.K_DOWN and game_object.direction != UP:
#             game_object.next_direction = DOWN
#             elif event.key == pygame.K_LEFT
#               and game_object.direction != RIGHT:
#             game_object.next_direction = LEFT
#             elif event.key == pygame.K_RIGHT
#               and game_object.direction != LEFT:
#                 game_object.next_direction = RIGHT

# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None
