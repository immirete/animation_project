# animation_project/modules/face_renderer_pygame.py

import pygame
import math
import sys
from . import face  # Importa los patrones de cara

# Configuración Pygame
TARGET_WIDTH = 480
TARGET_HEIGHT = 320
COLS = 75
LED_SIZE_W = TARGET_WIDTH // COLS
ROWS = TARGET_HEIGHT // LED_SIZE_W
SCREEN_WIDTH = COLS * LED_SIZE_W
SCREEN_HEIGHT = ROWS * LED_SIZE_W
LED_SIZE = LED_SIZE_W

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

def init_pygame():
    global screen, clock, led_matrix
    try:
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(f"{COLS}x{ROWS} Face Animation")
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

    pygame.draw.rect(screen, border_color, (x_pixel, y_pixel, LED_SIZE, LED_SIZE))
    
    border_thickness = 1
    inner_x = x_pixel + border_thickness
    inner_y = y_pixel + border_thickness
    inner_size = LED_SIZE - (2 * border_thickness)
    
    if inner_size > 0:
        pygame.draw.rect(screen, center_color,
                        (inner_x, inner_y, inner_size, inner_size))

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
            draw_led(c * LED_SIZE, r * LED_SIZE, led_matrix[r][c])
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