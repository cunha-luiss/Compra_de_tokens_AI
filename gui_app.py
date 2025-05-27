# gui_app.py
import wx
# Assuming aplicacao_logic.py is in the same directory or accessible via package structure
from package.aplicacao_logic import AppLogic # type: ignore

# --- Login Dialog ---
class LoginDialog(wx.Dialog):
    def __init__(self, parent, logic):
        super().__init__(parent, title="Studdy Buddy AI Tokens Login", size=(350, 200))
        self.logic = logic
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Input fields
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        lbl1 = wx.StaticText(panel, label="Login:")
        hbox1.Add(lbl1, flag=wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, border=8)
        self.txt_login = wx.TextCtrl(panel)
        hbox1.Add(self.txt_login, proportion=1)
        vbox.Add(hbox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        lbl2 = wx.StaticText(panel, label="Senha:")
        hbox2.Add(lbl2, flag=wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, border=8)
        self.txt_senha = wx.TextCtrl(panel, style=wx.TE_PASSWORD)
        hbox2.Add(self.txt_senha, proportion=1)
        vbox.Add(hbox2, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        vbox.Add((-1, 20)) # Spacer

        # Buttons
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        btn_login = wx.Button(panel, label="Login")
        btn_cancel = wx.Button(panel, label="Cancelar")
        hbox3.Add(btn_login)
        hbox3.Add(btn_cancel, flag=wx.LEFT, border=5)
        vbox.Add(hbox3, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

        panel.SetSizer(vbox)

        # Event Binding
        btn_login.Bind(wx.EVT_BUTTON, self.on_login)
        btn_cancel.Bind(wx.EVT_BUTTON, self.on_cancel)
        # Allow pressing Enter in password field to trigger login
        self.txt_senha.Bind(wx.EVT_TEXT_ENTER, self.on_login)

    def on_login(self, event):
        login = self.txt_login.GetValue()
        senha = self.txt_senha.GetValue()

        if self.logic.check_login(login, senha):
            self.EndModal(wx.ID_OK) # Close dialog, return OK
        else:
            wx.MessageBox("Usuário ou senha inválidos.", "Erro de Login",
                          wx.OK | wx.ICON_ERROR)
            self.txt_senha.SetValue("") # Clear password field

    def on_cancel(self, event):
        self.EndModal(wx.ID_CANCEL) # Close dialog, return Cancel

# --- Main Application Frame ---
class MainFrame(wx.Frame):
    def __init__(self, parent, title, logic):
        super().__init__(parent, title=title, size=(450, 300))
        self.logic = logic
        self.InitUI()
        self.Centre()
        self.UpdateTokenDisplay() # Initial token display

    def InitUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Welcome and Token Display
        user = self.logic.get_current_user()
        welcome_text = f"Bem-vindo(a), {user}!"
        st_welcome = wx.StaticText(panel, label=welcome_text, style=wx.ALIGN_CENTER)
        font_welcome = st_welcome.GetFont()
        font_welcome.PointSize += 2
        font_welcome = font_welcome.Bold()
        st_welcome.SetFont(font_welcome)
        vbox.Add(st_welcome, flag=wx.EXPAND | wx.ALL, border=15)

        self.st_tokens = wx.StaticText(panel, label="Você possui: 0 tokens", style=wx.ALIGN_CENTER)
        font_tokens = self.st_tokens.GetFont()
        font_tokens.PointSize += 1
        self.st_tokens.SetFont(font_tokens)
        vbox.Add(self.st_tokens, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=15)

        vbox.Add((-1, 20)) # Spacer

        # Buttons
        hbox_buttons = wx.BoxSizer(wx.HORIZONTAL)

        btn_buy = wx.Button(panel, label="Adquirir mais Tokens")
        btn_refresh = wx.Button(panel, label="Atualizar Tokens") # Good practice to have a refresh
        btn_logout = wx.Button(panel, label="Sair (Logout)")

        hbox_buttons.Add(btn_buy, flag=wx.RIGHT, border=10)
        hbox_buttons.Add(btn_refresh, flag=wx.RIGHT, border=10)
        hbox_buttons.Add(btn_logout)

        vbox.Add(hbox_buttons, flag=wx.ALIGN_CENTER | wx.BOTTOM, border=20)

        panel.SetSizer(vbox)

        # Event Binding
        btn_buy.Bind(wx.EVT_BUTTON, self.on_buy_tokens)
        btn_refresh.Bind(wx.EVT_BUTTON, self.on_refresh_tokens) # Bind refresh button
        btn_logout.Bind(wx.EVT_BUTTON, self.on_logout)
        self.Bind(wx.EVT_CLOSE, self.on_close_window) # Handle window close button

    def UpdateTokenDisplay(self):
        """Updates the token count label."""
        count = self.logic.get_tokens()
        self.st_tokens.SetLabel(f"Você possui: {count} tokens")

    def on_buy_tokens(self, event):
        """Opens the purchase dialog."""
        with PurchaseDialog(self, self.logic) as dlg:
            # ShowModal waits until the dialog is closed
            if dlg.ShowModal() == wx.ID_OK:
                wx.MessageBox(f"Compra realizada com sucesso!\nVocê agora tem {self.logic.get_tokens()} tokens.",
                              "Compra de Tokens", wx.OK | wx.ICON_INFORMATION)
                self.UpdateTokenDisplay() # Update display after purchase

    def on_refresh_tokens(self, event):
        """Handles the refresh button click."""
        self.UpdateTokenDisplay()
        wx.MessageBox("Contagem de tokens atualizada.", "Info", wx.OK | wx.ICON_INFORMATION)

    def on_logout(self, event):
        """Logs the user out and closes the main window."""
        self.logic.logout()
        wx.MessageBox("Você foi desconectado.", "Logout", wx.OK | wx.ICON_INFORMATION)
        self.Close() # Close this frame

    def on_close_window(self, event):
        """Ensures logout logic runs if window is closed directly."""
        self.logic.logout() # Optional: logout if they close window without logout button
        self.Destroy() # Properly destroy the window

# --- Purchase Dialog ---
class PurchaseDialog(wx.Dialog):
    def __init__(self, parent, logic):
        super().__init__(parent, title="Adquirir Tokens", size=(350, 250))
        self.logic = logic
        self.selected_amount = 0
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        st_title = wx.StaticText(panel, label="Selecione a quantidade de tokens:")
        vbox.Add(st_title, flag=wx.ALL, border=10)

        # Using Radio Buttons for selection
        self.rb10 = wx.RadioButton(panel, label="10 tokens = R$10,00", style=wx.RB_GROUP)
        self.rb20 = wx.RadioButton(panel, label="20 tokens = R$18,00")
        self.rb50 = wx.RadioButton(panel, label="50 tokens = R$45,00")

        vbox.Add(self.rb10, flag=wx.LEFT | wx.RIGHT | wx.TOP, border=10)
        vbox.Add(self.rb20, flag=wx.LEFT | wx.RIGHT | wx.TOP, border=10)
        vbox.Add(self.rb50, flag=wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM, border=10)

        vbox.Add((-1, 15)) # Spacer

        # Buttons
        hbox_buttons = wx.BoxSizer(wx.HORIZONTAL)
        btn_confirm = wx.Button(panel, label="Confirmar Compra")
        btn_cancel = wx.Button(panel, label="Cancelar")
        hbox_buttons.Add(btn_confirm)
        hbox_buttons.Add(btn_cancel, flag=wx.LEFT, border=5)
        vbox.Add(hbox_buttons, flag=wx.ALIGN_CENTER | wx.BOTTOM, border=10)

        panel.SetSizer(vbox)

        # Event Binding
        btn_confirm.Bind(wx.EVT_BUTTON, self.on_confirm)
        btn_cancel.Bind(wx.EVT_BUTTON, self.on_cancel)

    def on_confirm(self, event):
        amount_to_buy = 0
        if self.rb10.GetValue():
            amount_to_buy = 10
        elif self.rb20.GetValue():
            amount_to_buy = 20
        elif self.rb50.GetValue():
            amount_to_buy = 50
        else:
            wx.MessageBox("Por favor, selecione uma opção.", "Erro", wx.OK | wx.ICON_WARNING)
            return # Don't proceed

        if self.logic.buy_tokens(amount_to_buy):
            self.EndModal(wx.ID_OK) # Close dialog, signal success
        else:
            # This case shouldn't happen with radio buttons unless not logged in
            wx.MessageBox("Falha ao comprar tokens. Tente novamente.", "Erro", wx.OK | wx.ICON_ERROR)
            self.EndModal(wx.ID_CANCEL) # Close dialog, signal failure/cancel

    def on_cancel(self, event):
        self.EndModal(wx.ID_CANCEL)

# --- Application Class ---
class TokenApp(wx.App):
    def OnInit(self):
        self.logic = AppLogic() # Create the logic instance

        # Show Login Dialog Modally
        with LoginDialog(None, self.logic) as login_dlg:
            res = login_dlg.ShowModal() # Wait here until login dialog closes

        # If login was successful (dialog returned wx.ID_OK)
        if res == wx.ID_OK:
            # Create and show the main frame
            main_frame = MainFrame(None, title="Studdy Buddy AI - Compra de Tokens", logic=self.logic)
            main_frame.Show(True)
            self.SetTopWindow(main_frame) # Important for app lifecycle
            return True # Indicate app should continue
        else:
            # Login failed or was cancelled, exit the app
            return False

# --- Main Execution ---
if __name__ == '__main__':
    app = TokenApp(redirect=False) # redirect=False helps with debugging output
    app.MainLoop()