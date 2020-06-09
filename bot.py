import telebot
import configparser
from listaensaio import ListaEnsaio
from datetime import datetime
from buttons import Buttons

config = configparser.ConfigParser()
config.read('bot.conf')

TOKEN = config['BUBOT']['TOKEN']

bot = telebot.TeleBot(TOKEN)

respostas = Buttons.resposta
instrumentos = Buttons.instrumentos

lista_ensaio = None


@bot.message_handler(commands=['start', 'help'])
def send_welcome(msg):
    bot.send_message(chat_id=msg.chat.id, text='Para criar um novo ensaio, envie /ensaio seguido de uma descrição.\n\n'
                                               '<code>/ensaio Bixos 2021</code>', parse_mode='HTML')


@bot.message_handler(commands=['ensaio'])
def novo_ensaio(msg):
    descricao = msg.text[8:]
    hoje = datetime.now()
    data = f'{hoje.day:0>2}/{hoje.month:0>2}'

    global lista_ensaio
    lista_ensaio = ListaEnsaio(descricao, data)

    bot.send_message(chat_id=msg.chat.id,
                     text=f'{lista_ensaio.cabecalho}\n',
                     reply_markup=respostas,
                     parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: call.data in ['vou', 'naovou', 'atraso', 'estou'])
def update_list(call):
    if call.from_user.username is not None:
        nome = call.from_user.username
    else:
        nome = call.from_user.first_name

    if call.data == 'vou':
        bot.edit_message_reply_markup(message_id=call.message.message_id,
                                      chat_id=call.message.chat.id,
                                      reply_markup=instrumentos)
    else:
        if call.data == 'naovou':
            texto = lista_ensaio.naovou(nome)

        elif call.data == 'atraso':
            texto = lista_ensaio.atraso(nome)

        elif call.data == 'estou':
            texto = lista_ensaio.estou(nome)

        bot.edit_message_text(text=texto,
                              message_id=call.message.message_id,
                              chat_id=call.message.chat.id,
                              parse_mode='HTML',
                              reply_markup=respostas)


@bot.callback_query_handler(func=lambda call: call.data in ['caixa', 'ripa', 'agogo', 'chocalho', 'xequere',
                                                            'primeira', 'segunda', 'terceira', 'tamborim'])
def set_instrument(call):
    nome = call.from_user.username
    instrumento = call.data
    texto = lista_ensaio.vou(nome, instrumento)
    bot.edit_message_text(text=texto,
                          message_id=call.message.message_id,
                          chat_id=call.message.chat.id,
                          parse_mode='HTML',
                          reply_markup=respostas)


bot.polling(timeout=20, none_stop=True)
