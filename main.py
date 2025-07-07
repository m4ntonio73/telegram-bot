import telebot
import os
from flask import Flask
import threading

# Configurar Flask (para o Render detectar porta)
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Bot Telegram está rodando no Render!"

@app.route('/status')
def status():
    return "✅ Bot funcionando perfeitamente!"

# Configurar bot Telegram
TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)

# Função para manter o bot ativo
def keep_alive():
    print("🚀 Bot Telegram iniciado...")

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
def status_command(message):
    bot.reply_to(message, "✅ Bot funcionando perfeitamente no Render!")

@bot.message_handler(commands=['ping'])
def ping(message):
    bot.reply_to(message, "🏓 Pong! Bot está online.")

# Responder mensagens normais
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"Você disse: {message.text}")

# Função para rodar o bot
def run_bot():
    keep_alive()
    bot.polling(none_stop=True, interval=0, timeout=60)

# Executar ambos
if __name__ == "__main__":
    # Iniciar bot em thread separada
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    print("🌐 Servidor Flask iniciado...")
    # Iniciar servidor Flask
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
