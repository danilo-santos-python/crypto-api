import os
import sys
import customtkinter as ctk
import tkinter as tk
from datetime import datetime
from crypto_api import get_crypto_data

# -------------------------------------------------
# Diretório base
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# -------------------------------------------------
# Compatibilidade PyInstaller
# -------------------------------------------------
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = BASE_DIR

    return os.path.join(base_path, relative_path)

# -------------------------------------------------
# Ícones
# -------------------------------------------------
ICON_ICO = resource_path(os.path.join("assets", "coin.ico"))
ICON_PNG = resource_path(os.path.join("assets", "coin.png"))

# -------------------------------------------------
# Fonte multiplataforma
# -------------------------------------------------
FONT_FAMILY = "Consolas" if sys.platform.startswith("win") else "DejaVu Sans Mono"

# -------------------------------------------------
# Cores globais
# -------------------------------------------------
BG_COLOR = "#FFFFFF"

# -------------------------------------------------
# Aparência do app
# -------------------------------------------------
ctk.set_appearance_mode("light")

# -------------------------------------------------
# Dados
# -------------------------------------------------
ID_TO_TICKER = {
    "ripple": "XRP",
    "stellar": "XLM",
    "hedera-hashgraph": "HBAR",
    "ondo-finance": "ONDO",
    "xdce-crowd-sale": "XDC",
    "kaspa": "KASPA",
}

