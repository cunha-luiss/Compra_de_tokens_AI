class contaUsuario():
    def __init__(self, username, senha, tokens = 0):
        self.__username = username
        self.__senha = senha
        self.__tokens = tokens

    def username(self):
        return self.__username
    def senha(self):
        return self.__senha
    def tokens(self):
        return self.__tokens
    def adicionarTokens(self, amount):
        self.__tokens += amount

    def permissao(self):
        return False