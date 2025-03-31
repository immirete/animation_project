# animation_project/modules/face.py

face_patterns_eyes = {
    "normal": [
        "             ",
        "             ",
        "             ",
        "      OOOOOOOOOOOOOOOO                               OOOOOOOOOOOOOOOO",
        "      OOOOOOOOOOOOOOOOOO                           OOOOOOOOOOOOOOOOOO",
        "      OOOOOOOOOOOOOOOOOOOO                       OOOOOOOOOOOOOOOOOOOO",
        "      OOOOOOOOOOOOOOOOOOOOOO                   OOOOOOOOOOOOOOOOOOOOOO",
        "      OOOOOOOOOOOOOOOOOOOOOO                   OOOOOOOOOOOOOOOOOOOOOO",
        "      OOOOOOOOOOOOOOOOOOOOOO                   OOOOOOOOOOOOOOOOOOOOOO",
        "             ",
        "             ",
        "             ",
    ],
    "blink": [
        "             ",
        "             ",
        "             ",
        "             ",
        "             ",
        "             ",
        "             ",
        "             ",
        "      OOOOOOOOOOOOOOOOOOOOOO                   OOOOOOOOOOOOOOOOOOOOOO  ",  # Closed eyes (blink)
        "             ",
        "             ",
        "             ",
    ],
    "happy": [
        "             ",
        "             ",
        "      OOOOOOOOOOOOOOOOOOOOOO                   OOOOOOOOOOOOOOOOOOOOOO",
        "      OOOOOOOOOOOOOOOOOOOOOO                   OOOOOOOOOOOOOOOOOOOOOO",
        "      OOOOOOOOOOOOOOOOOOOOOO                   OOOOOOOOOOOOOOOOOOOOOO",
        "      OOOOOOOOOOOOOOOOOOOOOO                   OOOOOOOOOOOOOOOOOOOOOO",
        "      OOOOOOOOOOOOOOOOOOOOOO                   OOOOOOOOOOOOOOOOOOOOOO",
        "      OOOOOOOOOOOOOOOOOOOOOO                   OOOOOOOOOOOOOOOOOOOOOO",
        "        OOOOOOOOOOOOOOOOOO                       OOOOOOOOOOOOOOOOOO",
        "          OOOOOOOOOOOOOO                           OOOOOOOOOOOOOO  ",  # Happy eyes
        "             ",
        "             ",
    ],
    "sad": [
        "             ",
        "             ",
        "              OOOOOOOOOOOOOO                   OOOOOOOOOOOOOO  ",  # SAD eyes
        "          OOOOOOOOOOOOOOOOOO                   OOOOOOOOOOOOOOOOOO",
        "      OOOOOOOOOOOOOOOOOOOOOO                   OOOOOOOOOOOOOOOOOOOOOO",
        "      OOOOOOOOOOOOOOOOOOOOOO                   OOOOOOOOOOOOOOOOOOOOOO",
        "      OOOOOOOOOOOOOOOOOOOOOO                   OOOOOOOOOOOOOOOOOOOOOO",
        "      OOOOOOOOOOOOOOOOOOOOOO                   OOOOOOOOOOOOOOOOOOOOOO",
        "      OOOOOOOOOOOOOOOOOOOOOO                   OOOOOOOOOOOOOOOOOOOOOO",
        "       OOOOOOOOOOOOOOOOOOOOO                   OOOOOOOOOOOOOOOOOOOOO ",
        "             ",
        "             ",
    ],
    "angry": [

        "           OOOO                                            OOOO",
        "         OOOOOOOO                                        OOOOOOOO",
        "        OOOOOOOOOOOOO                                OOOOOOOOOOOOO",
        "       OOOOOOOOOOOOOOOOO                           OOOOOOOOOOOOOOOOO",
        "      OOOOOOOOOOOOOOOOOOOO                       OOOOOOOOOOOOOOOOOOOO",
        "      OOOOOOOOOOOOOOOOOOOOOO                   OOOOOOOOOOOOOOOOOOOOOO",
        "      OOOOOOOOOOOOOOOOOOOOOO                   OOOOOOOOOOOOOOOOOOOOOO",
        "      OOOOOOOOOOOOOOOOOOOOOO                   OOOOOOOOOOOOOOOOOOOOOO",
        "        OOOOOOOOOOOOOOOOO                         OOOOOOOOOOOOOOOOO  ",  # Angry eyes
        "         OOOOOOOOOOOO                                OOOOOOOOOOOO    ",
        "             ",
        "             ",
    ],
    "surprised": [
        "          OOOOOOOOOOOOOO                           OOOOOOOOOOOOOO  ",  # Surprised eyes
        "        OOOOOOOOOOOOOOOOOO                       OOOOOOOOOOOOOOOOOO",
        "      OOOOOOOOOOOOOOOOOOOOOO                   OOOOOOOOOOOOOOOOOOOOOO",
        "      OOOOOOOOOOOOOOOOOOOOOO                   OOOOOOOOOOOOOOOOOOOOOO",
        "      OOOOOOOOOOOOOOOOOOOOOO                   OOOOOOOOOOOOOOOOOOOOOO",
        "      OOOOOOOOOOOOOOOOOOOOOO                   OOOOOOOOOOOOOOOOOOOOOO",
        "      OOOOOOOOOOOOOOOOOOOOOO                   OOOOOOOOOOOOOOOOOOOOOO",
        "      OOOOOOOOOOOOOOOOOOOOOO                   OOOOOOOOOOOOOOOOOOOOOO",
        "        OOOOOOOOOOOOOOOOOO                       OOOOOOOOOOOOOOOOOO",
        "          OOOOOOOOOOOOOO                           OOOOOOOOOOOOOO  ",  # Surprised eyes
        "             ",
        "             ",
    ],
    "closed_mouth_open": [ # For closed eyes with mouth open (if needed)
        "             ",
        "             ",
        "             ",
        "             ",
        "             ",
        "             ",
        "             ",
        "             ",
        "      OOOOOOOOOOOOOOOOOOOOOO                   OOOOOOOOOOOOOOOOOOOOOO  ",  # Closed eyes (blink)
        "             ",
        "             ",
        "             ",
    ],
}