ORDER = [
    "ripple",
    "stellar",
    "hedera-hashgraph",
    "ondo-finance",
    "xdce-crowd-sale",
    "kaspa"
]


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Crypto API")
        self.geometry("500x400")
        self.resizable(False, False)

        self.configure(fg_color=BG_COLOR)

        self._set_icon()

        self.table_rows = []
        self.update_job = None

        self.create_widgets()
        self.update_prices()

    # -------------------------------------------------
    # Ícone multiplataforma
    # -------------------------------------------------
    def _set_icon(self):

        try:
            if sys.platform.startswith("win") and os.path.exists(ICON_ICO):
                self.iconbitmap(ICON_ICO)

            elif os.path.exists(ICON_PNG):
                self.icon_image = tk.PhotoImage(file=ICON_PNG)
                self.iconphoto(False, self.icon_image)

        except Exception:
            pass

    # -------------------------------------------------
    # Interface
    # -------------------------------------------------
    def create_widgets(self):

        title_font = ctk.CTkFont(
            family=FONT_FAMILY,
            size=20,
            weight="bold"
        )

        data_font = ctk.CTkFont(
            family=FONT_FAMILY,
            size=13
        )

        header_font = ctk.CTkFont(
            family=FONT_FAMILY,
            size=13,
            weight="bold"
        )

        self.title_label = ctk.CTkLabel(
            self,
            text="Cotações ao Vivo (USD / BRL)",
            font=title_font
        )

        self.title_label.pack(pady=14)

        self.table_frame = ctk.CTkFrame(
            self,
            fg_color="#D8F7FF"
        )

        self.table_frame.pack(fill="x", padx=20, pady=(0, 6))

        headers = ["Criptomoeda", "USD", "BRL"]

        for col, text in enumerate(headers):

            anchor = "w" if col == 0 else "e"

            label = ctk.CTkLabel(
                self.table_frame,
                text=text,
                font=header_font,
                anchor=anchor
            )

            label.grid(
                row=0,
                column=col,
                sticky=anchor,
                padx=8,
                pady=6
            )

        self.table_frame.grid_columnconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(1, minsize=140)
        self.table_frame.grid_columnconfigure(2, minsize=140)

        self.last_update_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=11)
        )

        self.last_update_label.pack(pady=(8, 6))

        self.btn = ctk.CTkButton(
            self,
            text="Atualizar Agora",
            command=self.update_prices
        )

        self.btn.pack(pady=(0, 11))

        self.link_sobre = ctk.CTkLabel(
            self,
            text="Sobre",
            text_color="#999292",
            cursor="hand2",
            font=ctk.CTkFont(size=13)
        )

        self.link_sobre.place(
            relx=1.0,
            rely=0.90,
            anchor="ne",
            x=-22
        )

        self.link_sobre.bind(
            "<Button-1>",
            lambda e: self.abrir_janela_sobre()
        )

    # -------------------------------------------------
    # Atualização
    # -------------------------------------------------
    def update_prices(self):

        if self.update_job:
            self.after_cancel(self.update_job)

        for widget in self.table_rows:
            widget.destroy()

        self.table_rows.clear()

        data = get_crypto_data()

        if not data:
            self.last_update_label.configure(
                text="Erro ao obter dados."
            )

            self.update_job = self.after(
                30000,
                self.update_prices
            )

            return

        data_font = ctk.CTkFont(
            family=FONT_FAMILY,
            size=13
        )

        for row, coin_id in enumerate(ORDER, start=1):

            values = data.get(coin_id, {})

            usd = values.get("usd", 0.0)
            brl = values.get("brl", 0.0)

            labels = [
                ID_TO_TICKER.get(coin_id, coin_id),
                f"$ {usd:,.2f}",
                f"R$ {brl:,.2f}"
            ]

            for col, text in enumerate(labels):

                anchor = "w" if col == 0 else "e"

                lbl = ctk.CTkLabel(
                    self.table_frame,
                    text=text,
                    font=data_font,
                    anchor=anchor
                )

                lbl.grid(
                    row=row,
                    column=col,
                    sticky=anchor,
                    padx=8,
                    pady=2
                )

                self.table_rows.append(lbl)

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.last_update_label.configure(
            text=f"Última atualização: {now}"
        )

        self.update_job = self.after(
            30000,
            self.update_prices
        )

    # -------------------------------------------------
    # Sobre
    # -------------------------------------------------

    def abrir_janela_sobre(self):

        # Impede múltiplas janelas            
        if hasattr(self, "janela_sobre"):

            if self.janela_sobre is not None:

                if self.janela_sobre.winfo_exists():

                    self.janela_sobre.focus_force()
                    return

        self.janela_sobre = ctk.CTkToplevel(self)

        janela = self.janela_sobre

        # Evento de fechamento
        janela.protocol("WM_DELETE_WINDOW", self.fechar_janela_sobre)

        # Janela poup
        janela.title("Sobre o app")
        janela.configure(fg_color=BG_COLOR)

        # -----------------------------------
        # Ícone da popup (multiplataforma)
        # -----------------------------------
        try:

            # Windows
            if sys.platform.startswith("win") and os.path.exists(ICON_ICO):
                janela.iconbitmap(ICON_ICO)

            # Linux/macOS
            elif os.path.exists(ICON_PNG):

                janela.icon_img = tk.PhotoImage(file=ICON_PNG)
                janela.iconphoto(False, janela.icon_img)

        except Exception:
            pass

        # Configuração de tamanho-centralização:
        popup_width, popup_height = 350, 180

        tela_width = self.winfo_screenwidth()
        tela_height = self.winfo_screenheight()

        x = (tela_width // 2) - (popup_width // 2)
        y = (tela_height // 2) - (popup_height // 2)

        janela.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
        janela.resizable(False, False)

        info = (
            "Crypto API\n\n"
            "Visualizador de cotação de criptomoedas\n"
            "Interface: Python + CustomTkinter + API\n"
            "Desenvolvedor: Danilo dos Santos Soares\n"
            "Contato: (11) 9 4138-3504\n\n"
            "© 2026 - Todos os direitos reservados."
        )

        label = ctk.CTkLabel(
            janela,
            text=info,
            justify="left",
            font=ctk.CTkFont(size=14)
        )

        label.pack(padx=20, pady=20)

    def fechar_janela_sobre(self): 

        if self.janela_sobre is not None: 
            self.janela_sobre.destroy() 
            self.janela_sobre = None

if __name__ == "__main__":

    app = App()
    app.mainloop()
