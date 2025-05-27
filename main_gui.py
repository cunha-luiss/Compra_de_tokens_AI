# main_gui.py
import wx
import os
import json # For creating dummy db files if needed

# Ensure 'package' is discoverable. If main_gui.py is at the root and 'package' is a subfolder,
# direct imports like below should work.
from package.aplicacao_gui import AplicacaoGUI
# Other classes like contaUsuario, admin, bancoDados are used by AplicacaoGUI.

class LoginFrame(wx.Frame):
    def __init__(self, parent, title, app_logic):
        super(LoginFrame, self).__init__(parent, title=title, size=(400, 280))
        self.app_logic = app_logic
        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        title_text = wx.StaticText(panel, label="Studdy Buddy AI Tokens Login")
        font = title_text.GetFont()
        font.PointSize += 5
        font = font.Bold()
        title_text.SetFont(font)
        vbox.Add(title_text, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=20)        # Username
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        lbl1 = wx.StaticText(panel, label="Login:    ")
        hbox1.Add(lbl1, flag=wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, border=8)
        self.tc_username = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
        hbox1.Add(self.tc_username, proportion=1)
        vbox.Add(hbox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)        # Password
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        lbl2 = wx.StaticText(panel, label="Senha:   ")
        hbox2.Add(lbl2, flag=wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, border=8)
        self.tc_password = wx.TextCtrl(panel, style=wx.TE_PASSWORD | wx.TE_PROCESS_ENTER)
        hbox2.Add(self.tc_password, proportion=1)
        vbox.Add(hbox2, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        vbox.Add((-1, 20)) # Spacer

        # Buttons
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_login = wx.Button(panel, label="Login")
        self.btn_create_account = wx.Button(panel, label="Criar Conta")
        
        hbox3.Add(self.btn_login)
        hbox3.Add(self.btn_create_account, flag=wx.LEFT, border=10)
        vbox.Add(hbox3, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

        self.btn_login.Bind(wx.EVT_BUTTON, self.OnLogin)
        self.btn_create_account.Bind(wx.EVT_BUTTON, self.OnCreateAccount)
        
        # Bind Enter key events for navigation and login
        self.tc_username.Bind(wx.EVT_TEXT_ENTER, self.OnUsernameEnter)
        self.tc_password.Bind(wx.EVT_TEXT_ENTER, self.OnPasswordEnter)

        panel.SetSizer(vbox)

    def OnLogin(self, event):
        username = self.tc_username.GetValue()
        password = self.tc_password.GetValue()
        
        if not username or not password:
            wx.MessageBox("Por favor, digite o login e a senha.", "Erro de Entrada", wx.OK | wx.ICON_ERROR)
            return

        message, user_type = self.app_logic.attempt_login(username, password)

        if user_type:
            wx.MessageBox(message, "Login Bem Sucedido", wx.OK | wx.ICON_INFORMATION)
            self.Close()
            # Pass the same app_logic instance to the main frame
            main_frame = MainAppFrame(None, title="Studdy Buddy AI", app_logic=self.app_logic)
            main_frame.Show()
        else:
            wx.MessageBox(message, "Falha no Login", wx.OK | wx.ICON_ERROR)

    def OnCreateAccount(self, event):
        username = self.tc_username.GetValue()
        password = self.tc_password.GetValue()

        if not username or not password:
            wx.MessageBox("Por favor, digite o login e a senha para a nova conta.", "Erro de Entrada", wx.OK | wx.ICON_ERROR)
            return

        dlg = wx.MessageDialog(self, f"Deseja criar uma nova conta com o login '{username}'?",
                               "Confirmar Criação de Conta", wx.YES_NO | wx.ICON_QUESTION)
        if dlg.ShowModal() == wx.ID_YES:
            message, user_type = self.app_logic.create_new_user(username, password)
            wx.MessageBox(message, "Criação de Conta", wx.OK | wx.ICON_INFORMATION)
            if user_type: # If account created successfully, clear fields
                self.tc_username.SetValue("")
                self.tc_password.SetValue("")
                # Optionally, log them in directly:
                # self.Close()
                # main_frame = MainAppFrame(None, title="Studdy Buddy AI", app_logic=self.app_logic)
                # main_frame.Show()
        dlg.Destroy()

    def OnUsernameEnter(self, event):
        """When Enter is pressed in username field, move focus to password field"""
        self.tc_password.SetFocus()

    def OnPasswordEnter(self, event):
        """When Enter is pressed in password field, attempt login"""
        self.OnLogin(event)


class MainAppFrame(wx.Frame):
    def __init__(self, parent, title, app_logic):
        super(MainAppFrame, self).__init__(parent, title=title, size=(550, 450))
        self.app_logic = app_logic
        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):
        self.panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        welcome_msg = f"Bem-vindo, {self.app_logic.get_current_username()}!" #
        self.welcome_text = wx.StaticText(self.panel, label=welcome_msg)
        font = self.welcome_text.GetFont()
        font.PointSize += 3
        self.welcome_text.SetFont(font)
        vbox.Add(self.welcome_text, flag=wx.ALIGN_CENTER | wx.ALL, border=15)
        
        # Static text for displaying results or info
        self.info_display = wx.StaticText(self.panel, label="\n--- Studdy Buddy AI --- \nSelecione uma opção:")
        self.info_display.Wrap(self.GetSize().width - 40) # Wrap text
        vbox.Add(self.info_display, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=15)


        # Options Buttons Grid
        grid_sizer = wx.GridSizer(2, 2, hgap=10, vgap=10) # Rows, Cols, HGap, VGap

        self.btn_view_tokens = wx.Button(self.panel, label="1. Ver Tokens")
        self.btn_purchase_tokens = wx.Button(self.panel, label="2. Comprar Tokens")
        self.btn_list_users = wx.Button(self.panel, label="3. Listar Usuários")
        self.btn_logout = wx.Button(self.panel, label="4. Sair (Logout)")

        self.btn_view_tokens.Bind(wx.EVT_BUTTON, self.OnViewTokens)
        self.btn_purchase_tokens.Bind(wx.EVT_BUTTON, self.OnPurchaseTokens)
        self.btn_list_users.Bind(wx.EVT_BUTTON, self.OnListUsers)
        self.btn_logout.Bind(wx.EVT_BUTTON, self.OnLogout)
        
        grid_sizer.Add(self.btn_view_tokens, 0, wx.EXPAND)
        grid_sizer.Add(self.btn_purchase_tokens, 0, wx.EXPAND)
        grid_sizer.Add(self.btn_list_users, 0, wx.EXPAND)
        grid_sizer.Add(self.btn_logout, 0, wx.EXPAND)
        
        # Disable admin button if not admin
        if not self.app_logic.get_current_user_permission(): #
            self.btn_list_users.Disable()

        vbox.Add(grid_sizer, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=20)
        
        self.panel.SetSizer(vbox)
        self.Layout()

    def OnViewTokens(self, event):
        tokens = self.app_logic.get_current_user_tokens() #
        self.info_display.SetLabelText(f'Você possui: {tokens} tokens.')
        # wx.MessageBox(f'Você possui: {tokens} tokens', "Quantidade de Tokens", wx.OK | wx.ICON_INFORMATION)

    def OnPurchaseTokens(self, event):
        dlg = TokenPurchaseDialog(self, "Adquirir Mais Tokens", self.app_logic)
        dlg.ShowModal()
        dlg.Destroy()
        # Refresh token count display after dialog closes
        self.OnViewTokens(None) # Call OnViewTokens to update the display
        self.info_display.SetLabelText(f'Compra de tokens processada. Saldo atual: {self.app_logic.get_current_user_tokens()} tokens.')
    def OnListUsers(self, event):
        # This check is also done at button disabling, but good for logical safety
        if not self.app_logic.get_current_user_permission(): #
            wx.MessageBox("Acesso negado. Esta função é apenas para administradores.", "Permissão Negada", wx.OK | wx.ICON_ERROR)
            self.info_display.SetLabelText("Acesso negado à lista de usuários.")
            return

        users_data = self.app_logic.get_all_users_for_admin() #
        if users_data:
            display_text = "Lista de Usuários Registrados:\n" + "-"*30 + "\n"
            for user in users_data:
                display_text += f"Usuário: {user['username']}, Tokens: {user['tokens']}\n" #
            
            # Create a custom dialog with scrollable text
            dlg = UserListDialog(self, "Lista de Usuários", display_text)
            dlg.ShowModal()
            dlg.Destroy()
            self.info_display.SetLabelText("Lista de usuários exibida.")
        else:
            wx.MessageBox("Nenhum usuário comum encontrado ou você não tem permissão.", "Lista de Usuários", wx.OK | wx.ICON_INFORMATION)
            self.info_display.SetLabelText("Nenhum usuário para listar ou acesso negado.")


    def OnLogout(self, event):
        logout_msg = self.app_logic.logout()
        wx.MessageBox(logout_msg + "\nSaindo da plataforma...", "Logout", wx.OK | wx.ICON_INFORMATION)
        self.Close()
        # Show login frame again
        app_instance = wx.GetApp()
        login_frame = LoginFrame(None, title="Studdy Buddy AI Tokens Login", app_logic=app_instance.app_logic)
        login_frame.Show()


class TokenPurchaseDialog(wx.Dialog):
    def __init__(self, parent, title, app_logic):
        super(TokenPurchaseDialog, self).__init__(parent, title=title, size=(380, 320))
        self.app_logic = app_logic
        self.InitUI()
        self.CentreOnParent()

    def InitUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        st_title = wx.StaticText(panel, label="Qual pacote de tokens deseja obter?")
        vbox.Add(st_title, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

        # Token options descriptions from original application
        self.token_options_desc = {
            "10": "10 tokens = R$10,00",
            "20": "20 tokens = R$18,00",
            "50": "50 tokens = R$45,00"
        }
        
        self.rb_group = []
        # Create RadioButtons for token choices
        for key_val, desc_val in self.token_options_desc.items():
            rb = wx.RadioButton(panel, label=desc_val, name=key_val)
            vbox.Add(rb, flag=wx.LEFT | wx.RIGHT | wx.TOP, border=10)
            self.rb_group.append(rb)
        
        if self.rb_group: # Select first one by default
            self.rb_group[0].SetValue(True)

        vbox.Add((-1, 20)) # Spacer

        btn_purchase = wx.Button(panel, label="Confirmar Compra")
        btn_cancel = wx.Button(panel, label="Voltar ao Menu")

        btn_purchase.Bind(wx.EVT_BUTTON, self.OnConfirmPurchase)
        btn_cancel.Bind(wx.EVT_BUTTON, lambda event: self.Close()) # Simple close

        hbox_btns = wx.BoxSizer(wx.HORIZONTAL)
        hbox_btns.Add(btn_purchase)
        hbox_btns.Add(btn_cancel, flag=wx.LEFT, border=10)
        vbox.Add(hbox_btns, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        
        panel.SetSizer(vbox)

    def OnConfirmPurchase(self, event):
        selected_key = None
        for rb in self.rb_group:
            if rb.GetValue():
                selected_key = rb.GetName() # Name was set to the token amount key
                break
        
        if selected_key:
            result_message = self.app_logic.purchase_tokens(selected_key) #
            wx.MessageBox(result_message, "Resultado da Compra", wx.OK | wx.ICON_INFORMATION)
            if "sucesso" in result_message.lower(): #
                self.Close() 
        else:
            wx.MessageBox("Por favor, selecione um pacote de tokens.", "Nenhuma Seleção", wx.OK | wx.ICON_WARNING)

class UserListDialog(wx.Dialog):
    def __init__(self, parent, title, text_content):
        super(UserListDialog, self).__init__(parent, title=title, size=(450, 350))
        self.InitUI(text_content)
        self.CentreOnParent()

    def InitUI(self, text_content):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Create a text control with scroll bars for displaying the user list
        text_ctrl = wx.TextCtrl(panel, value=text_content, 
                               style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL | wx.VSCROLL)
        
        # Set a monospace font for better alignment
        font = wx.Font(9, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        text_ctrl.SetFont(font)
        
        vbox.Add(text_ctrl, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        # Add a close button
        btn_close = wx.Button(panel, wx.ID_OK, "Fechar")
        vbox.Add(btn_close, flag=wx.ALIGN_CENTER | wx.BOTTOM, border=10)

        panel.SetSizer(vbox)

class StuddyBuddyApp(wx.App):
    def OnInit(self):
        # Ensure the directory for DB files exists
        # bancoDados.py expects 'controllers/db/' relative to its own location.
        # Assuming bancoDados.py is in 'package/', this path becomes 'package/controllers/db/'
        db_dir_path = os.path.join('package', 'controllers', 'db')
        if not os.path.exists(db_dir_path):
            try:
                os.makedirs(db_dir_path)
                print(f"Diretório do banco de dados criado: {os.path.abspath(db_dir_path)}")
            except OSError as e:
                wx.MessageBox(f"Erro ao criar diretório do banco de dados {db_dir_path}: {e}", "Erro Crítico", wx.OK | wx.ICON_ERROR)
                return False # Stop app initialization

        # Create dummy db files if they don't exist, to prevent FileNotFoundError
        for db_file in ['users.json', 'admin.json']:
            db_file_path = os.path.join(db_dir_path, db_file)
            if not os.path.exists(db_file_path):
                try:
                    with open(db_file_path, 'w', encoding='utf-8') as f:
                        json.dump([], f) # Initialize with an empty list
                    print(f"Arquivo de banco de dados criado: {os.path.abspath(db_file_path)}")
                except IOError as e:
                    wx.MessageBox(f"Erro ao criar arquivo de banco de dados {db_file_path}: {e}", "Erro Crítico", wx.OK | wx.ICON_ERROR)
                    return False


        self.app_logic = AplicacaoGUI() # Create a single instance of the app logic
        self.login_frame = LoginFrame(None, title="Studdy Buddy AI Tokens Login", app_logic=self.app_logic)
        self.login_frame.Show()
        return True

if __name__ == '__main__':
    app = StuddyBuddyApp()
    app.MainLoop()