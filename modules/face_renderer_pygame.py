import pygame
import math
import sys
from . import face  # Importa los patrones de cara

# Configuración Pygame
TARGET_WIDTH = 480
TARGET_HEIGHT = 320
COLS = 75
LED_WIDTH = TARGET_WIDTH // COLS
LED_HEIGHT_RATIO = 2.0  # Proporción altura/ancho
LED_HEIGHT = int(LED_WIDTH * LED_HEIGHT_RATIO)
ROWS = TARGET_HEIGHT // LED_HEIGHT
SCREEN_WIDTH = COLS * LED_WIDTH
SCREEN_HEIGHT = ROWS * LED_HEIGHT

# Colores
BLACK = (0, 0, 0)
DARK_GRAY = (30, 30, 30)
LIGHT_GRAY = (60, 60, 60)
DARK_ORANGE = (180, 80, 0)
BRIGHT_YELLOW = (255, 200, 0)

# Variables globales de Pygame
screen = None
clock = None
led_matrix = [[0 for _ in range(COLS)] for _ in range(ROWS)]

def set_led_height_ratio(ratio):
    global LED_HEIGHT_RATIO, LED_HEIGHT, ROWS, SCREEN_HEIGHT
    LED_HEIGHT_RATIO = max(0.5, min(3.0, ratio))
    LED_HEIGHT = int(LED_WIDTH * LED_HEIGHT_RATIO)
    ROWS = TARGET_HEIGHT // LED_HEIGHT
    SCREEN_HEIGHT = ROWS * LED_HEIGHT
    global led_matrix
    led_matrix = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    global screen
    if screen:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def init_pygame():
    global screen, clock, led_matrix
    try:
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(f"{COLS}x{ROWS} Face Animation (Ratio: {LED_HEIGHT_RATIO:.1f})")
        clock = pygame.time.Clock()
        led_matrix = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        return True
    except pygame.error as e:
        print(f"Error initializing Pygame: {e}")
        return False

def cleanup_pygame():
    pygame.quit()

def draw_led(x_pixel, y_pixel, state):
    if not screen:
        return

    border_color = DARK_ORANGE if state else DARK_GRAY
    center_color = BRIGHT_YELLOW if state else LIGHT_GRAY

    pygame.draw.rect(screen, border_color, (x_pixel, y_pixel, LED_WIDTH, LED_HEIGHT))
    
    border_thickness = 1
    inner_x = x_pixel + border_thickness
    inner_y = y_pixel + border_thickness
    inner_width = LED_WIDTH - (2 * border_thickness)
    inner_height = LED_HEIGHT - (2 * border_thickness)
    
    if inner_width > 0 and inner_height > 0:
        pygame.draw.rect(screen, center_color,
                        (inner_x, inner_y, inner_width, inner_height))

def update_matrix_from_patterns(eye_pattern, mouth_pattern):
    global led_matrix
    led_matrix = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    
    total_ascii_height = len(eye_pattern) + len(mouth_pattern)
    available_rows = ROWS
    base_offset_y = max(0, (available_rows - total_ascii_height) // 3)
    
    eye_offset_y = base_offset_y
    mouth_offset_y = eye_offset_y + len(eye_pattern)
    
    for r, line in enumerate(eye_pattern):
        draw_row = r + eye_offset_y
        if 0 <= draw_row < ROWS:
            for c, char in enumerate(line):
                draw_col = c
                if 0 <= draw_col < COLS and char in ['O', '0']:
                    led_matrix[draw_row][draw_col] = 1
    
    for r, line in enumerate(mouth_pattern):
        draw_row = r + mouth_offset_y
        if 0 <= draw_row < ROWS:
            for c, char in enumerate(line):
                draw_col = c
                if 0 <= draw_col < COLS and char in ['O', '0']:
                    led_matrix[draw_row][draw_col] = 1

def draw_frame():
    if not screen:
        return
    screen.fill(BLACK)
    for r in range(ROWS):
        for c in range(COLS):
            draw_led(c * LED_WIDTH, r * LED_HEIGHT, led_matrix[r][c])
    pygame.display.flip()

def tick_clock(fps=30):
    if clock:
        clock.tick(fps)

def handle_events():
    if not screen:
        return False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True