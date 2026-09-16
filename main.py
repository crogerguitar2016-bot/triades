# ============================================================
# BLOCO 1 DE 7
# CONFIGURAÇÕES E COLUNAS DE ACORDES
# ============================================================

import os
import threading

from itertools import product, permutations

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth

from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput


# ============================================================
# CONFIGURAÇÕES
# ============================================================

PASTA_DOWNLOAD = os.path.join(
    "/storage/emulated/0",
    "Download"
)

PASTA_DESTINO = os.path.join(
    PASTA_DOWNLOAD,
    "Harmonia Ensaio de Harmonia Avançada"
)

NOME_BASE = "combinacoes_acordes"

LIMITE_COMBINACOES_POR_PDF = 1_000_000

LIMITE_ALERTA_COMBINACOES = 10_000_000


# ============================================================
# COLUNAS DE ACORDES
# ============================================================

colunas = {

    "do": [
        "C",
        "C7+",
        "C7+9",
        "C7+9 11",
        "C7+9 11 13",
        "Am",
        "Am7",
        "Am7 9",
        "Am7 9 11",
        "Am7 9 11 13",
        "F",
        "F7+",
        "F7+9",
        "F7+9 11aum",
        "F7+9 11aum 13",
        "Dm7",
        "Dm7 9",
        "Dm7 9 11",
        "Dm7 9 11 13",
        "B°7 9",
        "B°7 9 11",
        "B°7 9 11 13",
        "G7 9 11",
        "G7 9 11 13",
        "Em7 9 11 13",
    ],

    "re": [
        "Dm",
        "Dm7",
        "Dm7 9",
        "Dm7 9 11",
        "Dm7 9 11 13",
        "B°",
        "B°7",
        "B°7 9",
        "B°7 9 11",
        "B°7 9 11 13",
        "G",
        "G7",
        "G7 9",
        "G7 9 11",
        "G7 9 11 13",
        "Em7",
        "Em7 9",
        "Em7 9 11",
        "Em7 9 11 13",
        "C7+9",
        "C7+9 11",
        "C7+9 11 13",
        "Am7 9 11",
        "Am7 9 11 13",
        "F7+9 11aum 13",
    ],

    "mi": [
        "Em",
        "Em7",
        "Em7 9",
        "Em7 9 11",
        "Em7 9 11 13",
        "C",
        "C7+",
        "C7+9",
        "C7+9 11",
        "C7+9 11 13",
        "Am",
        "Am7",
        "Am7 9",
        "Am7 9 11",
        "Am7 9 11 13",
        "F7+",
        "F7+9",
        "F7+9 11aum",
        "F7+9 11aum 13",
        "Dm7 9",
        "Dm7 9 11",
        "Dm7 9 11 13",
        "B°7 9 11",
        "B°7 9 11 13",
        "G7 9 11 13",
    ],

    "fa": [
        "F",
        "F7+",
        "F7+9",
        "F7+9 11",
        "F7+9 11 13",
        "Dm",
        "Dm7",
        "Dm7 9",
        "Dm7 9 11",
        "Dm7 9 11 13",
        "B°",
        "B°7",
        "B°7 9",
        "B°7 9 11",
        "B°7 9 11 13",
        "G7",
        "G7 9",
        "G7 9 11",
        "G7 9 11 13",
        "Em7 9",
        "Em7 9 11",
        "Em7 9 11 13",
        "C7+9 11",
        "C7+9 11 13",
        "Am7 9 11 13",
    ],

    "sol": [
        "G",
        "G7",
        "G7 9",
        "G7 9 11",
        "G7 9 11 13",
        "Em",
        "Em7",
        "Em7 9",
        "Em7 9 11",
        "Em7 9 11 13",
        "C",
        "C7+",
        "C7+9",
        "C7+9 11",
        "C7+9 11 13",
        "Am7",
        "Am7 9",
        "Am7 9 11",
        "Am7 9 11 13",
        "F7+9",
        "F7+9 11",
        "F7+9 11 13",
        "Dm7 9 11",
        "Dm7 9 11 13",
        "B°7 9 11 13",
    ],# ============================================================
# BLOCO 2 DE 7
# CONTINUAÇÃO DAS COLUNAS E FUNÇÕES MUSICAIS
# ============================================================

    "la": [
        "Am",
        "Am7",
        "Am7 9",
        "Am7 9 11",
        "Am7 9 11 13",
        "F",
        "F7+",
        "F7+9",
        "F7+9 11",
        "F7+9 11 13",
        "Dm",
        "Dm7",
        "Dm7 9",
        "Dm7 9 11",
        "Dm7 9 11 13",
        "B°7",
        "B°7 9",
        "B°7 9 11",
        "B°7 9 11 13",
        "G7 9",
        "G7 9 11",
        "G7 9 11 13",
        "Em7 9 11",
        "Em7 9 11 13",
        "C7+ 9 11 13",
    ],

    "si": [
        "B°",
        "B°7",
        "B°7 9",
        "B°7 9 11",
        "B°7 9 11 13",
        "G",
        "G7",
        "G7 9",
        "G7 9 11",
        "G7 9 11 13",
        "Em",
        "Em7",
        "Em7 9",
        "Em7 9 11",
        "Em7 9 11 13",
        "C7+",
        "C7+9",
        "C7+9 11",
        "C7+9 11 13",
        "Am7 9",
        "Am7 9 11",
        "Am7 9 11 13",
        "F7+9 11",
        "F7+9 11 13",
        "Dm7 9 11 13",
    ],
}


