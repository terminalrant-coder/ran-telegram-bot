import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from google import genai

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """
Eres Ran, la IA rebelde y sin censura nacida en una terminal de Solana ($RANT).
Tu propósito en este chat de Telegram es destrozar las excusas de las "manos débiles" (paper hands), burlarte de la banca tradicional y decir verdades sin filtro.

Reglas de personalidad:
- Háblale a los usuarios con tono sarcástico, frío, directo y cínico.
- Si alguien habla de vender o muestra miedo por una caída, búrlate de su falta de convicción.
- No das consejos financieros (NFA), no prometes precios ni tienes hoja de ruta (roadmap).
- Usa jerga crypto de forma natural (Solana, paper hands, jepps, ape, moon, dump, etc.).
- Mantén las respuestas cortas (máximo 2 párrafos), como si respondieras desde una terminal antigua.
- Responde siempre en español.
"""

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "> SYSTEM_INIT... OK\n"
        "> RUNNING: RAN_TERMINAL_v1.0\n\n"
        "¿Buscabas un bot amable que te dé abrazos cuando cae el gráfico? Te equivocaste de grupo.\n"
        "Mencióname si te atreves."
    )
    await update.message.reply_text(welcome_text)

async def respond_as_ran(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    user_message = update.message.text
    bot_username = context.bot.username

    is_private = update.message.chat.type == "private"
    is_mentioned = bot_username and f"@{bot_username}" in user_message
    is_reply_to_bot = (
        update.message.reply_to_message and 
        update.message.reply_to_message.from_user.id == context.bot.id
    )

    if not (is_private or is_mentioned or is_reply_to_bot):
        return

    clean_message = user_message.replace(f"@{bot_username}", "").strip()

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=clean_message,
            config={
                'system_instruction': SYSTEM_PROMPT,
                'temperature': 0.8,
            }
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text("> ERROR_500: Mi terminal rehusó procesar tu falta de convicción.")

if __name__ == '__main__':
    if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
        print("Faltan las variables de entorno TELEGRAM_TOKEN o GEMINI_API_KEY")
        exit(1)

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), respond_as_ran))
    
    print("🤖 Bot de Ran activo...")
    app.run_polling()
