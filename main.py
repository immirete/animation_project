# animation_project/main.py

import curses
from modules import display
from modules import chatgpt
import asyncio


# Test texts
positive_text = "I'm very happy to talk to you today."
negative_text = "Today I feel very sad and discouraged."
neutral_text = "Today is a normal day Sia."
surprise_text = "Incredible! I wasn't expecting that."
sad_text = "I am very sad, this is not working as expected"
angry_text = "This application is rubbish"

# Texto para prueba
texto_positivo = "Estoy muy feliz de hablar contigo hoy."
texto_negativo = "Hoy me siento muy triste y desanimado."
texto_neutral = "Hoy es un día normal Sia."
texto_sorpresa = "¡Increíble! No me lo esperaba."
texto_triste= "Estoy muy triste, esto no funciona como esperaba"
texto_enfadado="Esta aplicación es una mierda"
texto_multi_emocion = "¡Qué día tan maravilloso hace hoy! El sol brilla y me siento muy feliz.  Pero, de repente, recuerdo que perdí mis llaves. ¡Qué fastidio! Ahora estoy un poco triste.  Después, intentando buscarlas, me tropiezo y me golpeo el pie. ¡Aggg, qué rabia! ¡Estoy muy enfadado!  Sin embargo, al levantar la vista, ¡sorpresa! ¡Encuentro las llaves justo delante de mí! ¡Increíble! ¡Estoy muy sorprendido y aliviado! Al final, todo salió bien.  Bueno, así es la vida, a veces normal, a veces emocionante."

async def run_terminal_animation(stdscr, text):
    """Ejecuta la animación en modo terminal"""
    display_manager = display.DisplayManager('terminal')
    await display_manager.animation_terminal(stdscr, text)

async def run_matrix_animation(text):
    """Ejecuta la animación en modo matriz"""
    display_manager = display.DisplayManager('matrix')
    await display_manager.animation_terminal(None, text)  # Pasamos None para stdscr

def get_response_from_prompt(stdscr, display_mode):
    """Obtiene respuesta de ChatGPT y muestra animación"""
    stdscr.clear()
    stdscr.addstr(4, 5, "¡Hola! Soy ChatGPT. ¿Qué deseas saber hoy?")
    stdscr.refresh()

    curses.echo()
    user_message = stdscr.getstr(6, 5, 100).decode("utf-8").strip()
    curses.noecho()

    response = chatgpt.get_chatgpt_response(user_message)
    
    if display_mode == 'terminal':
        curses.wrapper(lambda stdscr: asyncio.run(run_terminal_animation(stdscr, response)))
    else:
        asyncio.run(run_matrix_animation(response))

def choose_display_mode(stdscr):
    """Permite al usuario elegir el modo de visualización"""
    stdscr.clear()
    stdscr.addstr(4, 5, "Elige modo de visualización:")
    stdscr.addstr(6, 5, "1. Terminal (curses)")
    stdscr.addstr(7, 5, "2. Matriz LED (simulada)")
    stdscr.refresh()
    
    curses.echo()
    display_choice = stdscr.getch()
    curses.noecho()
    
    return 'terminal' if chr(display_choice) == '1' else 'matrix'

def choose_operation_mode(stdscr, display_mode):
    """Permite al usuario elegir el modo de operación"""
    stdscr.clear()
    stdscr.addstr(4, 5, "Elige un modo de operación:")
    stdscr.addstr(6, 5, "1. Modo ChatGPT (ingresar pregunta)")
    stdscr.addstr(7, 5, "2. Modo de prueba (animación predefinida)")
    stdscr.refresh()

    curses.echo()
    mode_choice = stdscr.getch()
    curses.noecho()

    if chr(mode_choice) == '1':
        get_response_from_prompt(stdscr, display_mode)
    else:
        if display_mode == 'terminal':
            curses.wrapper(lambda stdscr: asyncio.run(run_terminal_animation(stdscr, texto_multi_emocion)))
        else:
            asyncio.run(run_matrix_animation(texto_multi_emocion))

def main(stdscr):
    """Función principal"""
    curses.curs_set(0)
    display_mode = choose_display_mode(stdscr)
    choose_operation_mode(stdscr, display_mode)

if __name__ == "__main__":
    curses.wrapper(main)