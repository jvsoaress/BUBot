from telebot import types as t


class Buttons:
    resposta = t.InlineKeyboardMarkup(row_width=2)
    resposta1 = t.InlineKeyboardButton(text='\U0001F3C3 Vou', callback_data='vou')
    resposta2 = t.InlineKeyboardButton(text='\U0000274C Não vou', callback_data='naovou')
    resposta3 = t.InlineKeyboardButton(text='\U0001F552 Atraso', callback_data='atraso')
    resposta4 = t.InlineKeyboardButton(text='\U00002705 Estou', callback_data='estou')
    resposta.add(resposta1, resposta2, resposta3, resposta4)

    instrumentos = t.InlineKeyboardMarkup(row_width=3)
    caixa = t.InlineKeyboardButton(text='Caixa', callback_data='caixa')
    primeira = t.InlineKeyboardButton(text='Primeira', callback_data='primeira')
    segunda = t.InlineKeyboardButton(text='Segunda', callback_data='segunda')
    terceira = t.InlineKeyboardButton(text='Terceira', callback_data='terceira')
    ripa = t.InlineKeyboardButton(text='Ripa', callback_data='ripa')
    tamborim = t.InlineKeyboardButton(text='Tamborim', callback_data='tamborim')
    chocalho = t.InlineKeyboardButton(text='Chocalho', callback_data='chocalho')
    agogo = t.InlineKeyboardButton(text='Agogô', callback_data='agogo')
    xequere = t.InlineKeyboardButton(text='Xequerê', callback_data='xequere')
    instrumentos.add(caixa, primeira, segunda, terceira, ripa, tamborim, chocalho, agogo, xequere)