face_patterns_mouth = {
    "normal": [
        "             ",
        "             ",
        "             ",
        "             ",
        "             ",
        "              OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO ",
        "             ",
        "             ",
        "             ",
        "             ",
        "             ",

    ],
    "s_sound": [ # Corregido nombre 'sOsound' a 's_sound'
        "             ",
        "             ",
        "             ",
        "                                OOOOOOOOOOOOO                  ",
        "              OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO ",
        "              OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO ",
        "                          OOOOOOOOOOOOOOOOOOOOOOOO    ",
        "             ",
        "             ",
        "             ",
        "             ",

    ],
    "talking_1": [ # Corregido nombre 'talkingO1' a 'talking_1'
        "             ",
        "             ",
        "             ",
        "              OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO ",
        "              OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO ",
        "              OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO ",
        "              OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO ",
        "             ",
        "             ",
        "             ",
        "             ",

    ],
    "talking_2": [ # Corregido nombre 'talkingO2' a 'talking_2'
        "             ",
        "             ",
        "             ",
        "             ",
        "              OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO ",
        "              OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO ",
        "              OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO ",
        "              OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO ",
        "              OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO ",
        "                 OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO    ",
        "                    OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO       ",
    ],
    "closed_mouth_open": [ # Corregido nombre 'closedOmouthOopen' a 'closed_mouth_open'
         # Este patrón parece más una boca abierta que una cerrada
         # Lo mantendré como está pero considera si el nombre es correcto
        "             ",
        "             ",
        "             ",
        "             ",
        "                OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO   ",
        "              OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO ",
        "              OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO ",
        "              OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO ", # Bottom part of slightly open mouth
        "             ",
        "             ",
        "             ",
    ],
}

def draw_face(stdscr, eye_pattern, mouth_pattern):
    """Draws the face on the terminal combining eye and mouth patterns."""
    stdscr.clear()
    combined_face = eye_pattern + mouth_pattern  # Combine vertically
    for i, line in enumerate(combined_face):
        stdscr.addstr(i + 5, 5, line)
    stdscr.refresh()