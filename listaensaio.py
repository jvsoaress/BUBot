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
            linha = [nome, instrumento]
            if linha not in self.lista:
                self.lista.append(linha)
            self.num_pessoas += 1
        except Exception:
            pass
        return self.to_string()

    def naovou(self, nome):
        try:
            for pos, linha in enumerate(self.lista):
                if nome in linha:
                    if len(linha) == 3:     # se a pessoa está como "EMOJI nome - instrumento" na lista
                        self.lista[pos].pop(0)
                    self.num_pessoas -= 1
                    self.lista[pos].insert(0, '\U0000274C')
        except Exception:
            pass
        return self.to_string()

    def atraso(self, nome):
        try:
            for pos, linha in enumerate(self.lista):
                if nome in linha:
                    if len(linha) == 3:     # se a pessoa está como "EMOJI nome - instrumento" na lista
                        self.lista[pos].pop(0)
                    self.lista[pos].insert(0, '\U0001F552')
        except Exception:
            pass
        return self.to_string()

    def estou(self, nome):
        try:
            for pos, linha in enumerate(self.lista):
                if nome in linha:
                    if len(linha) == 3:     # se a pessoa está como "EMOJI nome - instrumento" na lista
                        self.lista[pos].pop(0)
                    self.lista[pos].insert(0, '\U00002705')
        except Exception:
            pass
        return self.to_string()

    def to_string(self):
        texto = self.cabecalho
        for linha in self.lista:
            if len(linha) == 2:
                texto += f'{linha[0]} - {linha[1]}\n'
            if len(linha) == 3:
                texto += f'{linha[0]} {linha[1]} - {linha[2]}\n'
        return texto
