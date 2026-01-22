# para rodar o bot:
# & "C:\Users\User\Desktop\envio de email\.venv\Scripts\python.exe" .\main.py

import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from bot_email import enviar_email 

# ================= CONFIGURAÇÕES =================
EMAIL_ORIGEM = 'pvinicius768@gmail.com'  
SENHA_EMAIL = 'mlql crdc jzlf cdqa'             
EMAIL_DESTINO = 'philype20@hotmail.com' 
TELEGRAM_TOKEN = '8443841482:AAH-E4Xc63FJ_vBBZaLLEvgXp_F9Crm3H9E'
PALAVRA_CHAVE = "#movi"
# =================================================

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📧 Envio de e-mail\n\n"
        "O e-mail só será enviado se a mensagem contiver a palavra:\n"
        f"➡️ {PALAVRA_CHAVE}"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto_original = update.message.text
    texto = texto_original.lower()

    # NÃO contém a palavra-chave
    if PALAVRA_CHAVE not in texto:
        await update.message.reply_text(
            "❌ E-mail NÃO enviado.\n"
            f"A mensagem precisa conter: {PALAVRA_CHAVE}"
        )
        return

    # Contém a palavra-chave → envia o e-mail
    enviar_email(
        texto_original,
        EMAIL_ORIGEM,
        SENHA_EMAIL,
        EMAIL_DESTINO
    )

    await update.message.reply_text("✅ E-mail enviado com sucesso!")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
