import pygame
import math
import sys
from . import face  # Importa los patrones de cara

# Configuración Pygame
TARGET_WIDTH = 480
TARGET_HEIGHT = 320

# Ajuste clave: Proporción terminal (~2:1 altura/ancho)
TERMINAL_CHAR_RATIO = 2.0  # Los caracteres de terminal son ~2x más altos que anchos

# Calcular tamaño de LEDs manteniendo proporción terminal
COLS = 72  # Columnas basadas en tus patrones ASCII
LED_WIDTH = TARGET_WIDTH // COLS
LED_HEIGHT = int(LED_WIDTH * TERMINAL_CHAR_RATIO)  # Altura proporcional a terminal

# Calcular filas basadas en altura de LED
ROWS = TARGET_HEIGHT // LED_HEIGHT

# Ajustar tamaño de pantalla para que sea múltiplo exacto
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

def init_pygame():
    global screen, clock, led_matrix
    try:
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(f"LED Matrix {COLS}x{ROWS} (Ratio Terminal)")
        clock = pygame.time.Clock()
        led_matrix = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        return True
    except pygame.error as e:
        print(f"Error initializing Pygame: {e}")
        return False

def draw_led(x_pixel, y_pixel, state):
    if not screen:
        return

    border_color = DARK_ORANGE if state else DARK_GRAY
    center_color = BRIGHT_YELLOW if state else LIGHT_GRAY

    # Dibujar LED con proporción terminal
    pygame.draw.rect(screen, border_color, 
                    (x_pixel, y_pixel, LED_WIDTH, LED_HEIGHT))
    
    border_thickness = 1
    inner_rect = (
        x_pixel + border_thickness,
        y_pixel + border_thickness,
        LED_WIDTH - (2 * border_thickness),
        LED_HEIGHT - (2 * border_thickness)
    
    if inner_rect[2] > 0 and inner_rect[3] > 0:
        pygame.draw.rect(screen, center_color, inner_rect)

def update_matrix_from_patterns(eye_pattern, mouth_pattern):
    global led_matrix
    led_matrix = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    
    # Calcular offsets para centrar verticalmente
    total_pattern_height = len(eye_pattern) + len(mouth_pattern)
    if total_pattern_height > ROWS:
        # Escalar patrones si son demasiado grandes
        scale_factor = ROWS / total_pattern_height
        eye_pattern = eye_pattern[:int(len(eye_pattern)*scale_factor)]
        mouth_pattern = mouth_pattern[:int(len(mouth_pattern)*scale_factor)]
        total_pattern_height = len(eye_pattern) + len(mouth_pattern)
    
    vertical_offset = max(0, (ROWS - total_pattern_height) // 2)
    
    # Procesar ojos
    for r, line in enumerate(eye_pattern):
        draw_row = r + vertical_offset
        if 0 <= draw_row < ROWS:
            line = line.ljust(COLS)[:COLS]  # Ajustar largo de línea
            for c, char in enumerate(line):
                if char in ['O', '0']:
                    led_matrix[draw_row][c] = 1
    
    # Procesar boca
    mouth_start_row = vertical_offset + len(eye_pattern)
    for r, line in enumerate(mouth_pattern):
        draw_row = r + mouth_start_row
        if 0 <= draw_row < ROWS:
            line = line.ljust(COLS)[:COLS]  # Ajustar largo de línea
            for c, char in enumerate(line):
                if char in ['O', '0']:
                    led_matrix[draw_row][c] = 1

def draw_frame():
    if not screen:
        return
    
    screen.fill(BLACK)
    
    # Dibujar matriz LED
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
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
    
    return True

def cleanup_pygame():
    pygame.quit()