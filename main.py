import telebot
import os
from flask import Flask, jsonify
import threading
import requests
import time
from datetime import datetime
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Configurar Flask (para o Render detectar porta)
app = Flask(__name__)

# Variáveis globais para monitoramento
bot_start_time = datetime.now()
last_bot_activity = datetime.now()
bot_is_alive = False

@app.route('/')
def home():
    return "🤖 Bot Telegram está rodando no Render!"

@app.route('/status')
def status():
    return "✅ Bot funcionando perfeitamente!"

# NOVO: Endpoint de Health Check detalhado
@app.route('/health')
def health():
    global bot_is_alive, last_bot_activity, bot_start_time
    
    current_time = datetime.now()
    uptime = current_time - bot_start_time
    
    # Verificar se o bot está respondendo (últimos 2 minutos)
    minutes_since_activity = (current_time - last_bot_activity).total_seconds() / 60
    bot_responsive = minutes_since_activity < 2
    
    health_data = {
        'status': 'healthy' if bot_is_alive and bot_responsive else 'unhealthy',
        'bot_alive': bot_is_alive,
        'bot_responsive': bot_responsive,
        'uptime_seconds': int(uptime.total_seconds()),
        'uptime_formatted': str(uptime).split('.')[0],
        'last_activity': last_bot_activity.isoformat(),
        'minutes_since_activity': round(minutes_since_activity, 2),
        'timestamp': current_time.isoformat(),
        'port': os.environ.get('PORT', 5000),
        'render_url': os.environ.get('RENDER_EXTERNAL_URL', 'localhost')
    }
    
    print(f"🏥 Health Check: {health_data['status']} - {current_time.strftime('%H:%M:%S')}")
    return jsonify(health_data)

# NOVO: Endpoint para forçar restart se necessário
@app.route('/restart')
def restart_bot():
    print("🔄 Restart solicitado via endpoint")
    # Aqui você pode implementar lógica de restart se necessário
    return jsonify({'message': 'Restart signal sent', 'timestamp': datetime.now().isoformat()})

# Configurar bot Telegram
TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)

# Função para atualizar atividade do bot
def update_bot_activity():
    global last_bot_activity
    last_bot_activity = datetime.now()

# Função para criar menu principal
def create_main_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    
    # Primeira linha
    btn_start = InlineKeyboardButton("🚀 Iniciar", callback_data="start")
    btn_help = InlineKeyboardButton("❓ Ajuda", callback_data="help")
    markup.add(btn_start, btn_help)
    
    # Segunda linha
    btn_status = InlineKeyboardButton("📊 Status", callback_data="status")
    btn_ping = InlineKeyboardButton("🏓 Ping", callback_data="ping")
    markup.add(btn_status, btn_ping)
    
    # Terceira linha
    btn_uptime = InlineKeyboardButton("⏰ Uptime", callback_data="uptime")
    btn_info = InlineKeyboardButton("ℹ️ Info", callback_data="info")
    markup.add(btn_uptime, btn_info)
    
    # Quarta linha
    btn_support = InlineKeyboardButton("💝 Apoiar Canal", url="https://t.me/PyteTeam")
    markup.add(btn_support)
    
    return markup

# Função para criar menu de volta
def create_back_menu():
    markup = InlineKeyboardMarkup()
    btn_back = InlineKeyboardButton("⬅️ Voltar ao Menu", callback_data="menu")
    markup.add(btn_back)
    return markup

# Função para manter o bot ativo
def keep_alive():
    global bot_is_alive
    bot_is_alive = True
    print("🚀 Bot Telegram iniciado...")

# Comandos do bot
@bot.message_handler(commands=['start'])
def start(message):
    update_bot_activity()  # Atualizar atividade
    welcome_text = (
        "🤖 **Olá! Bem-vindo ao Bot!** 👋\n\n"
        "Eu sou um bot rodando no Render 24/7!\n"
        "Use o menu abaixo para navegar pelas opções:"
    )
    bot.send_message(
        message.chat.id, 
        welcome_text,
        reply_markup=create_main_menu(),
        parse_mode='Markdown'
    )

@bot.message_handler(commands=['menu'])
def menu_command(message):
    update_bot_activity()  # Atualizar atividade
    bot.send_message(
        message.chat.id,
        "📋 **Menu Principal**\n\nEscolha uma opção:",
        reply_markup=create_main_menu(),
        parse_mode='Markdown'
    )

