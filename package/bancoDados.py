import json
import os

class bancoDados:
    def __init__(self, filepath):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self._path = os.path.join(base_dir, 'controllers', 'db', filepath)
        if filepath:
            self._load()
        else:
            self.items = []
            self._save()

    def _load(self):
        try:
            with open(self._path, 'r', encoding='utf-8') as f:
                self.items = json.load(f)
        except FileNotFoundError:
            print(f'Arquivo {self._path} não encontrado!')
            self.items = []

    def _save(self):
        with open(self._path, 'w', encoding='utf-8') as f:
            json.dump(self.items, f, indent=4)

    def addItem(self, item):
        #função para criação de login
        novoItem = vars(item)
        self.items.append(novoItem)
        self._save()

    def verifica_login(self, username, senha):
        for usuario in self.items:
            if (
                usuario.get("_contaUsuario__username") == username and
                usuario.get("_contaUsuario__senha") == senha
            ):
                return usuario  # Usuário encontrado
        return None  # Não encontrado

    def atualiza_usuario(self, usuario_atualizado):
        for i, usuario in enumerate(self.items):
            if usuario.get("_contaUsuario__username") == usuario_atualizado.username():
                # Atualiza os dados
                self.items[i]["_contaUsuario__tokens"] = usuario_atualizado.tokens()
                self._save()
                return True
        return False
