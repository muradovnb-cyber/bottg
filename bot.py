import os
import logging
from anthropic import Anthropic
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# --- Настройки ---
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "ВАШ_TELEGRAM_TOKEN")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "ВАШ_ANTHROPIC_KEY")

# Опционально: разрешить только определённые Telegram ID
# ALLOWED_USER_IDS = {123456789}  # Раскомментировать и добавить свой ID

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

client = Anthropic(api_key=ANTHROPIC_API_KEY)

# Храним историю переписки для каждого пользователя
conversation_history: dict[int, list] = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я Claude — AI-ассистент от Anthropic.\n"
        "Просто напиши мне что-нибудь, и я отвечу.\n\n"
        "Команды:\n"
        "/start — это сообщение\n"
        "/clear — очистить историю диалога\n"
        "/help — помощь"
    )


async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    conversation_history.pop(user_id, None)
    await update.message.reply_text("История диалога очищена. Начинаем заново!")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Просто отправь мне любое текстовое сообщение — я отвечу как Claude.\n"
        "Я помню контекст нашего разговора (до 20 последних сообщений).\n\n"
        "/clear — сбросить контекст разговора"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_text = update.message.text

    # Опциональная проверка доступа
    # if user_id not in ALLOWED_USER_IDS:
    #     await update.message.reply_text("Доступ запрещён.")
    #     return

    # Инициализируем историю если нет
    if user_id not in conversation_history:
        conversation_history[user_id] = []

    # Добавляем сообщение пользователя
    conversation_history[user_id].append({
        "role": "user",
        "content": user_text,
    })

    # Ограничиваем историю последними 20 сообщениями
    if len(conversation_history[user_id]) > 20:
        conversation_history[user_id] = conversation_history[user_id][-20:]

    # Показываем индикатор набора
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action="typing"
    )

    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2048,
            system="Ты полезный ассистент Claude. Отвечай на языке пользователя.",
            messages=conversation_history[user_id],
        )

        assistant_reply = response.content[0].text

        # Сохраняем ответ в историю
        conversation_history[user_id].append({
            "role": "assistant",
            "content": assistant_reply,
        })

        # Telegram ограничивает сообщения до 4096 символов
        if len(assistant_reply) > 4096:
            for i in range(0, len(assistant_reply), 4096):
                await update.message.reply_text(assistant_reply[i:i+4096])
        else:
            await update.message.reply_text(assistant_reply)

    except Exception as e:
        logging.error(f"Ошибка API: {e}")
        await update.message.reply_text(
            f"Произошла ошибка при обращении к Claude. Попробуй ещё раз.\n({e})"
        )


def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("clear", clear))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logging.info("Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()
