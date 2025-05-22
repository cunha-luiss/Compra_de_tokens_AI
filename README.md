# Studdy Buddy AI - Compra de Tokens

## Visão Geral

Este projeto tem como objetivo fornecer uma plataforma de gerenciamento e compra de tokens para uma aplicação denominada "Studdy Buddy AI". A solução permite que usuários e administradores gerenciem suas contas, comprem pacotes de tokens e acompanhem o saldo disponível de forma simples, via interface de linha de comando.

---

## Definição do Problema

Em plataformas de inteligência artificial e assistentes digitais, é comum utilizar um sistema de créditos ou tokens para controlar o acesso a funcionalidades premium ou limitar o uso baseado em consumo. No entanto, a gestão manual desses créditos pode ser trabalhosa, propensa a erros e pouco intuitiva para o usuário final. 

**Problemas enfrentados sem o sistema:**
- Dificuldade de controle sobre o saldo de tokens dos usuários.
- Falta de uma interface de compra e visualização dos tokens.
- Ausência de gerenciamento diferenciado para administradores e usuários comuns.
- Processo manual e suscetível a fraudes ou inconsistências.

---

## Solução Proposta

O "Studdy Buddy AI - Compra de Tokens" automatiza e facilita a administração de tokens, oferecendo:

- **Login e Cadastro**: Usuários podem criar contas e acessar a plataforma.
- **Compra de Tokens**: Possibilidade de adquirir pacotes de tokens (10, 20 ou 50 tokens) com preços diferenciados.
- **Visualização de Saldo**: Usuários podem consultar seu saldo de tokens a qualquer momento.
- **Gestão de Usuários (Admin)**: Administradores têm acesso à lista de todos os usuários e seus respectivos saldos.
- **Persistência de Dados**: Informações são armazenadas em arquivos JSON, garantindo que dados de usuários e administradores sejam salvos de forma segura e persistente.

---

## Casos de Uso

### 1. Usuário Comum

- **Cadastro e Login**: Ao acessar a aplicação, o usuário pode criar uma nova conta ou autenticar-se com uma conta já existente.
- **Visualização de Tokens**: O usuário pode visualizar facilmente seu saldo de tokens.
- **Compra de Tokens**: O usuário pode adquirir novos tokens selecionando o pacote desejado.
- **Uso de Tokens**: Os tokens adquiridos poderão ser utilizados em funcionalidades premium da plataforma Studdy Buddy AI (integração futura).

### 2. Administrador

- **Autenticação como Admin**: O administrador possui permissões diferenciadas.
- **Visualização de Usuários**: Pode ver a lista de todos os usuários cadastrados e seus respectivos saldos.
- **Gestão de Tokens**: Pode acompanhar e, futuramente, gerenciar a distribuição de tokens entre os usuários.

---

## Estrutura da Aplicação

- `package/aplicação.py`: Lógica principal da aplicação, interface do usuário, fluxo de login e operações.
- `package/contaUsuario.py`: Classe de usuários comuns.
- `package/admin.py`: Classe de administradores (herda de contaUsuario).
- `package/bancoDados.py`: Gerenciamento de persistência dos dados dos usuários e administradores em arquivos JSON.
- `testbench_01.py`: Script de inicialização para testes.

---

## Fluxo Básico da Aplicação

1. **Login/Cadastro:** Solicita usuário e senha. Se não existir, oferece a opção de criar uma nova conta.
2. **Menu Principal:**
   - Ver saldo de tokens.
   - Comprar tokens (escolha entre pacotes de 10, 20 ou 50 tokens).
   - Usuário administrador pode visualizar todos os usuários.
   - Sair.

---

## Exemplo de Uso

Ao rodar o `testbench_01.py`, a aplicação será iniciada. O usuário será guiado por menus intuitivos de texto:

```
--- Studdy Buddy AI Tokens Login ---
Digite seu login: usuario1
Digite sua senha: ******
Usuário encontrado!

--- Studdy Buddy AI - Compra de Tokens ---

Opções:
1. Verificação da quantidade de tokens existentes
2. Adquirição de mais tokens
3. Lista de usuário (admin)
4. Sair da plataforma
```

---

## Tecnologias Utilizadas

- **Python 3**
- **Persistência em JSON** (sem dependências de banco de dados externos)

---

## Futuras Expansões

- Integração direta com a plataforma Studdy Buddy AI para uso dos tokens.
- Suporte a outros métodos de pagamento.
- Interface gráfica (GUI) para maior facilidade de uso.
- Relatórios de consumo de tokens.

---

## Contribuição

Sinta-se livre para abrir issues ou pull requests para sugerir melhorias, relatar bugs ou contribuir para o crescimento do projeto.
