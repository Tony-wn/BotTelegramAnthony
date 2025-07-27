import logging
import requests
import json
import os
import azure.functions as func

#Cargar variables
TELEGRAM_TOKEN = os.getenv('8486169769:AAH6_cqWB-Ocf76RkdtT47Xwn4j3sXex4pQ')
AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')

#Telegram API URL
TELEGRAM_API_URL = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
        message_text = body["message"]["text"]
        chat_id = body["message"]["chat"]["id"]

        # Llamar a Azure OpenAI
        response_text = ask_openai(message_text)

        # Responder en Telegram
        telegram_payload = {
            "chat_id": chat_id,
            "text": response_text
        }
        requests.post(TELEGRAM_API_URL, json=telegram_payload)

        return func.HttpResponse("OK", status_code=200)

    except Exception as e:
        logging.error(f"Error: {e}")
        return func.HttpResponse("Error", status_code=500)

def ask_openai(question):
    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_OPENAI_API_KEY
    }

    data = {
        "messages": [
            {"role": "system", "content": "Eres un asistente educativo que responde preguntas con claridad."},
            {"role": "user", "content": question}
        ],
        "temperature": 0.7,
        "max_tokens": 300
    }

    endpoint = f"{AZURE_OPENAI_ENDPOINT}/openai/deployments/tu-modelo/chat/completions?api-version=2024-02-15"
    
    response = requests.post(endpoint, headers=headers, json=data)
    result = response.json()

    return result["choices"][0]["message"]["content"]
