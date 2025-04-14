import os
import openai
from dotenv import load_dotenv

# Cargar variables del entorno
load_dotenv()

# Configurar la clave (versión antigua)
openai.api_key = os.getenv("OPENAI_API_KEY")  # Asegúrate de que el nombre coincide con tu .env

# Esto es solo un ejemplo, en tu código puede variar
def get_chatgpt_response(user_message):
    # Verifica que user_message sea una cadena (str) y no bytes
    if isinstance(user_message, bytes):
        user_message = user_message.decode("utf-8")

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_message}]
    )
    return response.choices[0].message["content"]