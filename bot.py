"""
Bot de Telegram - FAQ automático para negocios
Proyecto de portfolio - responde preguntas frecuentes 24/7

Cómo usarlo:
1. Instala las dependencias: pip install python-telegram-bot --break-system-packages
2. Reemplaza "TU_TOKEN_AQUI" con el token que te da @BotFather en Telegram
3. Edita el diccionario RESPUESTAS con la info de tu negocio (o del negocio de tu cliente)
4. Corre el bot: python bot.py
5. Busca tu bot en Telegram y mándale /start
"""

import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ==========================================
# CONFIGURACIÓN - Edita esto para cada cliente
# ==========================================

# El token se lee de una "variable de entorno" (más seguro, y así funciona en Railway)
# Para probar en tu compu, puedes poner el token directo aquí como texto entre comillas
TOKEN = os.environ.get("BOT_TOKEN", "8604035868:AAGsPKc5Xsrxpxh5tChUfi8VL_RE9HrDzNA")

NOMBRE_NEGOCIO = "Mi Negocio"

RESPUESTAS = {
    "horarios": "🕐 Nuestro horario es de Lunes a Sábado, 9:00 AM a 8:00 PM.",
    "ubicación": "📍 Estamos en [Dirección aquí]. Ver en mapa: [link de Google Maps]",
    "precios": "💰 Nuestros precios varían según el servicio. Escríbenos qué te interesa y te cotizamos.",
    "contacto": "📞 Puedes escribirnos aquí mismo o llamarnos al [número de teléfono].",
}

MENU_PRINCIPAL = [
    ["🕐 Horarios", "📍 Ubicación"],
    ["💰 Precios", "📞 Contacto"],
]

# ==========================================
# LÓGICA DEL BOT
# ==========================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Se ejecuta cuando el usuario manda /start"""
    mensaje_bienvenida = (
        f"¡Hola! 👋 Bienvenido a *{NOMBRE_NEGOCIO}*.\n\n"
        "Soy tu asistente automático, puedo ayudarte con:\n"
        "🕐 Horarios de atención\n"
        "📍 Ubicación\n"
        "💰 Precios\n"
        "📞 Contacto\n\n"
        "Elige una opción del menú de abajo 👇"
    )
    teclado = ReplyKeyboardMarkup(MENU_PRINCIPAL, resize_keyboard=True)
    await update.message.reply_text(mensaje_bienvenida, reply_markup=teclado, parse_mode="Markdown")


async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Responde según el texto que mande el usuario"""
    texto_usuario = update.message.text.lower()

    if "horario" in texto_usuario:
        respuesta = RESPUESTAS["horarios"]
    elif "ubicaci" in texto_usuario or "dirección" in texto_usuario or "direccion" in texto_usuario:
        respuesta = RESPUESTAS["ubicación"]
    elif "precio" in texto_usuario or "costo" in texto_usuario or "cuánto" in texto_usuario:
        respuesta = RESPUESTAS["precios"]
    elif "contacto" in texto_usuario or "teléfono" in texto_usuario or "telefono" in texto_usuario:
        respuesta = RESPUESTAS["contacto"]
    else:
        respuesta = (
            "No entendí tu pregunta 🤔. Usa el menú de abajo o escribe /start para ver las opciones."
        )

    await update.message.reply_text(respuesta)


def main():
    if TOKEN == "TU_TOKEN_AQUI":
        print("⚠️  ERROR: Debes reemplazar TU_TOKEN_AQUI con tu token real de @BotFather")
        return

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

    print(f"🤖 Bot de {NOMBRE_NEGOCIO} corriendo... (Ctrl+C para detener)")
    app.run_polling()


if __name__ == "__main__":
    main()