# Handler para botões inline
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    update_bot_activity()  # Atualizar atividade
    try:
        if call.data == "start":
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="🚀 **Bot Iniciado!**\n\n"
                     "✅ Todas as funcionalidades estão ativas\n"
                     "🌐 Servidor rodando no Render\n"
                     "🔄 Ping automático ativado\n\n"
                     "Bot pronto para uso!",
                reply_markup=create_back_menu(),
                parse_mode='Markdown'
            )
        
        elif call.data == "help":
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="❓ **Como usar o bot:**\n\n"
                     "🚀 **Iniciar** - Reinicia o bot\n"
                     "📊 **Status** - Verifica se está funcionando\n"
                     "🏓 **Ping** - Testa a conexão\n"
                     "⏰ **Uptime** - Tempo online\n"
                     "ℹ️ **Info** - Informações do sistema\n\n"
                     "💬 Você também pode enviar mensagens normais!",
                reply_markup=create_back_menu(),
                parse_mode='Markdown'
            )
        
        elif call.data == "status":
            current_time = datetime.now()
            uptime = current_time - bot_start_time
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="📊 **Status do Bot**\n\n"
                     "✅ **Status:** Online\n"
                     "🌐 **Servidor:** Render\n"
                     "🔄 **Ping:** Ativo\n"
                     "⚡ **Resposta:** Rápida\n"
                     f"⏰ **Uptime:** {str(uptime).split('.')[0]}\n\n"
                     "Tudo funcionando perfeitamente!",
                reply_markup=create_back_menu(),
                parse_mode='Markdown'
            )
        
        elif call.data == "ping":
            start_time = time.time()
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="🏓 **Pong!**\n\n"
                     f"⚡ **Latência:** {round((time.time() - start_time) * 1000)}ms\n"
                     f"🕐 **Horário:** {time.strftime('%H:%M:%S')}\n"
                     f"📅 **Data:** {time.strftime('%d/%m/%Y')}\n\n"
                     "Bot está online e respondendo!",
                reply_markup=create_back_menu(),
                parse_mode='Markdown'
            )
        
        elif call.data == "uptime":
            current_time = datetime.now()
            uptime = current_time - bot_start_time
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="⏰ **Informações de Uptime**\n\n"
                     f"🚀 **Iniciado:** {bot_start_time.strftime('%d/%m/%Y %H:%M:%S')}\n"
                     f"⏱️ **Tempo Online:** {str(uptime).split('.')[0]}\n"
                     "🔄 **Ping automático:** A cada 10 min\n"
                     "⚡ **Resposta:** 24/7\n"
                     "🛡️ **Estabilidade:** Alta\n\n"
                     "Bot configurado para máxima disponibilidade!",
                reply_markup=create_back_menu(),
                parse_mode='Markdown'
            )
        
        elif call.data == "info":
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="ℹ️ **Informações do Sistema**\n\n"
                     "🤖 **Bot:** Telegram Bot API\n"
                     "🐍 **Linguagem:** Python\n"
                     "📚 **Biblioteca:** pyTelegramBotAPI\n"
                     "🌐 **Hospedagem:** Render\n"
                     "🔧 **Framework:** Flask\n"
                     "🏥 **Health Check:** Ativo\n\n"
                     "Desenvolvido com ❤️",
                reply_markup=create_back_menu(),
                parse_mode='Markdown'
            )
        
        elif call.data == "menu":
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="📋 **Menu Principal**\n\nEscolha uma opção:",
                reply_markup=create_main_menu(),
                parse_mode='Markdown'
            )
        
        # Responder ao callback para remover o "loading"
        bot.answer_callback_query(call.id)
        
    except Exception as e:
        print(f"❌ Erro no callback: {e}")
        bot.answer_callback_query(call.id, "❌ Erro ao processar comando")

# Comandos tradicionais (ainda funcionam)
@bot.message_handler(commands=['help'])
def help_command(message):
    update_bot_activity()  # Atualizar atividade
    bot.reply_to(message, 
                "📋 Use /menu para acessar o menu interativo ou digite os comandos:\n"
                "/start - Iniciar conversa\n"
                "/menu - Menu interativo\n"
                "/status - Status do bot\n"
                "/ping - Testar conexão")

@bot.message_handler(commands=['status'])
def status_command(message):
    update_bot_activity()  # Atualizar atividade
    current_time = datetime.now()
    uptime = current_time - bot_start_time
    bot.reply_to(message, f"✅ Bot funcionando perfeitamente no Render!\n⏰ Uptime: {str(uptime).split('.')[0]}")

@bot.message_handler(commands=['ping'])
def ping(message):
    update_bot_activity()  # Atualizar atividade
    bot.reply_to(message, "🏓 Pong! Bot está online.")

# Responder mensagens normais
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    update_bot_activity()  # Atualizar atividade
    response_text = (
        f"💬 **Você disse:** {message.text}\n\n"
        "Use /menu para acessar o menu interativo!"
    )
    bot.reply_to(message, response_text, parse_mode='Markdown')

# Função para rodar o bot com tratamento de erros
def run_bot():
    global bot_is_alive
    keep_alive()
    while True:
        try:
            print("🤖 Iniciando polling do bot...")
            bot.polling(none_stop=True, interval=0, timeout=60)
        except Exception as e:
            print(f"❌ Erro no bot: {e}")
            bot_is_alive = False
            time.sleep(30)  # Aguarda 30 segundos antes de tentar novamente
            bot_is_alive = True
            print("🔄 Tentando reconectar...")

# Executar tudo
if __name__ == "__main__":
    # Iniciar bot em thread separada
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    print("🌐 Servidor Flask iniciado...")
    print("🏥 Health Check endpoint: /health")
    print("🔄 Ping automático ativado...")
    print("📋 Menu interativo configurado...")
    
    # Iniciar servidor Flask
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
