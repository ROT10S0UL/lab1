import pygame
import random
import sys
import os

# Инициализация
pygame.init()

# Размеры окна
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 155, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")

# Таймер
clock = pygame.time.Clock()
FPS = 10

# Шрифт
font = pygame.font.SysFont("Arial", 24)

RECORDS_FILE = "records.txt"


def draw_cell(x, y, color):
    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, color, rect)


def draw_snake(snake):
    for segment in snake:
        draw_cell(segment[0], segment[1], DARK_GREEN)


def draw_food(pos):
    draw_cell(pos[0], pos[1], RED)


def random_food_position(snake):
    while True:
        pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if pos not in snake:
            return pos


def show_text(text, x=10, y=10, color=WHITE):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

def draw_button(rect, text, mouse_pos):
    color = (180, 180, 180) if rect.collidepoint(mouse_pos) else GRAY
    pygame.draw.rect(screen, color, rect)
    show_text(text, rect.x + 20, rect.y + 8)

def load_record():
    if not os.path.exists(RECORDS_FILE):
        with open(RECORDS_FILE, "w") as f:
            f.write("0")
        return 0
    with open(RECORDS_FILE, "r") as f:
        content = f.read().strip()
        return int(content) if content.isdigit() else 0


def save_record(score):
    with open(RECORDS_FILE, "w") as f:
        f.write(str(score))


def game_over_menu(score, record):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        screen.fill(BLACK)
        show_text("Вы проиграли!", WIDTH // 2 - 100, HEIGHT // 2 - 80)
        show_text(f"Ваш счёт: {score}", WIDTH // 2 - 100, HEIGHT // 2 - 40)
        show_text(f"Рекорд: {record}", WIDTH // 2 - 100, HEIGHT // 2 - 10)

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        new_game_btn = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 30, 200, 40)
        exit_btn = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 80, 200, 40)

        # Цвет кнопок с подсветкой при наведении
        new_game_color = (180, 180, 180) if new_game_btn.collidepoint(mouse) else GRAY
        exit_btn_color = (180, 180, 180) if exit_btn.collidepoint(mouse) else GRAY

        pygame.draw.rect(screen, new_game_color, new_game_btn)
        pygame.draw.rect(screen, exit_btn_color, exit_btn)

        show_text("Новая игра", WIDTH // 2 - 60, HEIGHT // 2 + 38)
        show_text("Выход", WIDTH // 2 - 30, HEIGHT // 2 + 88)

        if new_game_btn.collidepoint(mouse) and click[0]:
            return True

        if exit_btn.collidepoint(mouse) and click[0]:
            return False

        pygame.display.flip()
        clock.tick(15)

def run_game():
    snake = [(5, 5), (4, 5), (3, 5)]
    direction = (1, 0)
    direction_buffer = direction
    food = random_food_position(snake)
    score = 0
    record = load_record()

    while True:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, 1):
                    direction_buffer = (0, -1)
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    direction_buffer = (0, 1)
                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    direction_buffer = (-1, 0)
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    direction_buffer = (1, 0)

        direction = direction_buffer
        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        if (
            head in snake
            or head[0] < 0 or head[0] >= GRID_WIDTH
            or head[1] < 0 or head[1] >= GRID_HEIGHT
        ):
            if score > record:
                save_record(score)
                record = score
            return game_over_menu(score, record)

        snake.insert(0, head)

        if head == food:
            score += 1
            food = random_food_position(snake)
        else:
            snake.pop()

        draw_snake(snake)
        draw_food(food)
        show_text(f"Счёт: {score}")

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    while True:
        restart = run_game()
        if not restart:
            pygame.quit()
            sys.exit()