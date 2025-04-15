# animation_project/main.py

import curses
from modules import display
from modules import chatgpt
import asyncio
from modules import transcription_module # Importa el nuevo módulo


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

def get_response_from_transcription(stdscr, display_mode):
    """Obtiene texto transcrito, consulta a ChatGPT y muestra animación"""
    stdscr.clear()
    stdscr.addstr(4, 5, "Preparando para transcribir...")
    stdscr.addstr(6, 5, "La ventana de video se abrirá.")
    stdscr.addstr(7, 5, "Mira a la cámara y habla.")
    stdscr.addstr(8, 5, "Cuando desvíes la mirada, se procesará tu voz.")
    stdscr.addstr(9, 5, "(Presiona 'q' en la ventana de video para cancelar)")
    stdscr.refresh()

    # --- Importante: Salir del modo curses temporalmente ---
    # curses y cv2.imshow/waitKey no se llevan bien siempre.
    # Es mejor cerrar curses, ejecutar la transcripción (que usa cv2),
    # y luego reiniciar curses si es necesario, o simplemente mostrar el resultado final.
    curses.endwin() # Termina curses temporalmente

    print("\n" + "="*30)
    print(" Iniciando Módulo de Transcripción ")
    print("="*30 + "\n")

    transcribed_text = None
    try:
        # Llama a la función del módulo de transcripción
        transcribed_text = transcription_module.start_transcription_and_get_text()
    except Exception as e:
         print(f"\n[ERROR] Ocurrió un error al ejecutar el módulo de transcripción: {e}\n")
         # Podrías querer esperar antes de volver a curses
         input("Presiona Enter para volver al menú...")


    # ---- INICIO DE LA PARTE QUE TE FALTA ----

    # 4. Definir una función interna para manejar los resultados DENTRO de un nuevo curses
    def show_result_in_curses(stdscr_new):
        """Esta función se ejecuta dentro de un nuevo wrapper de curses."""
        curses.curs_set(0) # Ocultar cursor
        stdscr_new.clear()

        # 5. Verificar si se obtuvo texto
        if transcribed_text:
            stdscr_new.addstr(4, 5, f"Texto transcrito: {transcribed_text[:80]}{'...' if len(transcribed_text)>80 else ''}") # Muestra parte del texto
            stdscr_new.addstr(6, 5, "Enviando a ChatGPT...")
            stdscr_new.refresh()

            # 6. Intentar obtener respuesta de ChatGPT
            try:
                response = chatgpt.get_chatgpt_response(transcribed_text)
                # Limpiar "Enviando..." antes de la animación
                stdscr_new.clear()
                stdscr_new.refresh()

                # 7. Ejecutar la animación con la RESPUESTA de ChatGPT
                if display_mode == 'terminal':
                     # Pasar el nuevo stdscr_new a la animación de terminal
                     # Asegúrate que run_terminal_animation pueda manejar esto
                     asyncio.run(run_terminal_animation(stdscr_new, response))
                     # La animación terminal ya usa curses, podría no necesitar pausa adicional
                     # Pero añadimos una por consistencia, por si la animación no espera
                     stdscr_new.addstr(stdscr_new.getmaxyx()[0] - 2, 5, "Animación completada. Presiona una tecla...")
                     stdscr_new.getch()
                else: # 'matrix'
                     # Matrix se ejecuta (simulada) fuera de curses directamente
                     asyncio.run(run_matrix_animation(response))
                     # Mostrar mensaje de finalización en la ventana de curses
                     stdscr_new.clear()
                     stdscr_new.addstr(5, 5, "Animación Matrix completada (simulada).")
                     stdscr_new.addstr(7, 5, "Presiona una tecla para volver al menú.")
                     stdscr_new.getch() # Esperar tecla

            except Exception as e:
                # 8. Manejar errores de ChatGPT
                stdscr_new.clear()
                stdscr_new.addstr(5, 5, f"Error al obtener respuesta de ChatGPT: {e}")
                stdscr_new.addstr(7, 5, "Presiona una tecla para continuar.")
                stdscr_new.getch() # Esperar tecla
        else:
            # 9. Si no hubo texto transcrito
            stdscr_new.addstr(4, 5, "No se obtuvo texto transcrito o se canceló.")
            stdscr_new.addstr(6, 5, "Presiona una tecla para volver al menú.")
            stdscr_new.getch() # Esperar tecla

    # 10. Ejecutar la función de resultados dentro de curses.wrapper
    # Esto reinicia curses de forma segura para mostrar los resultados
    curses.wrapper(show_result_in_curses)

    # ---- FIN DE LA PARTE QUE TE FALTA ----

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
    stdscr.addstr(8, 5, "3. Modo Transcripción + ChatGPT (hablar)") # Nueva opción
    stdscr.addstr(10, 5, "q. Salir")
    stdscr.refresh()

    curses.echo()
    mode_choice = stdscr.getch()
    curses.noecho()

    if chr(mode_choice) == '1':
        get_response_from_prompt(stdscr, display_mode)
    elif mode_choice == ord('2'):
            stdscr.clear()
            stdscr.addstr(4, 5, "Ejecutando animación de prueba...")
            stdscr.refresh()
            # Usar el texto de prueba mult Emoción
            texto_prueba = texto_multi_emocion
            if display_mode == 'terminal':
                 # Llamamos directamente a la función async dentro de asyncio.run
                 # Necesitamos pasar el stdscr actual
                 asyncio.run(run_terminal_animation(stdscr, texto_prueba))
            else:
                 asyncio.run(run_matrix_animation(texto_prueba))
                 # Añadir mensaje de finalización para el modo matrix en curses
                 stdscr.clear()
                 stdscr.addstr(5,5, "Animación Matrix de prueba completada (simulada).")
                 stdscr.addstr(7,5, "Presiona una tecla para volver al menú.")
                 stdscr.getch()
    elif mode_choice == ord('3'):
            # Llama a la función que maneja la transcripción y la llamada a ChatGPT
            get_response_from_transcription(stdscr, display_mode)
            # Después de que get_response_from_transcription termine (y su wrapper de curses interno),
            # el bucle while hará que se muestre el menú de nuevo.

    else:
            stdscr.addstr(12, 5, "Opción inválida. Inténtalo de nuevo.")
            stdscr.refresh()
            curses.napms(1000) # Pausa de 1 segundo


def main(stdscr):
    """Función principal"""
    curses.curs_set(0)
    display_mode = choose_display_mode(stdscr)
    choose_operation_mode(stdscr, display_mode)

if __name__ == "__main__":
    curses.wrapper(main)