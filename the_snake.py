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
CENTER_CELL = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
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
        self.last = None

    def draw(self, position_to_draw_rect):
        """Рисуем объект в рабочем пространстве."""
        x, y = position_to_draw_rect[0][0], position_to_draw_rect[0][1]
        rect = pg.Rect(x, y, GRID_SIZE, GRID_SIZE)
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


class Apple(GameObject):
    """Класс-яблоко. Будем его искать и есть"""

    def __init__(self, position_taken=None, color=APPLE_COLOR):
        """
        Оставляем атрибут родительского класса со случайным расположением.
        Переопределяем атрибут с цветом объекта.
        """
        super().__init__(color)
        self.position_taken = position_taken if position_taken else []
        self.randomize_position(position_taken)

    def randomize_position(self, position_taken):
        """
        Метод для определения начальной позиции объекта.
        Учитывает поля занятые змейкой.
        """
        while True:
            x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            coordinate = [(x, y)]
            if coordinate not in position_taken:
                self.position = coordinate
                break


class Snake(GameObject):
    """Класс-змейка. Будет искать яблоко."""

    def __init__(self, color=SNAKE_COLOR):
        """
        Атрибуты класса-змейка:
            * Не понимаю зачем нам тут super().__init__(),
                мы всё равно переопределяем все атрибуты родительского класса
            * length - длина объекта
            * position - позиция объекта в пространстве,
                определяется списком заняты ячеек
            * direction - направление движения объекта
            * next_direction - изменение направления движения объекта
            * body_color - цвет
            * last - информация о последнем элементе объекта
        """
        super().__init__(color)
        self.length = 1
        self.direction = LEFT

    def update_direction(self, new_direction):
        """Изменяет направление движения"""
        self.direction = new_direction

    def get_head_position(self):
        """Получает текущее положение головы змейки."""
        return self.position[0]

    def move(self):
        """
        Определяет положение объекта с учетом направления движения.
        Учитываются особые ситуации,
        когда змейка достигает края рабочего пространства.
        """
        x, y = self.get_head_position()
        self.last = self.position[-1] if self.length > 1 else self.position[0]
        new_head_position = (
            (x + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (y + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.position.insert(0, new_head_position)
        if len(self.position) > self.length:
            self.position.pop()

    def reset(self):
        """Сброс змейки к начальному состоянию."""
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.length = 1
        self.position = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = LEFT
        self.last = None


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
            elif event.key == pg.K_UP and snake.direction != DOWN:
                snake.update_direction(UP)
            elif event.key == pg.K_DOWN and snake.direction != UP:
                snake.update_direction(DOWN)
            elif event.key == pg.K_LEFT and snake.direction != RIGHT:
                snake.update_direction(LEFT)
            elif event.key == pg.K_RIGHT and snake.direction != LEFT:
                snake.update_direction(RIGHT)


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
    apple = Apple(snake.position)
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()
        if apple.position[0] == snake.position[0]:
            snake.length += 1
            apple.randomize_position(snake.position)
        elif snake.get_head_position() in snake.position[4:]:
            snake.reset()
            apple.randomize_position(snake.position)
        pg.display.set_caption(
            f'Змейка, для выхода нажми Escape. '
            f'Рекорд: {record_length_func(snake.length)}'
        )
        snake.draw(snake.position)
        apple.draw(apple.position)
        pg.display.update()


if __name__ == '__main__':
    main()
