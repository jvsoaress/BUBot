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

listas_de_ensaio = dict()


# checa se a lista existe
def list_exists(msg):
    try:
        listas_de_ensaio[msg.chat.id]
    except KeyError:
        bot.reply_to(message=msg, text='Não existe nenhuma lista de ensaio. Crie uma nova com /ensaio')
        return False
    else:
        return True


@bot.message_handler(commands=['listas'])
def send_lists(msg):
    print(listas_de_ensaio)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(msg):
    bot.send_message(chat_id=msg.chat.id, text='Para criar um novo ensaio, envie /ensaio seguido de uma descrição.\n\n'
                                               '<code>/ensaio Bixos 2021</code>', parse_mode='HTML')


@bot.message_handler(commands=['ensaio'])
def novo_ensaio(msg):
    chat_id = msg.chat.id
    # checa se o id já existe no banco de dados
    # se não existir, adiciona
    with open('chatlist.txt', 'a+') as chatlist:
        chatlist.seek(0)
        leitor = chatlist.read()
        ids = leitor.split('\n')
        if str(chat_id) not in ids:
            chatlist.write(str(chat_id) + '\n')
            print(f'Novo Chat ID adicionado: {chat_id}')

    global listas_de_ensaio
    # se não houver uma lista criada, crie uma
    if chat_id not in listas_de_ensaio:
        descricao = msg.text[8:]
        data = datetime.now(tz=timezone('Brazil/East'))

        # adiciona um objeto de ListaEnsaio ao dicionário de listas de ensaio
        nova_lista = ListaEnsaio(chat_id, descricao, data)
        listas_de_ensaio[chat_id] = nova_lista

        bot.send_message(chat_id=chat_id,
                         text=f'{nova_lista.cabecalho}\n',
                         reply_markup=respostas,
                         parse_mode='HTML')

        print(f'Nova lista criada (Data: {data} | Chat ID: {chat_id})')
    else:
        bot.send_message(chat_id=msg.chat.id,
                         text='Lista já existente. Para excluir a lista existente, digite /limpar')


@bot.callback_query_handler(func=lambda call: call.data in ['vou', 'naovou', 'atraso', 'estou'])
def update_list(call):
    if list_exists(call.message):
        lista_ensaio = listas_de_ensaio[call.message.chat.id]
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
    lista_ensaio = listas_de_ensaio[call.message.chat.id]
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
    if list_exists(msg):
        lista_ensaio = listas_de_ensaio[msg.chat.id]
        print(f'{msg.from_user.first_name} pediu informações da lista')
        infos = lista_ensaio.infos()
        bot.reply_to(message=msg, text=infos, parse_mode='HTML')


@bot.message_handler(commands=['amanha', 'ontem'])
def change_date(msg):
    if list_exists(msg):
        lista_ensaio = listas_de_ensaio[msg.chat.id]
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


@bot.message_handler(commands=['limpar'])
def delete_lists(msg):
    if list_exists(msg):
        lista_ensaio = listas_de_ensaio[msg.chat.id]
        listas_de_ensaio.__delitem__(msg.chat.id)
        print(f'Lista deletada (Data: {lista_ensaio.data} | Chat ID: {msg.chat.id})')
        bot.reply_to(message=msg, text='Lista de ensaio deletada')


bot.polling(timeout=60, none_stop=True)
