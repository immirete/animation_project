import openai

# Configurar clave de la API de OpenAI
openai.api_key = "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"

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