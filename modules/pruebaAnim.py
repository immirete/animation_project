import pygame
import sys
import time
from pygame.locals import *

# Inicialización de Pygame
pygame.init()

# Configuración de pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Demo Animación Facial LED")
clock = pygame.time.Clock()

# Colores
BLACK = (0, 0, 0)
DARK_RED = (80, 20, 20)    # Borde rojo oscuro
ORANGE = (200, 100, 0)     # Color principal del LED
BRIGHT_YELLOW = (255, 200, 50)  # Punto de luz

# Tamaño de cada LED
LED_SIZE = 8

# Patrones de ojos (17x11 LEDs)
eye_patterns = {
    "normal": [
        "     000000000000000     ",
        "   00000000000000000    ",
        "  0000000000000000000   ",
        " 000000000000000000000  ",
        " 000000000000000000000  ",
        " 000000000000000000000  ",
        " 000000000000000000000  ",
        " 000000000000000000000  ",
        "  0000000000000000000   ",
        "   00000000000000000    ",
        "     000000000000000     "
    ],
    "happy": [
        "                 ",
        " 000000000000000 ",
        " 000000000000000 ",
        " 000000000000000 ",
        " 000000000000000 ",
        " 000000000000000 ",
        "  0000000000000  ",
        "   00000000000   ",
        "    000000000    ",
        "     0000000     ",
        "      00000      "
    ],
    "angry": [
        " 00           00 ",
        "  000       000  ",
        "   0000   0000   ",
        "    000000000    ",
        "     0000000     ",
        "      00000      ",
        "     0000000     ",
        "    000000000    ",
        "   0000   0000   ",
        "  000       000  ",
        " 00           00 "
    ],
    "surprised": [
        "     0000000     ",
        "   00000000000   ",
        "  0000000000000  ",
        " 000000000000000 ",
        " 000000000000000 ",
        " 000000000000000 ",
        " 000000000000000 ",
        " 000000000000000 ",
        "  0000000000000  ",
        "   00000000000   ",
        "     0000000     "
    ],
    "blink": [
        "                 ",
        "                 ",
        "                 ",
        "                 ",
        "                 ",
        " 000000000000000 ",
        " 000000000000000 ",
        "                 ",
        "                 ",
        "                 ",
        "                 "
    ]
}

# Patrones de boca (37x10 LEDs)
mouth_patterns = {
    "normal": [
        "                                     ",
        "                                     ",
        "                                     ",
        "      0000000000000000000000000000000",
        "      0000000000000000000000000000000",
        "                                     ",
        "                                     ",
        "                                     ",
        "                                     ",
        "                                     "
    ],
    "happy": [
        "                                     ",
        "                                     ",
        "      0000000000000000000000000      ",
        "    00000000000000000000000000000    ",
        "  000000000000000000000000000000000  ",
        "   0000000000000000000000000000000   ",
        "     000000000000000000000000000     ",
        "       00000000000000000000000       ",
        "         0000000000000000000         ",
        "           0000000000000            "
    ],
    "open": [
        "                                     ",
        "      0000000000000000000000000      ",
        "    00000000000000000000000000000    ",
        "  000000000000000000000000000000000  ",
        "  000000000000000000000000000000000  ",
        "  000000000000000000000000000000000  ",
        "  000000000000000000000000000000000  ",
        "   0000000000000000000000000000000   ",
        "     000000000000000000000000000     ",
        "       00000000000000000000000       "
    ],
    "s_sound": [
        "                                     ",
        "                                     ",
        "           0000000000000             ",
        "        0000000000000000000          ",
        "      0000000000000000000000000       ",
        "     000000000000000000000000000      ",
        "       00000000000000000000000        ",
        "         0000000000000000000          ",
        "           0000000000000             ",
        "                                     "
    ],
    "talking1": [
        "                                     ",
        "                                     ",
        "      0000000000000000000000000      ",
        "    00000000000000000000000000000    ",
        "   0000000000000000000000000000000   ",
        "   0000000000000000000000000000000   ",
        "    00000000000000000000000000000    ",
        "      0000000000000000000000000      ",
        "                                     ",
        "                                     "
    ],
    "talking2": [
        "                                     ",
        "      0000000000000000000000000      ",
        "    00000000000000000000000000000    ",
        "   0000000000000000000000000000000   ",
        "  000000000000000000000000000000000  ",
        "  000000000000000000000000000000000  ",
        "   0000000000000000000000000000000   ",
        "    00000000000000000000000000000    ",
        "      0000000000000000000000000      ",
        "                                     "
    ]
}

