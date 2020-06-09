class ListaEnsaio:
    def __init__(self, descricao, data):
        self.lista = list()
        self.descricao = descricao
        self.data = data
        self.num_pessoas = 0

    @property
    def cabecalho(self):
        return f'<strong>ENSAIO {self.data} {self.descricao}</strong>\n' \
               f'<em>{self.num_pessoas} pessoa(s) na lista</em>\n\n'

    def vou(self, nome, instrumento):
        try:
            ritmista = {'nome': nome, 'instrumento': instrumento}

            print(f'Pesquisando {ritmista} em {self.lista}')
            if len(self.lista) == 0:
                self.lista.append(ritmista)
                self.num_pessoas += 1
                print(f'{ritmista["nome"]} adicionado')
            else:
                for linha in self.lista:
                    if ritmista['nome'] in linha['nome']:
                        print(f'{ritmista["nome"]} já está na lista')
                        break
                    else:
                        self.lista.append(ritmista)
                        self.num_pessoas += 1
                        print(f'{ritmista["nome"]} adicionado')

        except Exception:
            pass
        return self.to_string()

    def naovou(self, nome):
        try:
            for pos, linha in enumerate(self.lista):
                if nome == linha['nome']:
                    self.lista[pos]["emoji"] = '\U0000274C'
                    self.num_pessoas -= 1
                    break
        except Exception:
            pass
        return self.to_string()

    def atraso(self, nome):
        try:
            for pos, linha in enumerate(self.lista):
                if nome == linha['nome']:
                    self.lista[pos]["emoji"] = '\U0001F552'
                    break
        except Exception:
            pass
        return self.to_string()

    def estou(self, nome):
        try:
            for pos, linha in enumerate(self.lista):
                if nome == linha['nome']:
                    self.lista[pos]['emoji'] = '\U00002705'
                    break
        except Exception:
            pass
        return self.to_string()

    def to_string(self):
        texto = self.cabecalho
        for linha in self.lista:
            if len(linha) == 2:
                texto += f'{linha["nome"]} - {linha["instrumento"]}\n'
            if len(linha) == 3:
                texto += f'{linha["emoji"]} {linha["nome"]} - {linha["instrumento"]}\n'
        return texto
