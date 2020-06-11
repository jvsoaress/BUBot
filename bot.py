import telebot
import configparser
from listaensaio import ListaEnsaio
from datetime import datetime, timedelta
from pytz import timezone
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
    global lista_ensaio
    if not isinstance(lista_ensaio, ListaEnsaio):
        descricao = msg.text[8:]
        data = datetime.now(tz=timezone('Brazil/East'))

        lista_ensaio = ListaEnsaio(descricao, data)

        bot.send_message(chat_id=msg.chat.id,
                         text=f'{lista_ensaio.cabecalho}\n',
                         reply_markup=respostas,
                         parse_mode='HTML')

        print(f'Novo ensaio criado em {data}')
    else:
        bot.send_message(chat_id=msg.chat.id,
                         text='Lista já existente. Para excluir uma lista, digite /deletar')


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


@bot.callback_query_handler(func=lambda call: call.data in ['caixa', 'ripa', 'agogô', 'chocalho', 'xequerê',
                                                            'primeira', 'segunda', 'terceira', 'tamborim'])
def set_instrument(call):
    nome = call.from_user.username
    instrumento = call.data.title()
    texto = lista_ensaio.vou(nome, instrumento)
    bot.edit_message_text(text=texto,
                          message_id=call.message.message_id,
                          chat_id=call.message.chat.id,
                          parse_mode='HTML',
                          reply_markup=respostas)


@bot.message_handler(commands=['infos'])
def send_list_infos(msg):
    if isinstance(lista_ensaio, ListaEnsaio):
        print(f'{msg.from_user.first_name} pediu informações da lista')
        infos = lista_ensaio.infos()
        bot.reply_to(message=msg, text=infos, parse_mode='HTML')
    else:
        bot.reply_to(message=msg, text='Não existe nenhuma lista de ensaio. Crie uma nova com /ensaio')


@bot.message_handler(commands=['amanha', 'ontem'])
def change_date(msg):
    global lista_ensaio
    if lista_ensaio:
        try:
            message_id = msg.reply_to_message.message_id
        except AttributeError:
            bot.reply_to(message=msg, text='Responda à mensagem contendo a lista que deseja alterar a data')
        else:
            if msg.text == '/amanha':
                nova_data = timedelta(days=1)
            else:
                nova_data = timedelta(days=-1)
            lista_ensaio.data += nova_data
            texto = lista_ensaio.to_string()
            bot.edit_message_text(chat_id=msg.chat.id,
                                  message_id=message_id,
                                  text=texto,
                                  parse_mode='HTML',
                                  reply_markup=respostas)
            print(f'{msg.from_user.first_name} alterou a data do ensaio')


@bot.message_handler(commands=['deletar'])
def delete_list(msg):
    global lista_ensaio
    if lista_ensaio:
        try:
            message_id = msg.reply_to_message.message_id
        except AttributeError:
            bot.reply_to(message=msg, text='Responda à mensagem contendo a lista que deseja deletar')
        else:
            bot.delete_message(chat_id=msg.chat.id, message_id=message_id)
            bot.reply_to(message=msg, text='Lista de ensaio deletada')
            lista_ensaio = None
    else:
        bot.reply_to(message=msg, text='Não existe nenhuma lista de ensaio. Crie uma nova com /ensaio')


bot.polling(timeout=60, none_stop=True)