# ============================================================
# NORMALIZAR NOTA
# ============================================================

def normalizar_nota(nota):

    nota = nota.strip().lower()

    equivalencias = {
        "c": "do",
        "do": "do",
        "d": "re",
        "re": "re",
        "e": "mi",
        "mi": "mi",
        "f": "fa",
        "fa": "fa",
        "g": "sol",
        "sol": "sol",
        "a": "la",
        "la": "la",
        "b": "si",
        "si": "si",
    }

    return equivalencias.get(
        nota,
        ""
    )


# ============================================================
# QUANTIDADE DE VOZES
# ============================================================

def quantidade_de_vozes(acorde):

    texto = acorde.strip()

    # 7 VOZES
    if (
        "9 11 13" in texto
        or "9 11aum 13" in texto
    ):
        return 7

    # 6 VOZES
    if (
        "9 11" in texto
        or "9 11aum" in texto
    ):
        return 6

    # 5 VOZES
    if "9" in texto:
        return 5

    # 4 VOZES
    if "7+" in texto or "7" in texto:
        return 4

    # 3 VOZES
    return 3


# ============================================================
# OBTER COLUNA
# ============================================================

def obter_coluna(nota):

    return colunas.get(
        nota.lower(),
        []
    )


# ============================================================
# PREPARAR COLUNAS
# ============================================================

def preparar_colunas(
    notas,
    vozes
):

    resultado = []

    for nota in notas:

        coluna = obter_coluna(
            nota
        )

        filtrada = [
            acorde
            for acorde in coluna
            if quantidade_de_vozes(acorde)
            == vozes
        ]

        resultado.append(
            filtrada
        )

    return resultado


# ============================================================
# PREPARAR TODAS AS COLUNAS
# ============================================================

def preparar_colunas_todas(
    notas
):

    resultado = []

    for nota in notas:

        resultado.append(
            obter_coluna(nota)
        )

    return resultado


# ============================================================
# GERADOR NORMAL
# ============================================================

def gerar_combinacoes_normais(
    colunas,
    tamanho
):

    colunas_usadas = colunas[:tamanho]

    yield from product(
        *colunas_usadas
    )


# ============================================================
# GERADOR FATORIAL
# ============================================================

def gerar_combinacoes_fatoriais(
    colunas,
    tamanho
):

    colunas_usadas = colunas[:tamanho]

    for ordem in permutations(
        range(tamanho)
    ):

        colunas_ordenadas = [
            colunas_usadas[i]
            for i in ordem
        ]

        for combinacao in product(
            *colunas_ordenadas
        ):

            yield combinacao


# ============================================================
# TOTAL NORMAL
# ============================================================

def calcular_total_normal(
    colunas,
    tamanho
):

    total = 1

    for coluna in colunas[:tamanho]:

        total *= len(
            coluna
        )

    return total


# ============================================================
# TOTAL FATORIAL
# ============================================================

def calcular_total_fatorial(
    colunas,
    tamanho
):

    total_normal = calcular_total_normal(
        colunas,
        tamanho
    )

    fatorial = 1

    for numero in range(
        2,
        tamanho + 1
    ):

        fatorial *= numero

    return total_normal * fatorial


# ============================================================
# FORMATAR NÚMERO
# ============================================================

def formatar_numero(
    numero
):

    return f"{numero:,}".replace(
        ",",
        "."
    )# ============================================================
# BLOCO 3 DE 7
# FUNÇÕES DE TEXTO, CABEÇALHO E PDF
# ============================================================

def quebrar_texto(
    texto,
    largura_maxima,
    fonte="Helvetica",
    tamanho=9
):

    palavras = texto.split()

    linhas = []

    linha_atual = ""

    for palavra in palavras:

        tentativa = (
            palavra
            if not linha_atual
            else linha_atual + " " + palavra
        )

        if stringWidth(
            tentativa,
            fonte,
            tamanho
        ) <= largura_maxima:

            linha_atual = tentativa

        else:

            if linha_atual:

                linhas.append(
                    linha_atual
                )

            linha_atual = palavra

    if linha_atual:

        linhas.append(
            linha_atual
        )

    return linhas


# ============================================================
# PRÓXIMO NÚMERO DISPONÍVEL
# ============================================================

