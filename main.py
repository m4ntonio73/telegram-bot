import telebot
import os
from flask import Flask
import threading
import requests
import time

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

# Função de ping automático para evitar hibernação
def auto_ping():
    time.sleep(300)  # Aguarda 5 minutos antes de começar
    while True:
        try:
            # Obtém a URL do próprio serviço
            service_url = os.environ.get('RENDER_EXTERNAL_URL', 'http://localhost:5000')
            response = requests.get(f"{service_url}/status", timeout=30)
            print(f"🔄 Ping automático: {response.status_code} - {time.strftime('%H:%M:%S')}")
        except Exception as e:
            print(f"⚠️ Erro no ping: {e}")
        time.sleep(600)  # Ping a cada 10 minutos

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
                "/ping - Testar conexão\n"
                "/uptime - Tempo online")

@bot.message_handler(commands=['status'])
def status_command(message):
    bot.reply_to(message, "✅ Bot funcionando perfeitamente no Render!")

@bot.message_handler(commands=['ping'])
def ping(message):
    bot.reply_to(message, "🏓 Pong! Bot está online.")

@bot.message_handler(commands=['uptime'])
def uptime(message):
    bot.reply_to(message, "⏰ Bot está online 24/7 com ping automático ativado!")

# Responder mensagens normais
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"Você disse: {message.text}")

# Função para rodar o bot
def run_bot():
    keep_alive()
    bot.polling(none_stop=True, interval=0, timeout=60)

# Executar tudo
if __name__ == "__main__":
    # Iniciar ping automático
    #ping_thread = threading.Thread(target=auto_ping)
    #ping_thread.daemon = True
    #ping_thread.start()
    
    # Iniciar bot em thread separada
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    print("🌐 Servidor Flask iniciado...")
    print("🔄 Ping automático ativado...")
    
    # Iniciar servidor Flask
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
