import telebot
import os
import time
import threading

# Configurar bot
TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)

# Função para manter o bot ativo
def keep_alive():
    print("Bot Telegram está rodando...")

# Comandos do bot
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 
                "🤖 Olá! Eu sou um bot rodando no Render!\n"
                "Digite /help para ver os comandos disponíveis.")

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.reply_to(message, 
                "📋 Comandos disponíveis:\n"
                "/start - Iniciar conversa\n"
                "/help - Mostrar ajuda\n"
                "/status - Status do bot\n"
                "/ping - Testar conexão")

@bot.message_handler(commands=['status'])
def status(message):
    bot.reply_to(message, "✅ Bot funcionando perfeitamente no Render!")

@bot.message_handler(commands=['ping'])
def ping(message):
    bot.reply_to(message, "🏓 Pong! Bot está online.")

# Responder mensagens normais
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"Você disse: {message.text}")

# Iniciar bot
if __name__ == "__main__":
    print("🚀 Iniciando bot Telegram...")
    # Manter ativo
    threading.Thread(target=keep_alive, daemon=True).start()
    
    # Iniciar polling
    bot.polling(none_stop=True, interval=0)