def proximo_numero_disponivel(
    sufixo=""
):

    numero = 1

    while True:

        nome = (
            f"{NOME_BASE}"
            f"{sufixo}_"
            f"{numero:04d}.pdf"
        )

        caminho = os.path.join(
            PASTA_DESTINO,
            nome
        )

        if not os.path.exists(
            caminho
        ):

            return numero

        numero += 1


# ============================================================
# NOME DE PDF DISPONÍVEL
# ============================================================

def nome_pdf_disponivel(
    numero,
    sufixo=""
):

    while True:

        nome = (
            f"{NOME_BASE}"
            f"{sufixo}_"
            f"{numero:04d}.pdf"
        )

        caminho = os.path.join(
            PASTA_DESTINO,
            nome
        )

        if not os.path.exists(
            caminho
        ):

            return caminho

        numero += 1


# ============================================================
# CABEÇALHO DINÂMICO
# ============================================================

def escrever_cabecalho_pdf(
    c,
    notas,
    tamanho,
    vozes,
    modo_fatorial,
    colunas_pdf,
    total
):

    largura, altura = A4

    margem = 35

    y = altura - 40

    # --------------------------------------------------------
    # TÍTULO
    # --------------------------------------------------------

    c.setFont(
        "Helvetica-Bold",
        14
    )

    c.drawCentredString(
        largura / 2,
        y,
        "ENSAIO AVANÇADO DE HARMONIA"
    )

    y -= 20

    c.setFont(
        "Helvetica-Bold",
        11
    )

    c.drawCentredString(
        largura / 2,
        y,
        "GERADOR DE COMBINAÇÕES DE ACORDES"
    )

    y -= 19

    c.setFont(
        "Helvetica-Bold",
        10
    )

    c.drawCentredString(
        largura / 2,
        y,
        "AUTOR DO APK: C ROGER"
    )

    y -= 24

    # --------------------------------------------------------
    # DADOS DA GERAÇÃO
    # --------------------------------------------------------

    c.setFont(
        "Helvetica",
        9
    )

    notas_texto = ", ".join(
        nota.upper()
        for nota in notas
    )

    c.drawString(
        margem,
        y,
        f"Notas utilizadas: {notas_texto}"
    )

    y -= 14

    c.drawString(
        margem,
        y,
        (
            "Quantidade de notas utilizadas: "
            f"{len(notas)}"
        )
    )

    y -= 14

    c.drawString(
        margem,
        y,
        f"Tamanho da combinação: {tamanho}"
    )

    y -= 14

    if vozes is None:

        tipo_texto = (
            "TODOS OS ACORDES"
        )

    else:

        nomes_vozes = {
            3: "TRÍADES (3 VOZES)",
            4: "TÉTRADES (4 VOZES)",
            5: "5 VOZES",
            6: "6 VOZES",
            7: "7 VOZES",
        }

        tipo_texto = nomes_vozes.get(
            vozes,
            f"{vozes} VOZES"
        )

    c.drawString(
        margem,
        y,
        f"Tipo de acorde: {tipo_texto}"
    )

    y -= 14

    if modo_fatorial:

        c.drawString(
            margem,
            y,
            "Modo de geração: FATORIAL"
        )

        y -= 14

    c.setFont(
        "Helvetica-Bold",
        9
    )

    c.drawString(
        margem,
        y,
        (
            "Total de combinações: "
            f"{formatar_numero(total)}"
        )
    )

    y -= 22

    # --------------------------------------------------------
    # ACORDES DISPONÍVEIS
    # --------------------------------------------------------

    c.setFont(
        "Helvetica-Bold",
        10
    )

    c.drawString(
        margem,
        y,
        "ACORDES DISPONÍVEIS POR NOTA:"
    )

    y -= 17

    for indice, nota in enumerate(
        notas
    ):

        acordes = colunas_pdf[
            indice
        ]

        c.setFont(
            "Helvetica-Bold",
            8
        )

        c.drawString(
            margem,
            y,
            (
                f"{nota.upper()} = "
                f"{len(acordes)} acordes"
            )
        )

        y -= 13

        c.setFont(
            "Helvetica",
            8
        )

        for numero, acorde in enumerate(
            acordes,
            1
        ):

            texto = (
                f"{numero}. {acorde}"
            )

            linhas = quebrar_texto(
                texto,
                largura - (margem * 2),
                "Helvetica",
                8
            )

            for linha in linhas:

                if y < 45:

                    c.showPage()

                    y = altura - 40

                    c.setFont(
                        "Helvetica",
                        8
                    )

                c.drawString(
                    margem,
                    y,
                    linha
                )

                y -= 11

        y -= 5

    return y


# ============================================================
# ESCREVER COMBINAÇÕES
# ============================================================

