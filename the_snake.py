from random import randint

import pygame as pg

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

BOARD_BACKGROUND_COLOR = (100, 100, 100)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
SPEED = 10
CENTER_CELL = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
record_length = 1

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
screen.fill(BOARD_BACKGROUND_COLOR)

# Заголовок окна игрового поля:
# pg.display.set_caption('Змейка, для выхода закрой окно или нажми Escape')

# Настройка времени:
clock = pg.time.Clock()


class GameObject():
    """Родительский класс для объектов рабочего поля."""

    def __init__(self, color=BOARD_BACKGROUND_COLOR):
        """
        Два атрибута:
            * начальная позиция - задается случайно,
            * цвет объекта - переопределяется внутри дочернего класса.
        """
        self.position = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.body_color = color

    def draw(self):
        """Рисуем объект в рабочем пространстве."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс-яблоко. Будем его искать и есть"""

    def __init__(self, color=APPLE_COLOR):
        """
        Оставляем атрибут родительского класса со случайным расположением.
        Переопределяем атрибут с цветом объекта.
        """
        super().__init__(color)
        self.position = self.randomize_position()

    def randomize_position(self):
        """Метод для определения начальной позиции объекта."""
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        return x, y


class Snake(GameObject):
    """Класс-змейка. Будет искать яблоко."""

    def __init__(self, color=SNAKE_COLOR):
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
        super().__init__(color)
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = LEFT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Изменяет направление движения"""
        if self.next_direction:
            self.direction = self.next_direction

    def move(self):
        """
        Определяет положение объекта с учетом направления движения.
        Учитываются особые ситуации,
        когда змейка достигает края рабочего пространства.
        """
        X, Y = self.get_head_position()
        self.last = self.position[-1]
        if self.direction == RIGHT and X == (SCREEN_WIDTH - GRID_SIZE):
            new_head_position = (SCREEN_WIDTH % SCREEN_WIDTH, Y)
        elif self.direction == LEFT and X == 0:
            new_head_position = ((SCREEN_WIDTH - GRID_SIZE), Y)
        elif self.direction == UP and Y == 0:
            new_head_position = (X, (SCREEN_HEIGHT - GRID_SIZE))
        elif self.direction == DOWN and Y == (SCREEN_HEIGHT - GRID_SIZE):
            new_head_position = (X, SCREEN_HEIGHT % SCREEN_HEIGHT)
        else:
            new_head_position = (
                X + self.direction[0] * GRID_SIZE,
                Y + self.direction[1] * GRID_SIZE
            )
        self.position.insert(0, new_head_position)
        if len(self.position) > self.length:
            self.position.pop()

    def draw(self):
        """Отражение объекта на экране"""
        # Отрисовка головы змейки
        head_rect = pg.Rect(self.position[0], (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Получает текущее положение головы змейки."""
        return self.position[0]

    def reset(self):
        """Сброс змейки к начальному состоянию."""
        self.length = 1
        self.position = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(snake):
    """Функция обработки действий пользователя"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pg.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pg.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pg.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT
            elif event.key == pg.K_ESCAPE:
                pg.quit()
                raise SystemExit


def record_length_func(snake_length):
    """Фиксирует максимальную длину змейки в рамках игровой сессии."""
    global record_length
    if snake_length > record_length:
        record_length = snake_length
    return record_length


def main():
    """Логика работы приложения"""
    # Инициализация pg:
    pg.init()
    apple = Apple(APPLE_COLOR)
    snake = Snake(APPLE_COLOR)
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if apple.position in snake.position:
            snake.length += 1
            apple = Apple(APPLE_COLOR)
        if snake.get_head_position() in snake.position[1:]:
            snake.reset()
        pg.display.set_caption(
            f'Змейка, для выхода закрой окно или нажми Escape. '
            f'Рекорд: {record_length_func(snake.length)}'
        )
        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()


# Метод draw класса Apple
# def draw(self):
#     rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
#     pg.draw.rect(screen, self.body_color, rect)
#     pg.draw.rect(screen, BORDER_COLOR, rect, 1)

# # Метод draw класса Snake
# def draw(self):
#     for position in self.positions[:-1]:
#         rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
#         pg.draw.rect(screen, self.body_color, rect)
#         pg.draw.rect(screen, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
#     head_rect = pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pg.draw.rect(screen, self.body_color, head_rect)
#     pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
#         pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

# Функция обработки действий пользователя
# def handle_keys(game_object):
#     for event in pg.event.get():
#         if event.type == pg.QUIT:
#             pg.quit()
#             raise SystemExit
#         elif event.type == pg.KEYDOWN:
#             if event.key == pg.K_UP and game_object.direction != DOWN:
#                 game_object.next_direction = UP
#             elif event.key == pg.K_DOWN and game_object.direction != UP:
#             game_object.next_direction = DOWN
#             elif event.key == pg.K_LEFT
#               and game_object.direction != RIGHT:
#             game_object.next_direction = LEFT
#             elif event.key == pg.K_RIGHT
#               and game_object.direction != LEFT:
#                 game_object.next_direction = RIGHT

# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None
