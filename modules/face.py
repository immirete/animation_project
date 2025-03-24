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
        "              OOOOOOOOOOOOOOOOOOOOOOO0000OOOOOOOOOOOOO00000000 ",   # Closed mouth
    ],
    "s_sound": [
        "             ",
        "             ",
        "             ",
        "                            _______-------_______ ",
        "              OOOOOOOOOOOOOOOOOOOOOOO0000OOOOOOOOOOOOO00000000 ",   # Closed mouth for 's' sound
        "              OOOOOOOOOOOOOOOOOOOOOOO0000OOOOOOOOOOOOO00000000 ",   # Closed mouth
        "                       OOOOOOOOOOOOOOOOOOOOOOO0000OOO ",
    ],
    "talking_1": [  # Slightly open mouth
        "             ",
        "             ",
        "             ",
        "             ",
        "              OOOOOOOOOOOOOOOOOOOOOOO0000OOOOOOOOOOOOO00000000 ", # Top part of slightly open mouth
        "              OOOOOOOOOOOOOOOOOOOOOOO0000OOOOOOOOOOOOO00000000 ", # Top part of slightly open mouth
        "              OOOOOOOOOOOOOOOOOOOOOOO0000OOOOOOOOOOOOO00000000 ", # Top part of slightly open mouth
        "              OOOOOOOOOOOOOOOOOOOOOOO0000OOOOOOOOOOOOO00000000 ",   # Bottom part of slightly open mouth
    ],
    "talking_2": [  # Fully open mouth
        "             ",
        "             ",
        "             ",
        "             ",
        "              OOOOOOOOOOOOOOOOOOOOOOO0000OOOOOOOOOOOOO00000000 ", # Top part of slightly open mouth
        "              OOOOOOOOOOOOOOOOOOOOOOO0000OOOOOOOOOOOOO00000000 ", # Top part of slightly open mouth
        "              OOOOOOOOOOOOOOOOOOOOOOO0000OOOOOOOOOOOOO00000000 ", # Top part of slightly open mouth
        "              OOOOOOOOOOOOOOOOOOOOOOO0000OOOOOOOOOOOOO00000000 ", # Top part of open mouth
        "              OOOOOOOOOOOOOOOOOOOOOOO0000OOOOOOOOOOOOO00000000 ",   # Bottom part of open mouth
        "                 OOOOOOOOOOOOOOOOOOOOOOO0000OOOOOOOOOOOOO00    ",   # Lower part of open mouth
        "                    00OOOOO0000OOOOOOOOOOOOOOOOOOOOOOO       ",   # Lowest part of open mouth
    ],
    "closed_mouth_open": [ # For closed eyes with mouth open (if needed)
        "             ",
        "             ",
        "             ",
        "             ",
        "                OOOOOOOOOOOOOOOOOOOOO0000OOOOOOOOOOOOO000000   ", # Top part of slightly open mouth
        "              OOOOOOOOOOOOOOOOOOOOOOO0000OOOOOOOOOOOOO00000000 ", # Top part of slightly open mouth
        "              OOOOOOOOOOOOOOOOOOOOOOO0000OOOOOOOOOOOOO00000000 ", # Top part of slightly open mouth
        "              OOOOOOOOOOOOOOOOOOOOOOO0000OOOOOOOOOOOOO00000000 ",   # Bottom part of slightly open mouth
    ],
}

def draw_face(stdscr, eye_pattern, mouth_pattern):
    """Draws the face on the terminal combining eye and mouth patterns."""
    stdscr.clear()
    combined_face = eye_pattern + mouth_pattern  # Combine vertically
    for i, line in enumerate(combined_face):
        stdscr.addstr(i + 5, 5, line)
    stdscr.refresh()