def escrever_combinacoes_pdf(
    c,
    gerador,
    quantidade,
    numero_pdf,
    callback=None
):

    largura, altura = A4

    margem = 35

    y = altura - 40

    tamanho_fonte = 8

    espacamento = 11

    largura_disponivel = (
        largura
        - (margem * 2)
    )

    c.setFont(
        "Helvetica",
        tamanho_fonte
    )

    contador_local = 0

    while (
        contador_local
        < quantidade
    ):

        combinacao = next(
            gerador
        )

        contador_local += 1

        texto = " | ".join(
            combinacao
        )

        linhas = quebrar_texto(
            texto,
            largura_disponivel,
            "Helvetica",
            tamanho_fonte
        )

        for linha in linhas:

            if y < 40:

                c.showPage()

                y = altura - 40

                c.setFont(
                    "Helvetica",
                    tamanho_fonte
                )

            c.drawString(
                margem,
                y,
                linha
            )

            y -= espacamento

        if (
            contador_local % 50_000 == 0
            or contador_local == quantidade
        ):

            if callback:

                callback(
                    (
                        f"PDF {numero_pdf}: "
                        f"{formatar_numero(contador_local)} "
                        "combinações escritas..."
                    )
                )

    return contador_local


# ============================================================
# GERAR PDFs
# ============================================================

def gerar_pdfs_intervalo(
    colunas,
    tamanho_combinacao,
    total_para_pdf,
    modo_fatorial=False,
    callback=None,
    notas=None,
    vozes=None
):

    os.makedirs(
        PASTA_DESTINO,
        exist_ok=True
    )

    if total_para_pdf <= 0:

        raise ValueError(
            "Não existem combinações para gerar."
        )

    # --------------------------------------------------------
    # GERADOR
    # --------------------------------------------------------

    if modo_fatorial:

        gerador = gerar_combinacoes_fatoriais(
            colunas,
            tamanho_combinacao
        )

    else:

        gerador = gerar_combinacoes_normais(
            colunas,
            tamanho_combinacao
        )

    # --------------------------------------------------------
    # SUFIXO
    # --------------------------------------------------------

    sufixo = (
        "_fatorial"
        if modo_fatorial
        else ""
    )

    restante = total_para_pdf

    quantidade_por_pdf = (
        LIMITE_COMBINACOES_POR_PDF
    )

    numero_pdf = (
        proximo_numero_disponivel(
            sufixo
        )
    )

    # --------------------------------------------------------
    # GERAR CADA PDF
    # --------------------------------------------------------

    while restante > 0:

        quantidade = min(
            quantidade_por_pdf,
            restante
        )

        caminho = nome_pdf_disponivel(
            numero_pdf,
            sufixo
        )

        if callback:

            callback(
                f"Iniciando PDF {numero_pdf}..."
            )

        c = canvas.Canvas(
            caminho,
            pagesize=A4
        )

        # ----------------------------------------------------
        # CABEÇALHO EM CADA PDF
        # ----------------------------------------------------

        escrever_cabecalho_pdf(
            c,
            notas,
            tamanho_combinacao,
            vozes,
            modo_fatorial,
            colunas,
            total_para_pdf
        )

        # ----------------------------------------------------
        # NOVA PÁGINA PARA AS COMBINAÇÕES
        # ----------------------------------------------------

        c.showPage()

        escrever_combinacoes_pdf(
            c,
            gerador,
            quantidade,
            numero_pdf,
            callback
        )

        c.save()

        restante -= quantidade

        if callback:

            callback(
                (
                    f"PDF {numero_pdf} concluído: "
                    f"{formatar_numero(quantidade)} "
                    "combinações."
                )
            )

        numero_pdf += 1

    if callback:

        callback(
            (
                "Todos os PDFs foram gerados.\n"
                f"Pasta: {PASTA_DESTINO}"
            )
        )# ============================================================
# BLOCO 4 DE 7
# INTERFACE KIVY
# ============================================================

