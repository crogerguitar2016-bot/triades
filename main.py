from itertools import product
import os
from datetime import datetime

from kivy.app import App
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup


# ============================================================
# TRIADES
# PROFESSOR: CARLOS ROGÉRIO
# C ROGER
# Ensaio Avançado de Harmonia
# ============================================================


CAMPOS_HARMONICOS = {
    "C": {
        "C": ["C", "E", "G"],
        "Dm": ["D", "F", "A"],
        "Em": ["E", "G", "B"],
        "F": ["F", "A", "C"],
        "G": ["G", "B", "D"],
        "Am": ["A", "C", "E"],
        "B°": ["B", "D", "F"],
    },
    "G": {
        "G": ["G", "B", "D"],
        "Am": ["A", "C", "E"],
        "Bm": ["B", "D", "F#"],
        "C": ["C", "E", "G"],
        "D": ["D", "F#", "A"],
        "Em": ["E", "G", "B"],
        "F#°": ["F#", "A", "C"],
    },
    "D": {
        "D": ["D", "F#", "A"],
        "Em": ["E", "G", "B"],
        "F#m": ["F#", "A", "C#"],
        "G": ["G", "B", "D"],
        "A": ["A", "C#", "E"],
        "Bm": ["B", "D", "F#"],
        "C#°": ["C#", "E", "G"],
    },
    "A": {
        "A": ["A", "C#", "E"],
        "Bm": ["B", "D", "F#"],
        "C#m": ["C#", "E", "G#"],
        "D": ["D", "F#", "A"],
        "E": ["E", "G#", "B"],
        "F#m": ["F#", "A", "C#"],
        "G#°": ["G#", "B", "D"],
    },
    "E": {
        "E": ["E", "G#", "B"],
        "F#m": ["F#", "A", "C#"],
        "G#m": ["G#", "B", "D#"],
        "A": ["A", "C#", "E"],
        "B": ["B", "D#", "F#"],
        "C#m": ["C#", "E", "G#"],
        "D#°": ["D#", "F#", "A"],
    },
    "B": {
        "B": ["B", "D#", "F#"],
        "C#m": ["C#", "E", "G#"],
        "D#m": ["D#", "F#", "A#"],
        "E": ["E", "G#", "B"],
        "F#": ["F#", "A#", "C#"],
        "G#m": ["G#", "B", "D#"],
        "A#°": ["A#", "C#", "E"],
    },
    "F#": {
        "F#": ["F#", "A#", "C#"],
        "G#m": ["G#", "B", "D#"],
        "A#m": ["A#", "C#", "E#"],
        "B": ["B", "D#", "F#"],
        "C#": ["C#", "E#", "G#"],
        "D#m": ["D#", "F#", "A#"],
        "E#°": ["E#", "G#", "B"],
    },
    "F": {
        "F": ["F", "A", "C"],
        "Gm": ["G", "Bb", "D"],
        "Am": ["A", "C", "E"],
        "Bb": ["Bb", "D", "F"],
        "C": ["C", "E", "G"],
        "Dm": ["D", "F", "A"],
        "E°": ["E", "G", "Bb"],
    },
    "Bb": {
        "Bb": ["Bb", "D", "F"],
        "Cm": ["C", "Eb", "G"],
        "Dm": ["D", "F", "A"],
        "Eb": ["Eb", "G", "Bb"],
        "F": ["F", "A", "C"],
        "Gm": ["G", "Bb", "D"],
        "A°": ["A", "C", "Eb"],
    },
    "Eb": {
        "Eb": ["Eb", "G", "Bb"],
        "Fm": ["F", "Ab", "C"],
        "Gm": ["G", "Bb", "D"],
        "Ab": ["Ab", "C", "Eb"],
        "Bb": ["Bb", "D", "F"],
        "Cm": ["C", "Eb", "G"],
        "D°": ["D", "F", "Ab"],
    },
    "Ab": {
        "Ab": ["Ab", "C", "Eb"],
        "Bbm": ["Bb", "Db", "F"],
        "Cm": ["C", "Eb", "G"],
        "Db": ["Db", "F", "Ab"],
        "Eb": ["Eb", "G", "Bb"],
        "Fm": ["F", "Ab", "C"],
        "G°": ["G", "Bb", "Db"],
    },
    "Db": {
        "Db": ["Db", "F", "Ab"],
        "Ebm": ["Eb", "Gb", "Bb"],
        "Fm": ["F", "Ab", "C"],
        "Gb": ["Gb", "Bb", "Db"],
        "Ab": ["Ab", "C", "Eb"],
        "Bbm": ["Bb", "Db", "F"],
        "C°": ["C", "Eb", "Gb"],
    },
}


