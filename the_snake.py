from random import choice

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

# Изменение направления движения.
# Проверяем текущее направление движение и нажатую клавишу.
# Для каждой пары однозначно задаем возможный вариант движения.
CHANGE_DIRECTION = {
    (LEFT, pg.K_UP): UP,
    (RIGHT, pg.K_UP): UP,
    (LEFT, pg.K_DOWN): DOWN,
    (RIGHT, pg.K_DOWN): DOWN,
    (DOWN, pg.K_LEFT): LEFT,
    (UP, pg.K_LEFT): LEFT,
    (DOWN, pg.K_RIGHT): RIGHT,
    (UP, pg.K_RIGHT): RIGHT,
}

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


# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Родительский класс для объектов рабочего поля."""

    def __init__(self, color=BOARD_BACKGROUND_COLOR):
        """
        Два атрибута:
            * начальная позиция - задается случайно,
            * цвет объекта - переопределяется внутри дочернего класса.
        """
        self.position = CENTER_CELL
        self.body_color = color

    def draw_a_cell(self, position, color=None, draw_border=True):
        """Рисуем объект в рабочем пространстве."""
        color = color or self.body_color
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)
        if draw_border:
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """
        Абстрактный метод, который предназначен
        для переопределения в дочерних классах.
        Этот метод должен определять, как объект
        будет отрисовываться на экране.
        """


class Apple(GameObject):
    """Класс-яблоко. Будем его искать и есть"""

    def __init__(self, positions_taken=[CENTER_CELL], color=APPLE_COLOR):
        """
        Оставляем атрибут родительского класса со случайным расположением.
        Переопределяем атрибут с цветом объекта.
        """
        super().__init__(color)
        self.randomize_position(positions_taken)

    def randomize_position(self, positions):
        """
        Метод для определения начальной позиции объекта.
        Учитывает поля занятые змейкой.
        """
        ALL_CELLS = set((x * GRID_SIZE, y * GRID_SIZE)
                        for x in range(GRID_WIDTH)
                        for y in range(GRID_HEIGHT))
        self.position = choice(list(ALL_CELLS - set(positions)))

    def draw(self):
        """Рисует яблоко"""
        self.draw_a_cell(self.position)


class Snake(GameObject):
    """Класс-змейка. Будет искать яблоко."""

    def __init__(self, color=SNAKE_COLOR):
        """
        Атрибуты класса-змейка:
            * length - длина объекта
            * positions - позиция объекта в пространстве,
                определяется списком заняты ячеек
            * direction - направление движения объекта
            * last - информация о последнем элементе объекта
        """
        super().__init__(color)
        self.positions = [self.position]
        self.direction = LEFT

    def update_direction(self, new_direction):
        """Изменяет направление движения"""
        self.direction = new_direction

    def get_head_position(self):
        """Получает текущее положение головы змейки."""
        return self.positions[0]

    def move(self):
        """
        Определяет положение объекта с учетом направления движения.
        Учитываются особые ситуации,
        когда змейка достигает края рабочего пространства.
        """
        x, y = self.get_head_position()
        x_delta, y_delta = self.direction
        self.last = self.positions[-1]
        self.positions.insert(0,
                              (((x + x_delta * GRID_SIZE) % SCREEN_WIDTH),
                               ((y + y_delta * GRID_SIZE) % SCREEN_HEIGHT))
                              )
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Рисует змейку"""
        self.draw_a_cell(self.get_head_position())
        if self.last:
            self.draw_a_cell(self.last,
                             BOARD_BACKGROUND_COLOR,
                             draw_border=False)

    def reset(self):
        """Сброс змейки к начальному состоянию."""
        self.length = 1
        self.positions = [self.position]
        self.direction = LEFT


def handle_keys(snake):
    """Функция обработки действий пользователя"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                raise SystemExit
            snake.update_direction(CHANGE_DIRECTION.get(
                (snake.direction, event.key),
                snake.direction)
            )


def record_length_func(snake_length):
    """Фиксирует максимальную длину змейки в рамках игровой сессии."""
    global record_length
    record_length = max(record_length, snake_length)
    return record_length


def main():
    """Логика работы приложения"""
    # Инициализация pg:
    pg.init()
    snake = Snake()
    snake.reset()
    apple = Apple(snake.positions)
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()
        if apple.position == snake.get_head_position():
            snake.length += 1
            apple.randomize_position(snake.positions)
        elif snake.get_head_position() in snake.positions[4:]:
            snake.reset()
            apple.randomize_position(snake.positions)
            screen.fill(BOARD_BACKGROUND_COLOR)
        pg.display.set_caption(
            f'Змейка, для выхода нажми Escape. '
            f'Рекорд: {record_length_func(snake.length)}'
        )
        snake.draw()
        apple.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