def draw_led_pattern(surface, pattern, x_offset, y_offset):
    """Dibuja un patrón en la superficie dada"""
    for y, row in enumerate(pattern):
        for x, char in enumerate(row):
            if char == '0':
                # Coordenadas del LED
                led_x = x_offset + x * LED_SIZE
                led_y = y_offset + y * LED_SIZE
                
                # Dibujar borde rojo oscuro
                pygame.draw.rect(surface, DARK_RED, (led_x, led_y, LED_SIZE, LED_SIZE))
                
                # Dibujar centro naranja
                pygame.draw.rect(surface, ORANGE, 
                               (led_x + 1, led_y + 1, LED_SIZE - 2, LED_SIZE - 2))
                
                # Punto de luz amarillo
                pygame.draw.circle(surface, BRIGHT_YELLOW,
                                 (led_x + LED_SIZE // 2, led_y + LED_SIZE // 3),
                                 LED_SIZE // 4)

def render_face(eye_type, mouth_type):
    """Renderiza toda la cara en la pantalla"""
    screen.fill(BLACK)  # Corregido: Cambiado de BACK a BLACK
    
    # Calcular posición central
    center_x = WIDTH // 2
    center_y = HEIGHT // 3
    
    # Obtener patrones
    eye_pattern = eye_patterns.get(eye_type, eye_patterns["normal"])
    mouth_pattern = mouth_patterns.get(mouth_type, mouth_patterns["normal"])
    
    # Dibujar ojos (separados)
    eye_width = len(eye_pattern[0]) * LED_SIZE if eye_pattern else 0
    eye_height = len(eye_pattern) * LED_SIZE if eye_pattern else 0
    
    left_eye_x = center_x - eye_width - 50
    right_eye_x = center_x + 50
    
    draw_led_pattern(screen, eye_pattern, left_eye_x, center_y)
    draw_led_pattern(screen, eye_pattern, right_eye_x, center_y)
    
    # Dibujar boca
    mouth_x = center_x - (len(mouth_pattern[0]) * LED_SIZE) // 2 if mouth_pattern else 0
    mouth_y = center_y + eye_height + 20
    
    draw_led_pattern(screen, mouth_pattern, mouth_x, mouth_y)
    
    # Mostrar información
    font = pygame.font.SysFont('Arial', 20)
    info_text = f"Ojos: {eye_type} | Boca: {mouth_type} | LED Size: {LED_SIZE}px"
    text_surface = font.render(info_text, True, (255, 255, 255))
    screen.blit(text_surface, (10, HEIGHT - 30))
    
    pygame.display.flip()

# Estados de animación
animations = [
    # (Ojos, Boca, Duración)
    ("normal", "normal", 1.0),
    ("happy", "happy", 2.0),
    ("blink", "normal", 0.2),
    ("normal", "talking1", 0.1),
    ("normal", "talking2", 0.1),
    ("normal", "talking1", 0.1),
    ("normal", "talking2", 0.1),
    ("surprised", "open", 1.5),
    ("angry", "open", 1.5),
    ("blink", "normal", 0.2)
]

# Bucle principal
current_anim = 0
start_time = time.time()
running = True

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_UP:
                LED_SIZE = min(20, LED_SIZE + 1)  # Aumentar tamaño LED
            elif event.key == K_DOWN:
                LED_SIZE = max(4, LED_SIZE - 1)  # Disminuir tamaño LED
    
    # Control de animación
    elapsed = time.time() - start_time
    anim_data = animations[current_anim]
    
    if elapsed >= anim_data[2]:
        current_anim = (current_anim + 1) % len(animations)
        start_time = time.time()
    
    # Renderizar cara actual
    render_face(anim_data[0], anim_data[1])
    
    clock.tick(60)

pygame.quit()
sys.exit()