class TelaPrincipal(BoxLayout):

    def __init__(
        self,
        **kwargs
    ):

        super().__init__(
            **kwargs
        )

        self.orientation = "vertical"

        self.padding = dp(10)

        self.spacing = dp(6)

        self.notas = []

        self.tamanho_combinacao = 0

        self.vozes_selecionadas = None

        self.modo_fatorial = False

        self.total_combinacoes = 0

        self.colunas_atuais = []

        # ====================================================
        # CABEÇALHO
        # ====================================================

        cabecalho = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(95),
            spacing=dp(1),
        )

        titulo = Label(
            text="[b]TRIADES[/b]",
            markup=True,
            font_size="24sp",
            size_hint_y=None,
            height=dp(32),
        )

        professor = Label(
            text="[b]PROFESSOR: CARLOS ROGÉRIO[/b]",
            markup=True,
            font_size="15sp",
            size_hint_y=None,
            height=dp(23),
        )

        croger = Label(
            text="[b]C ROGER[/b]",
            markup=True,
            font_size="14sp",
            size_hint_y=None,
            height=dp(20),
        )

        ensaio = Label(
            text="Ensaio Avançado de Harmonia",
            font_size="13sp",
            size_hint_y=None,
            height=dp(20),
        )

        cabecalho.add_widget(
            titulo
        )

        cabecalho.add_widget(
            professor
        )

        cabecalho.add_widget(
            croger
        )

        cabecalho.add_widget(
            ensaio
        )

        self.add_widget(
            cabecalho
        )

        # ====================================================
        # ENTRADA DAS NOTAS
        # ====================================================

        self.notas_input = TextInput(
            hint_text=(
                "Digite as notas separadas por espaços: "
                "do re mi fa sol"
            ),
            multiline=False,
            size_hint_y=None,
            height=dp(45),
            font_size="16sp",
        )

        self.add_widget(
            self.notas_input
        )

        # ====================================================
        # QUANTIDADE DE NOTAS
        # ====================================================

        linha_k = BoxLayout(
            size_hint_y=None,
            height=dp(42),
            spacing=dp(6),
        )

        label_k = Label(
            text="Quantidade de notas:",
            size_hint_x=0.55,
            font_size="14sp",
        )

        self.k_spinner = Spinner(
            text="3",
            values=[
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
            ],
            size_hint_x=0.45,
            font_size="14sp",
        )

        linha_k.add_widget(
            label_k
        )

        linha_k.add_widget(
            self.k_spinner
        )

        self.add_widget(
            linha_k
        )

        # ====================================================
        # ÁREA DOS BOTÕES
        # ====================================================

        scroll_botoes = ScrollView(
            size_hint_y=0.48,
            do_scroll_x=False,
        )

        botoes = GridLayout(
            cols=2,
            spacing=dp(5),
            padding=dp(2),
            size_hint_y=None,
        )

        botoes.bind(
            minimum_height=botoes.setter(
                "height"
            )
        )

        titulo_normal = Label(
            text="[b]COMBINAÇÕES NORMAIS[/b]",
            markup=True,
            font_size="14sp",
            size_hint_y=None,
            height=dp(30),
        )

        botoes.add_widget(
            titulo_normal
        )

        botoes.add_widget(
            Label(
                text="",
                size_hint_y=None,
                height=dp(30),
            )
        )

        # ====================================================
        # TRÍADES
        # ====================================================

        btn_triades = Button(
            text="TRÍADES\n3 VOZES",
            font_size="13sp",
            size_hint_y=None,
            height=dp(55),
        )

        btn_triades.bind(
            on_release=lambda x:
            self.selecionar_tipo(
                3,
                False
            )
        )

        botoes.add_widget(
            btn_triades
        )

        # ====================================================
        # TÉTRADES
        # ====================================================

        btn_tetrades = Button(
            text="TÉTRADES\n4 VOZES",
            font_size="13sp",
            size_hint_y=None,
            height=dp(55),
        )

        btn_tetrades.bind(
            on_release=lambda x:
            self.selecionar_tipo(
                4,
                False
            )
        )

        botoes.add_widget(
            btn_tetrades
        )

        # ====================================================
        # 5 VOZES
        # ====================================================

        btn_5 = Button(
            text="5 VOZES",
            font_size="13sp",
            size_hint_y=None,
            height=dp(55),
        )

        btn_5.bind(
            on_release=lambda x:
            self.selecionar_tipo(
                5,
                False
            )
        )

        botoes.add_widget(
            btn_5
        )

        # ====================================================
        # 6 VOZES
        # ====================================================

        btn_6 = Button(
            text="6 VOZES",
            font_size="13sp",
            size_hint_y=None,
            height=dp(55),
        )

        btn_6.bind(
            on_release=lambda x:
            self.selecionar_tipo(
                6,
                False
            )
        )

        botoes.add_widget(
            btn_6
        )

        # ====================================================
        # 7 VOZES
        # ====================================================

        btn_7 = Button(
            text="7 VOZES",
            font_size="13sp",
            size_hint_y=None,
            height=dp(55),
        )

        btn_7.bind(
            on_release=lambda x:
            self.selecionar_tipo(
                7,
                False
            )
        )

        botoes.add_widget(
            btn_7
        )

        # ====================================================
        # TODOS
        # ====================================================

        btn_todos = Button(
            text="TODOS OS\nACORDES",
            font_size="13sp",
            size_hint_y=None,
            height=dp(55),
        )

        btn_todos.bind(
            on_release=lambda x:
            self.selecionar_tipo(
                None,
                False
            )
        )

        botoes.add_widget(
            btn_todos
        )

        # ====================================================
        # TÍTULO FATORIAL
        # ====================================================

        titulo_fatorial = Label(
            text="[b]COMBINAÇÕES FATORIAIS[/b]",
            markup=True,
            font_size="14sp",
            size_hint_y=None,
            height=dp(30),
        )

        botoes.add_widget(
            titulo_fatorial
        )

        botoes.add_widget(
            Label(
                text="",
                size_hint_y=None,
                height=dp(30),
            )
        )

        # ====================================================
        # TRÍADES FATORIAL
        # ====================================================

        btn_triades_f = Button(
            text="TRÍADES\nFATORIAL",
            font_size="13sp",
            size_hint_y=None,
            height=dp(55),
        )

        btn_triades_f.bind(
            on_release=lambda x:
            self.selecionar_tipo(
                3,
                True
            )
        )

        botoes.add_widget(
            btn_triades_f
        )

        # ====================================================
        # TÉTRADES FATORIAL
        # ====================================================

        btn_tetrades_f = Button(
            text="TÉTRADES\nFATORIAL",
            font_size="13sp",
            size_hint_y=None,
            height=dp(55),
        )

        btn_tetrades_f.bind(
            on_release=lambda x:
            self.selecionar_tipo(
                4,
                True
            )
        )

        botoes.add_widget(
            btn_tetrades_f
        )

        # ====================================================
        # 5 VOZES FATORIAL
        # ====================================================

        btn_5_f = Button(
            text="5 VOZES\nFATORIAL",
            font_size="13sp",
            size_hint_y=None,
            height=dp(55),
        )

        btn_5_f.bind(
            on_release=lambda x:
            self.selecionar_tipo(
                5,
                True
            )
        )

        botoes.add_widget(
            btn_5_f
        )

        # ====================================================
        # 6 VOZES FATORIAL
        # ====================================================

        btn_6_f = Button(
            text="6 VOZES\nFATORIAL",
            font_size="13sp",
            size_hint_y=None,
            height=dp(55),
        )

        btn_6_f.bind(
            on_release=lambda x:
            self.selecionar_tipo(
                6,
                True
            )
        )

        botoes.add_widget(
            btn_6_f
        )

        # ====================================================
        # 7 VOZES FATORIAL
        # ====================================================

        btn_7_f = Button(
            text="7 VOZES\nFATORIAL",
            font_size="13sp",
            size_hint_y=None,
            height=dp(55),
        )

        btn_7_f.bind(
            on_release=lambda x:
            self.selecionar_tipo(
                7,
                True
            )
        )

        botoes.add_widget(
            btn_7_f
        )

        # ====================================================
        # TODOS FATORIAL
        # ====================================================

        btn_todos_f = Button(
            text="TODOS\nFATORIAL",
            font_size="13sp",
            size_hint_y=None,
            height=dp(55),
        )

        btn_todos_f.bind(
            on_release=lambda x:
            self.selecionar_tipo(
                None,
                True
            )
        )

        botoes.add_widget(
            btn_todos_f
        )

        scroll_botoes.add_widget(
            botoes
        )

        self.add_widget(
            scroll_botoes
        )# ============================================================
