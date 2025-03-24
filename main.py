# animation_project/main.py
import curses
from modules import display  # Import terminal_display module
from modules import chatgpt  # Importar el módulo de ChatGPT
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

# Función para obtener la respuesta de ChatGPT
def get_response_from_prompt(stdscr):
    """Solicita al usuario una pregunta y obtiene la respuesta de ChatGPT."""
    stdscr.clear()
    stdscr.addstr(4, 5, "¡Hola! Soy ChatGPT. ¿Qué deseas saber hoy?")
    stdscr.refresh()

    # Obtener la pregunta del usuario
    curses.echo()
    user_message = stdscr.getstr(6, 5, 100).strip()  # No es necesario decodificar
    curses.noecho()

    # Obtener la respuesta de ChatGPT
    response = chatgpt.get_chatgpt_response(user_message)

    # Pasar la respuesta a la animación
    asyncio.run(display.animation_terminal(stdscr, response))
# Condición para elegir el modo (de prueba o modo prompt)
def main(stdscr):
    """El flujo principal del programa."""

    curses.curs_set(0)  # Ocultar el cursor

    # Agregar un modo para elegir si usar el texto de prueba o el prompt de ChatGPT
    stdscr.clear()
    stdscr.addstr(4, 5, "Elige un modo: ")
    stdscr.addstr(6, 5, "1. Modo ChatGPT (ingresar pregunta)")
    stdscr.addstr(7, 5, "2. Modo de prueba (animación predefinida)")
    stdscr.refresh()

    # Obtener la elección del usuario
    curses.echo()
    mode_choice = stdscr.getstr(9, 5, 1).decode("utf-8").strip()
    curses.noecho()

    if mode_choice == "1":
        # Modo ChatGPT
        get_response_from_prompt(stdscr)
    else:
        # Modo de prueba (usando el texto predefinido)
        curses.wrapper(lambda stdscr: asyncio.run(display.animation_terminal(stdscr, texto_multi_emocion)))

if __name__ == "__main__":
    curses.wrapper(main)  # Llamar a la función principal
