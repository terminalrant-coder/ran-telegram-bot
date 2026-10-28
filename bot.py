import os
from fastapi import FastAPI
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

app = FastAPI()

# Leer el token de las variables de entorno de Render
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Inicializar el bot de Telegram
telegram_app = Application.builder().token(TOKEN).build()

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Qué tal! $RANT bot está activo y listo en la terminal. 🚀")

# Manejador de mensajes de texto normales
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto_usuario = update.message.text
    # Aquí puedes personalizar la respuesta que quieras que dé el bot
    await update.message.reply_text(f"Recibí tu mensaje: '{texto_usuario}'. ¡Seguimos activos!")

# Registrar los manejadores en Telegram
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Rutas web obligatorias para Render (Health Check)
@app.get("/")
@app.get("/healthz")
def health_check():
    return {"status": "RANT bot is online!"}

# Iniciar el bot de Telegram en segundo plano cuando arranca FastAPI
@app.on_event("startup")
async def startup_event():
    if TOKEN:
        await telegram_app.initialize()
        await telegram_app.start()
        await telegram_app.updater.start_polling()

# Detener el bot de manera limpia al apagar
@app.on_event("shutdown")
async def shutdown_event():
    if TOKEN:
        await telegram_app.updater.stop()
        await telegram_app.stop()
        await telegram_app.shutdown()
