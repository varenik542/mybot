import logging
import requests
import json
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = "8326987381:AAFBeDQ_aSDwXn3fON_L557XuRH8IoV7Ia8"
OPENROUTER_API_KEY = "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"
SYSTEM_PROMPT = "Ты — агрессивный матершинник с юмором. Отвечай с матами и подколами."

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

def ask_deepseek(user_message):
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek/deepseek-chat",
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_message}
                ]
            },
            timeout=30
        )
        # Добавляем проверку ответа
        if response.status_code == 200:
            data = response.json()
            if "choices" in data and len(data["choices"]) > 0:
                return data["choices"][0]["message"]["content"]
            else:
                return f"Ошибка: Неверный формат ответа API - {data}"
        else:
            return f"Ошибка API: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Ошибка: {str(e)}"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(ask_deepseek(update.message.text))

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    print("Бот запущен (исправленная версия)!")
    app.run_polling()

if __name__ == "__main__":
    main()
