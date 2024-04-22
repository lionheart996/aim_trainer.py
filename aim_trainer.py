import math
import random
import time
import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Trainer")

TARGET_INCREMENT = 600

TARGET_EVENT = pygame.USEREVENT
TARGET_PADDING = 30

BACKGROUND_COLOR = (0, 25, 40)
# 0 red
# 25 green
# 40 blue
LIVES = 3
TOP_BAR_HEIGHT = 50

LEBEL_FONT = pygame.font.SysFont("comicsans", 24)


class Target:
    MAX_SIZE = 30
    GROWTH_RATE = 0.2
    COLOR = "red"
    SECOND_COLOR = "white"

    def __init__(self, x, y):
        self.x= x
        self.y = y
        self.size = 0
        self.grow = True

    def update(self):
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
            self.grow = False

        if self.grow:
            self.size += self.GROWTH_RATE
        else:
            self.size -= self.GROWTH_RATE

    def draw(self, window):
        pygame.draw.circle(window, self.COLOR, (self.x, self.y), self.size)
        pygame.draw.circle(window, self.SECOND_COLOR, (self.x, self.y), self.size * 0.8)
        pygame.draw.circle(window, self.COLOR, (self.x, self.y), self.size * 0.6)
        pygame.draw.circle(window, self.SECOND_COLOR, (self.x, self.y), self.size * 0.4)

    def collide(self, x, y):
        distance = math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)
        return distance <= self.size


def draw(window, targets):
    window.fill(BACKGROUND_COLOR)

    for target in targets:
        target.draw(window)


def format_time(secs):
    milli = math.floor(int(secs * 100 % 1000) / 100)
    seconds = int(round(secs % 60, 1))
    minutes = int(secs // 60)

    return f"{minutes:02d}:{seconds:02d}.{milli}"


def draw_top_bar(window, elapsed_time, targets_pressed, misses):

    pygame.draw.rect(window, "grey", (0, 0, WIDTH, TOP_BAR_HEIGHT))
    time_lebel = LEBEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "black")

    speed = round(targets_pressed / elapsed_time, 1)
    speed_lebel = LEBEL_FONT.render(f"Speed: {speed} t/s", 1, "black")

    hits_lebel = LEBEL_FONT.render(f"Hits: {targets_pressed}", 1, "black")

    lives_lebel = LEBEL_FONT.render(f"Lives: {LIVES - misses}", 1, "black")

    window.blit(time_lebel, (5, 5))
    window.blit(speed_lebel, (200, 5))
    window.blit(hits_lebel, (450, 5))
    window.blit(lives_lebel, (650, 5))


def end_screen(window, elapsed_time, targets_pressed, clicks):
    window.fill(BACKGROUND_COLOR)

    time_lebel = LEBEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "white")

    speed = round(targets_pressed / elapsed_time, 1)
    speed_lebel = LEBEL_FONT.render(f"Speed: {speed} t/s", 1, "white")

    hits_lebel = LEBEL_FONT.render(f"Hits: {targets_pressed}", 1, "white")

    accuracy = round(targets_pressed / clicks * 100, 1)
    accuracy_lebel = LEBEL_FONT.render(f"Accuracy: {accuracy}%", 1, "white")

    window.blit(time_lebel, (get_middle(time_lebel), 100))
    window.blit(speed_lebel, (get_middle(speed_lebel), 200))
    window.blit(hits_lebel, (get_middle(hits_lebel), 300))
    window.blit(accuracy_lebel, (get_middle(accuracy_lebel), 400))

    pygame.display.update()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                quit()

def get_middle(surface):
    return WIDTH / 2  - surface.get_width() / 2


def main():
    run = True
    targets = []
    clock = pygame.time.Clock()

    targets_pressed = 0
    clicks = 0
    misses = 0
    start_time = time.time()

    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)

    while run:
        clock.tick(60)
        click = False
        mouse_pos = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == TARGET_EVENT:
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
    #             so the target doesn't appear off the screen
                y = random.randint(
                    TARGET_PADDING + TOP_BAR_HEIGHT, HEIGHT - TARGET_PADDING)
                target = Target(x, y)
                targets.append(target)

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1

        for target in targets:
            target.update()

            if target.size <= 0:
                targets.remove(target)
                misses += 1

            if click and target.collide(*mouse_pos):
                targets.remove(target)
                targets_pressed += 1

        if misses >= LIVES:
            end_screen(WINDOW, elapsed_time, targets_pressed, clicks)

        draw(WINDOW, targets)
        draw_top_bar(WINDOW, elapsed_time, targets_pressed, misses)

        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()