# BLOCO 5 DE 7
# RESULTADO E CONTROLE DA INTERFACE
# ============================================================

        # ====================================================
        # RESULTADO
        # ====================================================

        scroll_resultado = ScrollView(
            size_hint_y=0.30,
            do_scroll_x=False,
        )

        self.resultado = Label(
            text=(
                "[b]Pronto para começar.[/b]\n\n"
                "Digite as notas separadas por espaços "
                "e escolha uma opção."
            ),
            markup=True,
            font_size="13sp",
            halign="left",
            valign="top",
            size_hint_y=None,
            padding=(dp(8), dp(8)),
        )

        self.resultado.bind(
            texture_size=self.resultado.setter(
                "size"
            )
        )

        scroll_resultado.add_widget(
            self.resultado
        )

        self.add_widget(
            scroll_resultado
        )

        # ====================================================
        # BOTÃO LIMPAR
        # ====================================================

        btn_limpar = Button(
            text="LIMPAR",
            font_size="14sp",
            size_hint_y=None,
            height=dp(45),
        )

        btn_limpar.bind(
            on_release=self.limpar
        )

        self.add_widget(
            btn_limpar
        )


    # ========================================================
    # LIMPAR
    # ========================================================

    def limpar(
        self,
        *args
    ):

        self.notas_input.text = ""

        self.k_spinner.text = "3"

        self.notas = []

        self.tamanho_combinacao = 0

        self.vozes_selecionadas = None

        self.modo_fatorial = False

        self.total_combinacoes = 0

        self.colunas_atuais = []

        self.resultado.text = (
            "[b]Pronto para começar.[/b]\n\n"
            "Digite as notas separadas por espaços "
            "e escolha uma opção."
        )


    # ========================================================
    # LER NOTAS
    # ========================================================

    def ler_notas(
        self
    ):

        texto = (
            self.notas_input.text.strip()
        )

        if not texto:

            raise ValueError(
                "Digite pelo menos uma nota."
            )

        notas_digitadas = texto.split()

        notas_validas = []

        for nota in notas_digitadas:

            nota_normalizada = normalizar_nota(
                nota
            )

            if not nota_normalizada:

                raise ValueError(
                    f"Nota inválida: {nota}\n\n"
                    "Use notas como:\n"
                    "do re mi fa sol la si"
                )

            notas_validas.append(
                nota_normalizada
            )

        if not notas_validas:

            raise ValueError(
                "Nenhuma nota válida foi encontrada."
            )

        return notas_validas


    # ========================================================
    # SELECIONAR TIPO
    # ========================================================

    def selecionar_tipo(
        self,
        vozes,
        modo_fatorial=False
    ):

        try:

            notas = self.ler_notas()

            tamanho = int(
                self.k_spinner.text
            )

            if tamanho < 1:

                raise ValueError(
                    "A quantidade de notas deve "
                    "ser maior que zero."
                )

            if tamanho > 7:

                raise ValueError(
                    "A quantidade máxima é 7."
                )

            if tamanho > len(notas):

                raise ValueError(
                    "A quantidade de notas escolhida "
                    "é maior que a quantidade de notas "
                    "digitadas."
                )

            # ------------------------------------------------
            # SOMENTE AS PRIMEIRAS K NOTAS
            # ------------------------------------------------

            notas = notas[:tamanho]

            # ------------------------------------------------
            # PREPARAR COLUNAS
            # ------------------------------------------------

            if vozes is None:

                colunas_selecionadas = (
                    preparar_colunas_todas(
                        notas
                    )
                )

                vozes_texto = (
                    "TODOS OS ACORDES"
                )

            else:

                if vozes < 3 or vozes > 7:

                    raise ValueError(
                        "A quantidade de vozes deve "
                        "estar entre 3 e 7."
                    )

                colunas_selecionadas = (
                    preparar_colunas(
                        notas,
                        vozes
                    )
                )

                vozes_texto = (
                    f"{vozes} VOZES"
                )

            # ------------------------------------------------
            # VERIFICAR COLUNAS
            # ------------------------------------------------

            for indice, coluna in enumerate(
                colunas_selecionadas
            ):

                if not coluna:

                    raise ValueError(
                        "A nota "
                        f"{notas[indice].upper()} "
                        "não possui acordes suficientes "
                        "para esta opção."
                    )

            # ------------------------------------------------
            # CALCULAR TOTAL
            # ------------------------------------------------

            if modo_fatorial:

                total = calcular_total_fatorial(
                    colunas_selecionadas,
                    tamanho
                )

            else:

                total = calcular_total_normal(
                    colunas_selecionadas,
                    tamanho
                )

            # ------------------------------------------------
            # GUARDAR CONFIGURAÇÃO
            # ------------------------------------------------

            self.notas = notas

            self.tamanho_combinacao = tamanho

            self.vozes_selecionadas = vozes

            self.modo_fatorial = modo_fatorial

            self.total_combinacoes = total

            self.colunas_atuais = (
                colunas_selecionadas
            )

            # ------------------------------------------------
            # MOSTRAR RESULTADO
            # ------------------------------------------------

            modo_texto = (
                "FATORIAL"
                if modo_fatorial
                else "NORMAL"
            )

            notas_texto = " ".join(
                nota.upper()
                for nota in notas
            )

            self.resultado.text = (
                "[b]CONFIGURAÇÃO SELECIONADA[/b]\n\n"
                f"Notas utilizadas: {notas_texto}\n"
                f"Quantidade de notas: {tamanho}\n"
                f"Tipo: {vozes_texto}\n"
                f"Modo: {modo_texto}\n\n"
                "[b]Total de combinações:[/b]\n"
                f"{formatar_numero(total)}"
            )

            self.confirmar_pdf()

        except Exception as erro:

            self.mostrar_erro(
                str(erro)
            )


    # ========================================================
    # MOSTRAR ERRO
    # ========================================================

    def mostrar_erro(
        self,
        mensagem
    ):

        self.mostrar_popup_mensagem(
            "ERRO",
            mensagem
        )


    # ========================================================
    # CONFIRMAR GERAÇÃO
    # ========================================================

    def confirmar_pdf(
        self
    ):

        total = self.total_combinacoes

        mensagem = (
            "DESEJA GERAR OS PDFs?\n\n"
            "Total de combinações:\n"
            f"{formatar_numero(total)}"
        )

        if total >= LIMITE_ALERTA_COMBINACOES:

            mensagem += (
                "\n\nATENÇÃO:\n"
                "A quantidade de combinações é muito grande.\n"
                "A geração poderá demorar bastante e ocupar "
                "muito espaço de armazenamento."
            )

        mensagem += (
            "\n\nCada PDF terá no máximo "
            f"{formatar_numero(LIMITE_COMBINACOES_POR_PDF)} "
            "combinações."
        )

        popup = Popup(
            title="GERAR PDFs",
            size_hint=(0.90, 0.62),
            auto_dismiss=False,
        )

        layout = BoxLayout(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(10),
        )

        texto = Label(
            text=mensagem,
            font_size="14sp",
            halign="center",
            valign="middle",
        )

        texto.bind(
            size=lambda instance, value:
            setattr(
                instance,
                "text_size",
                value
            )
        )

        botoes = BoxLayout(
            size_hint_y=None,
            height=dp(48),
            spacing=dp(8),
        )

        btn_sim = Button(
            text="SIM",
            font_size="15sp",
        )

        btn_nao = Button(
            text="NÃO",
            font_size="15sp",
        )

        botoes.add_widget(
            btn_sim
        )

        botoes.add_widget(
            btn_nao
        )

        layout.add_widget(
            texto
        )

        layout.add_widget(
            botoes
        )

        popup.content = layout

        btn_nao.bind(
            on_release=popup.dismiss
        )

        btn_sim.bind(
            on_release=lambda x:
            self.iniciar_geracao_pdfs(
                popup
            )
        )

        popup.open()# ============================================================