ACORDES_AUMENTADOS = {
    "C+": ["C", "E", "G#"],
    "C#+": ["C#", "F", "A"],
    "D+": ["D", "F#", "A#"],
    "D#+": ["D#", "G", "B"],
    "E+": ["E", "G#", "B#"],
    "F+": ["F", "A", "C#"],
    "F#+": ["F#", "A#", "D"],
    "G+": ["G", "B", "D#"],
    "G#+": ["G#", "C", "E"],
    "A+": ["A", "C#", "F"],
    "A#+": ["A#", "D", "F#"],
    "B+": ["B", "D#", "G"],
    "Fb+": ["Fb", "Ab", "C"],
}


def normalize_note_input(text):
    text = text.strip()
    text = text.replace("♯", "#")
    text = text.replace("♭", "b")

    if not text:
        return ""

    if len(text) == 1:
        return text.upper()

    return text[0].upper() + text[1:]


def obter_colunas(notas, campo_escolhido):
    colunas = []

    if campo_escolhido == "ATONAL":

        todos_acordes = []

        for campo in CAMPOS_HARMONICOS.values():
            for acorde, notas_acorde in campo.items():
                item = (acorde, notas_acorde)

                if item not in todos_acordes:
                    todos_acordes.append(item)

        for acorde, notas_acorde in ACORDES_AUMENTADOS.items():
            item = (acorde, notas_acorde)

            if item not in todos_acordes:
                todos_acordes.append(item)

        for nota in notas:
            coluna = []

            for acorde, notas_acorde in todos_acordes:
                if nota in notas_acorde and acorde not in coluna:
                    coluna.append(acorde)

            colunas.append(coluna)

    else:

        campo = CAMPOS_HARMONICOS.get(campo_escolhido)

        if not campo:
            return []

        for nota in notas:

            raizes = []
            terceiras = []
            quintas = []

            for acorde, notas_acorde in campo.items():

                if len(notas_acorde) >= 1 and nota == notas_acorde[0]:
                    raizes.append(acorde)

                elif len(notas_acorde) >= 2 and nota == notas_acorde[1]:
                    terceiras.append(acorde)

                elif len(notas_acorde) >= 3 and nota == notas_acorde[2]:
                    quintas.append(acorde)

            coluna = []

            for lista in (raizes, terceiras, quintas):
                for acorde in lista:
                    if acorde not in coluna:
                        coluna.append(acorde)

            colunas.append(coluna)

    return colunas


def gerar_pdf(caminho, campo, notas, colunas, combinacoes):

    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
    except Exception as erro:
        raise RuntimeError(
            "O módulo ReportLab ainda não está disponível no APK.\n\n"
            "A interface está funcionando, mas o PDF será habilitado "
            "quando corrigirmos o empacotamento do ReportLab.\n\n"
            f"Detalhe: {erro}"
        )

    c = canvas.Canvas(caminho, pagesize=A4)

    largura, altura = A4

    y = altura - 50

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "PROFESSOR: CARLOS ROGÉRIO")

    y -= 22

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "C ROGER")

    y -= 22

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Ensaio Avançado de Harmonia")

    y -= 35

    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Campo Harmônico: {campo}")

    y -= 18

    texto_notas = ", ".join(notas)

    c.drawString(50, y, f"Notas digitadas: {texto_notas}")

    y -= 28

    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "Notas e acordes encontrados:")

    y -= 20

    c.setFont("Helvetica", 9)

    for indice, nota in enumerate(notas, start=1):

        coluna = colunas[indice - 1]

        linha = f"Col {indice} ({nota}): " + " | ".join(coluna)

        # Quebra simples para linhas muito grandes
        partes = []

        while len(linha) > 95:
            corte = linha.rfind(" | ", 0, 95)

            if corte <= 0:
                corte = 95

            partes.append(linha[:corte])
            linha = linha[corte:]

            if linha.startswith(" | "):
                linha = linha[3:]

        partes.append(linha)

        for parte in partes:

            c.drawString(50, y, parte)

            y -= 13

            if y < 60:
                c.showPage()
                c.setFont("Helvetica", 9)
                y = altura - 50

    y -= 10

    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "Combinações:")

    y -= 18

    c.setFont("Helvetica", 9)

    for indice, combinacao in enumerate(combinacoes, start=1):

        linha = f"{indice}. {' - '.join(combinacao)}"

        c.drawString(50, y, linha)

        y -= 13

        if y < 60:

            c.showPage()

            c.setFont("Helvetica", 9)

            y = altura - 50

    c.save()


