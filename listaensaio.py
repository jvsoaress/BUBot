class ListaEnsaio:
    def __init__(self, descricao, data):
        self.lista = list()
        self.descricao = descricao
        self.data = data
        self.num_pessoas = 0
        self.instrumentos = {
            'Caixa': 0,
            'Ripa': 0,
            'Primeira': 0,
            'Segunda': 0,
            'Terceira': 0,
            'Chocalho': 0,
            'Xequerê': 0,
            'Agogô': 0,
            'Tamborim': 0
        }

    @property
    def cabecalho(self):
        return f'\U0001F40D <strong>ENSAIO {self.fmt_data} {self.descricao}</strong>\n' \
               f'<em>{self.num_pessoas} pessoa(s) na lista</em>\n\n'

    @property
    def fmt_data(self):
        return self.data.strftime('%d/%m')

    def vou(self, nome, instrumento):
        try:
            ritmista = {'nome': nome, 'instrumento': instrumento}

            print(f'Pesquisando {ritmista} em {self.lista}')
            if len(self.lista) == 0:
                self.lista.append(ritmista)
                self.num_pessoas += 1
                self.instrumentos[instrumento] += 1
                print(f'{ritmista["nome"]} adicionado')
            else:
                for linha in self.lista:
                    if ritmista['nome'] in linha['nome']:
                        print(f'{ritmista["nome"]} já está na lista')
                        break
                    else:
                        self.lista.append(ritmista)
                        self.num_pessoas += 1
                        self.instrumentos[instrumento] += 1
                        print(f'{ritmista["nome"]} adicionado')
                        break
        except Exception:
            pass
        return self.to_string()

    def naovou(self, nome):
        try:
            for linha in self.lista:
                if nome == linha['nome']:
                    self.lista.remove(linha)
                    self.num_pessoas -= 1
                    print(f'{nome} saiu da lista')
                    break
        except Exception:
            pass
        return self.to_string()

    def atraso(self, nome):
        try:
            for linha in self.lista:
                if nome == linha['nome']:
                    linha["emoji"] = '\U0001F552'
                    break
        except Exception:
            pass
        return self.to_string()

    def estou(self, nome):
        try:
            for linha in self.lista:
                if nome == linha['nome']:
                    linha['emoji'] = '\U00002705'
                    break
        except Exception:
            pass
        return self.to_string()

    def to_string(self):
        try:
            texto = self.cabecalho
            for linha in self.lista:
                if len(linha) == 2:
                    texto += f'{linha["nome"]} - {linha["instrumento"]}\n'
                if len(linha) == 3:
                    texto += f'{linha["emoji"]} {linha["nome"]} - {linha["instrumento"]}\n'
        except Exception:
            pass
        else:
            return texto

    def infos(self):
        infos = self.cabecalho
        for instrumento, qtd in self.instrumentos.items():
            infos += f'<code>{instrumento:<13}{qtd}</code>\n'
        return infos