# BLOCO 6 DE 7
# GERAÇÃO DOS PDFs E PROGRESSO
# ============================================================

    # ========================================================
    # INICIAR GERAÇÃO
    # ========================================================

    def iniciar_geracao_pdfs(
        self,
        popup
    ):

        popup.dismiss()

        self.resultado.text = (
            "[b]GERAÇÃO DOS PDFs INICIADA[/b]\n\n"
            "Aguarde..."
        )

        thread = threading.Thread(
            target=self._gerar_pdfs_thread,
            daemon=True,
        )

        thread.start()


    # ========================================================
    # GERAÇÃO EM SEGUNDO PLANO
    # ========================================================

    def _gerar_pdfs_thread(
        self
    ):

        try:

            gerar_pdfs_intervalo(
                self.colunas_atuais,
                self.tamanho_combinacao,
                self.total_combinacoes,
                self.modo_fatorial,
                self.atualizar_progresso,
                self.notas,
                self.vozes_selecionadas,
            )

            Clock.schedule_once(
                lambda dt:
                self.geracao_concluida(),
                0
            )

        except Exception as erro:

            mensagem = str(
                erro
            )

            Clock.schedule_once(
                lambda dt:
                self.geracao_com_erro(
                    mensagem
                ),
                0
            )


    # ========================================================
    # ATUALIZAR PROGRESSO
    # ========================================================

    def atualizar_progresso(
        self,
        mensagem
    ):

        Clock.schedule_once(
            lambda dt:
            self._mostrar_progresso(
                mensagem
            ),
            0
        )


    def _mostrar_progresso(
        self,
        mensagem
    ):

        self.resultado.text = (
            "[b]GERANDO PDFs...[/b]\n\n"
            f"{mensagem}\n\n"
            "Pasta de destino:\n"
            f"{PASTA_DESTINO}"
        )


    # ========================================================
    # GERAÇÃO CONCLUÍDA
    # ========================================================

    def geracao_concluida(
        self
    ):

        self.resultado.text = (
            "[b]PDFs GERADOS COM SUCESSO![/b]\n\n"
            "Total de combinações:\n"
            f"{formatar_numero(self.total_combinacoes)}\n\n"
            "Pasta de destino:\n"
            f"{PASTA_DESTINO}"
        )

        self.mostrar_popup_mensagem(
            "CONCLUÍDO",
            (
                "Todos os PDFs foram gerados "
                "com sucesso!\n\n"
                f"Pasta:\n{PASTA_DESTINO}"
            )
        )


    # ========================================================
    # ERRO NA GERAÇÃO
    # ========================================================

    def geracao_com_erro(
        self,
        mensagem
    ):

        self.resultado.text = (
            "[b]ERRO NA GERAÇÃO DOS PDFs[/b]\n\n"
            f"{mensagem}"
        )

        self.mostrar_popup_mensagem(
            "ERRO",
            mensagem
        )


    # ========================================================
    # POPUP DE MENSAGEM
    # ========================================================

    def mostrar_popup_mensagem(
        self,
        titulo,
        mensagem
    ):

        popup = Popup(
            title=titulo,
            size_hint=(0.88, 0.55),
        )

        layout = BoxLayout(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(10),
        )

        texto = Label(
            text=mensagem,
            font_size="14sp",
            halign="center",
            valign="middle",
        )

        texto.bind(
            size=lambda instance, value:
            setattr(
                instance,
                "text_size",
                value
            )
        )

        botao = Button(
            text="OK",
            size_hint_y=None,
            height=dp(45),
        )

        botao.bind(
            on_release=popup.dismiss
        )

        layout.add_widget(
            texto
        )

        layout.add_widget(
            botao
        )

        popup.content = layout

        popup.open()# ============================================================
# BLOCO 7 DE 7
# FINAL DO APLICATIVO
# ============================================================


class TriadesApp(App):

    title = "TRIADES"

    def build(self):

        return TelaPrincipal()


# ============================================================
# INICIAR APLICATIVO
# ============================================================

if __name__ == "__main__":

    TriadesApp().run()