class TelaPrincipal(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "vertical"
        self.padding = dp(12)
        self.spacing = dp(8)

        # ====================================================
        # CABEÇALHO
        # ====================================================

        cabecalho = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(105),
            spacing=dp(2),
        )

        titulo = Label(
            text="[b]TRIADES[/b]",
            markup=True,
            font_size="25sp",
            size_hint_y=None,
            height=dp(35),
        )

        professor = Label(
            text="[b]PROFESSOR: CARLOS ROGÉRIO[/b]",
            markup=True,
            font_size="16sp",
            size_hint_y=None,
            height=dp(25),
        )

        croger = Label(
            text="[b]C ROGER[/b]",
            markup=True,
            font_size="15sp",
            size_hint_y=None,
            height=dp(22),
        )

        ensaio = Label(
            text="Ensaio Avançado de Harmonia",
            font_size="14sp",
            size_hint_y=None,
            height=dp(22),
        )

        cabecalho.add_widget(titulo)
        cabecalho.add_widget(professor)
        cabecalho.add_widget(croger)
        cabecalho.add_widget(ensaio)

        self.add_widget(cabecalho)

        # ====================================================
        # ÁREA DE ENTRADA
        # ====================================================

        entrada = GridLayout(
            cols=1,
            size_hint_y=None,
            height=dp(150),
            spacing=dp(6),
        )

        entrada.add_widget(
            Label(
                text="Digite as notas separadas por vírgula:",
                halign="left",
                text_size=(None, None),
                size_hint_y=None,
                height=dp(25),
            )
        )

        self.notas_input = TextInput(
            hint_text="Ex.: C, E, G ou C, F#, Bb",
            multiline=False,
            size_hint_y=None,
            height=dp(45),
            font_size="17sp",
        )

        entrada.add_widget(self.notas_input)

        entrada.add_widget(
            Label(
                text="Escolha o Campo Harmônico:",
                halign="left",
                size_hint_y=None,
                height=dp(25),
            )
        )

        campos = list(CAMPOS_HARMONICOS.keys()) + ["ATONAL"]

        self.campo_spinner = Spinner(
            text="C",
            values=campos,
            size_hint_y=None,
            height=dp(45),
        )

        entrada.add_widget(self.campo_spinner)

        self.add_widget(entrada)

        # ====================================================
        # BOTÕES
        # ====================================================

        botoes = BoxLayout(
            size_hint_y=None,
            height=dp(48),
            spacing=dp(8),
        )

        btn_calcular = Button(
            text="CALCULAR",
            font_size="15sp",
        )

        btn_calcular.bind(on_release=self.calcular)

        btn_limpar = Button(
            text="LIMPAR",
            font_size="15sp",
        )

        btn_limpar.bind(on_release=self.limpar)

        botoes.add_widget(btn_calcular)
        botoes.add_widget(btn_limpar)

        self.add_widget(botoes)

        # ====================================================
        # BOTÃO PDF
        # ====================================================

        self.btn_pdf = Button(
            text="GERAR PDF",
            size_hint_y=None,
            height=dp(48),
            font_size="15sp",
            disabled=True,
        )

        self.btn_pdf.bind(on_release=self.gerar_pdf)

        self.add_widget(self.btn_pdf)

        # ====================================================
        # RESULTADOS
        # ====================================================

        scroll = ScrollView(
            do_scroll_x=False,
            do_scroll_y=True,
        )

        self.resultado = Label(
            text=(
                "[b]Pronto para começar.[/b]\n\n"
                "Digite as notas e toque em CALCULAR."
            ),
            markup=True,
            font_size="14sp",
            halign="left",
            valign="top",
            size_hint_y=None,
            padding=(dp(8), dp(8)),
        )

        self.resultado.bind(
            texture_size=self.atualizar_altura_resultado
        )

        scroll.add_widget(self.resultado)

        self.add_widget(scroll)

        self.colunas = []
        self.combinacoes = []
        self.notas = []

    def atualizar_altura_resultado(self, instance, tamanho):

        instance.height = max(
            tamanho[1] + dp(20),
            dp(100)
        )

    def mostrar_mensagem(self, titulo, mensagem):

        conteudo = BoxLayout(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(10),
        )

        texto = Label(
            text=mensagem,
            halign="center",
            valign="middle",
        )

        botao = Button(
            text="OK",
            size_hint_y=None,
            height=dp(45),
        )

        conteudo.add_widget(texto)
        conteudo.add_widget(botao)

        popup = Popup(
            title=titulo,
            content=conteudo,
            size_hint=(0.9, 0.55),
        )

        botao.bind(on_release=popup.dismiss)

        popup.open()

    def calcular(self, *args):

        texto = self.notas_input.text.strip()

        if not texto:

            self.mostrar_mensagem(
                "TRIADES",
                "Digite pelo menos uma nota.\n\n"
                "Exemplo: C, E, G"
            )

            return

        notas = [
            normalize_note_input(n)
            for n in texto.split(",")
            if n.strip()
        ]

        notas = [n for n in notas if n]

        if not notas:

            self.mostrar_mensagem(
                "TRIADES",
                "Nenhuma nota válida foi encontrada."
            )

            return

        campo = self.campo_spinner.text

        colunas = obter_colunas(notas, campo)

        if not colunas:

            self.mostrar_mensagem(
                "Erro",
                "Não foi possível encontrar o campo harmônico."
            )

            return

        for indice, coluna in enumerate(colunas):

            if not coluna:

                self.resultado.text = (
                    "[b]NENHUM ACORDE ENCONTRADO[/b]\n\n"
                    f"Nota: {notas[indice]}\n\n"
                    "Verifique a nota digitada e o campo escolhido."
                )

                self.btn_pdf.disabled = True

                return

        combinacoes = list(product(*colunas))

        self.notas = notas
        self.colunas = colunas
        self.combinacoes = combinacoes

        linhas = []

        linhas.append("[b]RESULTADO[/b]")
        linhas.append("")
        linhas.append(f"[b]Campo Harmônico:[/b] {campo}")
        linhas.append(f"[b]Notas:[/b] {', '.join(notas)}")
        linhas.append("")
        linhas.append("[b]ACORDES POR NOTA[/b]")
        linhas.append("")

        for indice, nota in enumerate(notas, start=1):

            coluna = colunas[indice - 1]

            linhas.append(
                f"[b]Coluna {indice} — {nota}[/b]"
            )

            linhas.append(
                " | ".join(coluna)
            )

            linhas.append("")

        linhas.append("[b]COMBINAÇÕES[/b]")
        linhas.append("")
        linhas.append(
            f"Total: {len(combinacoes)}"
        )
        linhas.append("")

        for indice, combinacao in enumerate(
            combinacoes,
            start=1
        ):

            linhas.append(
                f"{indice}. {' - '.join(combinacao)}"
            )

        self.resultado.text = "\n".join(linhas)

        self.btn_pdf.disabled = False

    def obter_pasta_pdf(self):

        # Primeiro tenta a pasta Download pública.
        candidatos = [
            "/storage/emulated/0/Download",
            "/sdcard/Download",
            "/storage/emulated/0/Downloads",
        ]

        for pasta in candidatos:

            try:

                if os.path.isdir(pasta) and os.access(
                    pasta,
                    os.W_OK
                ):
                    return pasta

            except Exception:
                pass

        # Fallback seguro: pasta privada do aplicativo.
        return App.get_running_app().user_data_dir

    def gerar_pdf(self, *args):

        if not self.combinacoes:

            self.mostrar_mensagem(
                "TRIADES",
                "Primeiro faça um cálculo."
            )

            return

        try:

            pasta = self.obter_pasta_pdf()

            os.makedirs(
                pasta,
                exist_ok=True
            )

            campo = self.campo_spinner.text

            data = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            nome = (
                f"TRIADES_{campo}_{data}.pdf"
            )

            caminho = os.path.join(
                pasta,
                nome
            )

            gerar_pdf(
                caminho,
                campo,
                self.notas,
                self.colunas,
                self.combinacoes,
            )

            self.mostrar_mensagem(
                "PDF GERADO",
                "PDF gerado com sucesso!\n\n"
                f"{caminho}"
            )

        except Exception as erro:

            self.mostrar_mensagem(
                "PDF",
                str(erro)
            )

    def limpar(self, *args):

        self.notas_input.text = ""
        self.campo_spinner.text = "C"

        self.resultado.text = (
            "[b]Pronto para começar.[/b]\n\n"
            "Digite as notas e toque em CALCULAR."
        )

        self.btn_pdf.disabled = True

        self.notas = []
        self.colunas = []
        self.combinacoes = []


class TriadesApp(App):

    title = "TRIADES"

    def build(self):

        return TelaPrincipal()


if __name__ == "__main__":
    TriadesApp().run()
