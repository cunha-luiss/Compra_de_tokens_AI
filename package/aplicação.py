from package.contaUsuario import contaUsuario
from package.admin import admin
from package.bancoDados import bancoDados

class aplicacao():
    def __init__(self):
        self.__dbUsuarios = bancoDados('users.json')
        self.__dbAdmin = bancoDados('admin.json')
        self._login()

    def _login(self):
        while True:
            print("\n--- Studdy Buddy AI Tokens Login ---")
            login = input("Digite seu login: ")
            senha = input("Digite sua senha: ")
            usuario_dict = self.__dbUsuarios.verifica_login(login, senha)
            admin_dict = self.__dbAdmin.verifica_login(login, senha)
            if usuario_dict:
                print("\nUsuário encontrado!")
                # Cria o objeto contaUsuario a partir do dicionário, usando os dados do Banco encontrados pelo verifica_login (que retorna o usuário)
                self._current_user = contaUsuario(
                    usuario_dict["_contaUsuario__username"],
                    usuario_dict["_contaUsuario__senha"],
                    usuario_dict["_contaUsuario__tokens"]
                )
                break
            elif admin_dict:
                print(f"\nAdmin encontrado. Bem vindo {admin_dict['_admin__username']}!")
                self._current_user = admin(admin_dict["_admin__username"], admin_dict["_admin__senha"], admin_dict["_admin__tokens"])
                break
            else:
                print("\nUsuário não encontrado")

                create = input("\nDeseja criar uma nova conta? ")
                if create in ["Sim", "S", "s", "sim"]:
                    self.__nUsuario = contaUsuario(login,senha)
                    self._newDbUser = self.__dbUsuarios.addItem(self.__nUsuario)
                    usuario_dict = self.__dbUsuarios.verifica_login(login, senha)
                    self._current_user = contaUsuario(usuario_dict["_contaUsuario__username"], usuario_dict["_contaUsuario__senha"], usuario_dict["_contaUsuario__tokens"])
                    break
                else:
                    print('')
        self.loop()

    def loop(self):
        voltar = False
        while not voltar:
            # Interface da aplicação
            print("\n--- Studdy Buddy AI - Compra de Tokens ---")
            print("\nOpções:")
            print("1. Verificação da quantidade de tokens existentes")
            print("2. Adquirição de mais tokens")
            print("3. Lista de usuário")
            print("4. Sair da plataforma")

            choice = input("Escolha sua opção: ")

            if choice == '1':
                self.quantidade_tokens()
            elif choice == '2':
                self.compraTokens()
            elif choice == '3':
                if self._current_user.permissao():
                    print("\nAqui está a lista de todos os usuários presentes na plataforma:")
                    self.listaAdmin()
                else: print("\n Vaza daqui!")
            elif choice == '4':
                print("\nSaindo...")
                voltar = True
            else:
                print('\nOpção inválida, tente novamente!')
                
    def saveUser(self):
        # Atualiza o banco de dados
        if self._current_user.permissao():
            self.__dbAdmin.atualiza_usuario(self._current_user)
        else:
            self.__dbUsuarios.atualiza_usuario(self._current_user)
        print("Salvo com sucesso!")

    def quantidade_tokens(self):
        print(f'\nVocê possui: {self._current_user.tokens()} tokens')

    def compraTokens(self):
        print("\nQual pacote deseja obter?")
        print("10 tokens = R$10,00")
        print("20 tokens = R$18,00")
        print("50 tokens = R$45,00")
        print("\n--Digite M se quiser voltar ao menu--")
        choice2 = input("\nInserir quantos tokens: ")

        if choice2 == '10':
            print("\nCompra realizada com sucesso")
            self._current_user.adicionarTokens(10)
            self.saveUser()
        elif choice2 == '20':
            print("\nCompra realizada com sucesso")
            self._current_user.adicionarTokens(20)
            self.saveUser()
        elif choice2 == '50':
            print("\nCompra realizada com sucesso")
            self._current_user.adicionarTokens(50)
            self.saveUser()
        elif choice2 == 'M':
            print("Voltando...")
        else:
            print("\nOpção não encontrada, tente novamente")
            self.compraTokens()
    
    def listaAdmin(self):
        for user in self.__dbUsuarios.get_items():
            print(f"Usuário: {user.get('_contaUsuario__username', 'N/A')}, Tokens: {user.get('_contaUsuario__tokens', 'N/A')}")
