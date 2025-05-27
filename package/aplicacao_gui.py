# package/aplicacao_gui.py
# Refactored from aplicação.py
from package.contaUsuario import contaUsuario
from package.admin import admin
from package.bancoDados import bancoDados

class AplicacaoGUI:
    def __init__(self):
        # Pathing for bancoDados relies on its own file location
        self.__dbUsuarios = bancoDados('users.json')
        self.__dbAdmin = bancoDados('admin.json')
        self._current_user = None

    def attempt_login(self, login, senha):
        """
        Attempts to log in a user or admin.
        Returns a tuple (message, user_type) where user_type is 'user', 'admin', or None.
        """
        usuario_dict = self.__dbUsuarios.verifica_login(login, senha) #
        admin_dict = self.__dbAdmin.verifica_login(login, senha) #

        if usuario_dict:
            self._current_user = contaUsuario(
                usuario_dict["_contaUsuario__username"], #
                usuario_dict["_contaUsuario__senha"], #
                usuario_dict["_contaUsuario__tokens"] #
            )
            return "Usuário encontrado!", "user"
        elif admin_dict:
            self._current_user = admin(
                admin_dict["_admin__username"], #
                admin_dict["_admin__senha"], #
                admin_dict["_admin__tokens"] #
            )
            return f"Admin encontrado. Bem vindo {self._current_user.username()}!", "admin"
        else:
            return "Usuário não encontrado.", None

    def create_new_user(self, login, senha):
        """
        Creates a new user account.
        Returns a tuple (message, user_type) where user_type is 'user' or None.
        """
        if self.__dbUsuarios.verifica_login(login, senha) or self.__dbAdmin.verifica_login(login, senha): #
            return "Login já existente. Tente outro.", None
        
        new_user_obj = contaUsuario(login, senha) #
        self.__dbUsuarios.addItem(new_user_obj) #
        
        # Automatically log in the new user
        usuario_dict = self.__dbUsuarios.verifica_login(login, senha) #
        if usuario_dict:
            self._current_user = contaUsuario(
                usuario_dict["_contaUsuario__username"], #
                usuario_dict["_contaUsuario__senha"], #
                usuario_dict["_contaUsuario__tokens"] #
            )
            return "Nova conta criada com sucesso!", "user"
        return "Falha ao criar e logar com a nova conta.", None

    def get_current_user_tokens(self):
        if self._current_user:
            return self._current_user.tokens() #
        return 0

    def purchase_tokens(self, amount_key):
        """
        Adds tokens to the current user's account based on the amount_key ('10', '20', '50').
        Returns a message string.
        """
        tokens_to_add = 0
        if amount_key == '10':
            tokens_to_add = 10
        elif amount_key == '20':
            tokens_to_add = 20
        elif amount_key == '50':
            tokens_to_add = 50
        
        if tokens_to_add > 0 and self._current_user:
            self._current_user.adicionarTokens(tokens_to_add) #
            self.save_current_user()
            return f"Compra de {tokens_to_add} tokens realizada com sucesso! Novo saldo: {self._current_user.tokens()}"
        elif not self._current_user:
            return "Nenhum usuário logado para comprar tokens."
        else:
            return "Opção de tokens inválida."

    def save_current_user(self):
        if not self._current_user:
            return "Nenhum usuário logado para salvar."
        
        if self._current_user.permissao(): #
            self.__dbAdmin.atualiza_usuario(self._current_user) #
        else:
            self.__dbUsuarios.atualiza_usuario(self._current_user) #
        return "Dados salvos com sucesso!"

    def get_all_users_for_admin(self):
        """
        Returns a list of user data dictionaries if the current user is an admin.
        Otherwise, returns None.
        """
        if self._current_user and self._current_user.permissao(): #
            users_data = []
            all_items = self.__dbUsuarios.get_items() #
            if all_items:
                for user_dict in all_items:
                    users_data.append({
                        "username": user_dict.get('_contaUsuario__username', 'N/A'), #
                        "tokens": user_dict.get('_contaUsuario__tokens', 'N/A') #
                    })
            return users_data
        return None

    def get_current_user_permission(self):
        if self._current_user:
            return self._current_user.permissao() #
        return False
    
    def get_current_username(self):
        if self._current_user:
            return self._current_user.username() #
        return "N/A"

    def logout(self):
        self._current_user = None
        return "Logout realizado com sucesso."