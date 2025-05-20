from package.contaUsuario import contaUsuario

class admin(contaUsuario):
    def __init__(self, username, senha, tokens=0):
        super().__init__(username, senha, tokens)
    def permissao(self):
        return True