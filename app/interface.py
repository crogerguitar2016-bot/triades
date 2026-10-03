# -*- coding: utf-8 -*-

from pathlib import Path

from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp, sp
from kivy.properties import ListProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner

from app.servico_harmonia import (
    listar_blocos,
    listar_modos,
    calcular_resultado,
)

from app.servico_atonal import (
    calcular_resultado_atonal,
)

from app.tarefa_pdf import TarefaPDF
from app.tarefa_pdf_atonal import TarefaPDFAtonal

from app.armazenamento_pdf import (
    obter_pasta_saida_pdf,
    obter_destino_exibicao_pdf,
)


# ============================================================
# CAMINHOS
# ============================================================

BASE = Path(__file__).resolve().parent.parent

CAMINHO_LOGO = (
    BASE
    / "assets"
    / "imagens"
    / "logo_harmonia.png"
)



# ============================================================
# TONALIDADES
# ============================================================

TONALIDADES = (
    "C",
    "C#",
    "Db",
    "D",
    "D#",
    "Eb",
    "E",
    "F",
    "F#",
    "Gb",
    "G",
    "G#",
    "Ab",
    "A",
    "A#",
    "Bb",
    "B",
)


# ============================================================
# NOTAS DISPONÍVEIS PARA AS COLUNAS
# ============================================================

NOTAS_COLUNAS = (
    "C",
    "C#",
    "Db",
    "D",
    "D#",
    "Eb",
    "E",
    "F",
    "F#",
    "Gb",
    "G",
    "G#",
    "Ab",
    "A",
    "A#",
    "Bb",
    "B",
)


# ============================================================
# QUANTIDADE DE VOZES
# ============================================================

OPCOES_VOZES = (
    (3, "3 VOZES — TRÍADES"),
    (4, "4 VOZES — TÉTRADES / SÉTIMAS"),
    (5, "5 VOZES — ACORDES DE NONA"),
    (6, "6 VOZES — DÉCIMAS PRIMEIRAS"),
    (7, "7 VOZES — DÉCIMAS TERCEIRAS"),
    (0, "TODAS AS VOZES"),
)

# No ATONAL não existe a opção "todas as vozes".
# O usuário escolhe exatamente uma estrutura por vez.
OPCOES_VOZES_ATONAL = (
    (3, "3 VOZES — TRÍADES"),
    (4, "4 VOZES — TÉTRADES / SÉTIMAS"),
    (5, "5 VOZES — ACORDES DE NONA"),
    (6, "6 VOZES — DÉCIMAS PRIMEIRAS"),
    (7, "7 VOZES — DÉCIMAS TERCEIRAS"),
)

# Aviso informativo. Não bloqueia a geração por quantidade.
LIMITE_AVISO_COMBINACOES = 10_000_000
LIMITE_COMBINACOES_POR_PDF = 1_000_000


# ============================================================
# CORES
# ============================================================

COR_FUNDO = (
    0.055,
    0.065,
    0.12,
    1,
)

COR_BLOCO = (
    0.12,
    0.14,
    0.27,
    1,
)

COR_BLOCO_ATIVO = (
    0.29,
    0.36,
    0.62,
    1,
)

COR_BLOCO_DESATIVADO = (
    0.08,
    0.09,
    0.15,
    1,
)

COR_MODO = (
    0.17,
    0.20,
    0.36,
    1,
)

COR_MODO_ATIVO = (
    0.34,
    0.42,
    0.69,
    1,
)

COR_VOZ = (
    0.16,
    0.22,
    0.39,
    1,
)

COR_VOZ_ATIVA = (
    0.36,
    0.46,
    0.73,
    1,
)

COR_NOTA = (
    0.15,
    0.19,
    0.31,
    1,
)

COR_NOTA_ATIVA = (
    0.78,
    0.68,
    0.34,
    1,
)

COR_NOTA_TEXTO_ATIVO = (
    0.05,
    0.05,
    0.07,
    1,
)

COR_FECHAR = (
    0.34,
    0.15,
    0.17,
    1,
)

COR_VOLTAR = (
    0.18,
    0.19,
    0.27,
    1,
)

COR_LIMPAR = (
    0.30,
    0.19,
    0.16,
    1,
)

COR_PAINEL = (
    0.075,
    0.085,
    0.16,
    1,
)

COR_TEXTO = (
    1,
    1,
    1,
    1,
)

COR_TEXTO_DESATIVADO = (
    0.38,
    0.39,
    0.45,
    1,
)

COR_DESTAQUE = (
    0.92,
    0.78,
    0.40,
    1,
)

COR_CALCULAR = (
    0.78,
    0.66,
    0.30,
    1,
)

COR_CALCULAR_PRESSIONADO = (
    0.90,
    0.78,
    0.40,
    1,
)


# ============================================================
# BOTÃO ARREDONDADO BASE
# ============================================================

class BotaoArredondado(Button):

    cor_normal = ListProperty(
        COR_BLOCO
    )

    cor_pressionado = ListProperty(
        COR_BLOCO_ATIVO
    )

    cor_desativado = ListProperty(
        COR_BLOCO_DESATIVADO
    )

    raio = NumericProperty(
        dp(18)
    )

    def __init__(
        self,
        font_max=18,
        font_min=11,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.font_max = font_max
        self.font_min = font_min

        self.background_normal = ""
        self.background_down = ""

        self.background_color = (
            0,
            0,
            0,
            0,
        )

        self.color = (
            COR_TEXTO
        )

        self.disabled_color = (
            COR_TEXTO_DESATIVADO
        )

        self.halign = "center"
        self.valign = "middle"

        with self.canvas.before:

            self.cor_canvas = Color(
                *self.cor_normal
            )

            self.fundo_arredondado = (
                RoundedRectangle(
                    pos=self.pos,
                    size=self.size,
                    radius=[
                        self.raio,
                    ],
                )
            )

        self.bind(
            pos=self._atualizar_forma,
            size=self._atualizar_forma,
            state=self._atualizar_cor,
            disabled=self._atualizar_cor,
            text=self._ajustar_texto,
        )

        Clock.schedule_once(
            self._ajustar_texto,
            0,
        )

    def _atualizar_forma(
        self,
        *args
    ):
        self.fundo_arredondado.pos = (
            self.pos
        )

        self.fundo_arredondado.size = (
            self.size
        )

        self.fundo_arredondado.radius = [
            self.raio,
        ]

        self._ajustar_texto()

    def _atualizar_cor(
        self,
        *args
    ):
        if self.disabled:

            cor = (
                self.cor_desativado
            )

        elif self.state == "down":

            cor = (
                self.cor_pressionado
            )

        else:

            cor = (
                self.cor_normal
            )

        self.cor_canvas.rgba = cor

    def definir_cor(
        self,
        cor
    ):
        self.cor_normal = list(
            cor
        )

        self._atualizar_cor()

    def _ajustar_texto(
        self,
        *args
    ):
        largura = max(
            dp(40),
            self.width - dp(24),
        )

        altura = max(
            dp(20),
            self.height - dp(10),
        )

        self.text_size = (
            largura,
            altura,
        )

        tamanho = (
            self.font_max
        )

        quantidade = len(
            str(self.text)
        )

        if quantidade >= 34:

            tamanho = min(
                tamanho,
                11,
            )

        elif quantidade >= 28:

            tamanho = min(
                tamanho,
                12,
            )

        elif quantidade >= 23:

            tamanho = min(
                tamanho,
                13,
            )

        elif quantidade >= 18:

            tamanho = min(
                tamanho,
                14,
            )

        elif quantidade >= 14:

            tamanho = min(
                tamanho,
                16,
            )

        tamanho = max(
            tamanho,
            self.font_min,
        )

        self.font_size = sp(
            tamanho
        )


# ============================================================
# BOTÃO DE BLOCO
# ============================================================

class BotaoBloco(BotaoArredondado):

    def __init__(
        self,
        chave_bloco,
        titulo_bloco,
        callback,
        **kwargs
    ):
        super().__init__(
            font_max=18,
            font_min=13,
            **kwargs
        )

        self.chave_bloco = (
            chave_bloco
        )

        self.text = (
            titulo_bloco
        )

        self.bold = True

        self.size_hint_y = None

        self.height = (
            dp(62)
        )

        self.cor_normal = list(
            COR_BLOCO
        )

        self.cor_pressionado = list(
            COR_BLOCO_ATIVO
        )

        self.cor_desativado = list(
            COR_BLOCO_DESATIVADO
        )

        self.raio = dp(20)

        self._atualizar_cor()

        self.bind(
            on_release=lambda *_:
            callback(
                self.chave_bloco,
                self,
            )
        )


# ============================================================
# BOTÃO DE MODO
# ============================================================

class BotaoModo(BotaoArredondado):

    def __init__(
        self,
        chave_modo,
        nome_modo,
        callback,
        **kwargs
    ):
        super().__init__(
            font_max=16,
            font_min=11,
            **kwargs
        )

        self.chave_modo = (
            chave_modo
        )

        self.nome_modo = (
            nome_modo
        )

        self.text = (
            nome_modo
        )

        self.size_hint_y = None

        self.height = (
            dp(54)
        )

        self.cor_normal = list(
            COR_MODO
        )

        self.cor_pressionado = list(
            COR_MODO_ATIVO
        )

        self.raio = dp(17)

        self._atualizar_cor()

        self.bind(
            on_release=lambda *_:
            callback(
                self
            )
        )


# ============================================================
# BOTÃO DE VOZES
# ============================================================

class BotaoVoz(BotaoArredondado):

    def __init__(
        self,
        quantidade,
        texto,
        callback,
        **kwargs
    ):
        super().__init__(
            font_max=16,
            font_min=10,
            **kwargs
        )

        self.quantidade = (
            quantidade
        )

        self.text = (
            texto
        )

        self.size_hint_y = None

        self.height = (
            dp(58)
        )

        self.cor_normal = list(
            COR_VOZ
        )

        self.cor_pressionado = list(
            COR_VOZ_ATIVA
        )

        self.raio = dp(18)

        self._atualizar_cor()

        self.bind(
            on_release=lambda *_:
            callback(
                self
            )
        )


# ============================================================
# BOTÃO DE NOTA
# ============================================================

class BotaoNota(BotaoArredondado):

    def __init__(
        self,
        nota,
        callback,
        **kwargs
    ):
        super().__init__(
            font_max=17,
            font_min=13,
            **kwargs
        )

        self.nota = nota

        self.text = nota

        self.selecionado = False

        self.size_hint_y = None

        self.height = dp(52)

        self.cor_normal = list(
            COR_NOTA
        )

        self.cor_pressionado = list(
            COR_NOTA_ATIVA
        )

        self.raio = dp(16)

        self._atualizar_cor()

        self.bind(
            on_release=lambda *_:
            callback(
                self
            )
        )


# ============================================================
# BOTÃO FECHAR
# ============================================================

class BotaoFechar(BotaoArredondado):

    def __init__(
        self,
        callback,
        **kwargs
    ):
        super().__init__(
            font_max=14,
            font_min=11,
            **kwargs
        )

        self.text = (
            "FECHAR OPÇÕES"
        )

        self.bold = True

        self.size_hint_y = None

        self.height = dp(48)

        self.cor_normal = list(
            COR_FECHAR
        )

        self.cor_pressionado = [
            0.43,
            0.20,
            0.22,
            1,
        ]

        self.raio = dp(16)

        self._atualizar_cor()

        self.bind(
            on_release=lambda *_:
            callback()
        )


# ============================================================
# BOTÃO VOLTAR
# ============================================================

class BotaoVoltar(BotaoArredondado):

    def __init__(
        self,
        texto,
        callback,
        **kwargs
    ):
        super().__init__(
            font_max=14,
            font_min=10,
            **kwargs
        )

        self.text = texto

        self.bold = True

        self.size_hint_y = None

        self.height = dp(48)

        self.cor_normal = list(
            COR_VOLTAR
        )

        self.cor_pressionado = list(
            COR_BLOCO_ATIVO
        )

        self.raio = dp(16)

        self._atualizar_cor()

        self.bind(
            on_release=lambda *_:
            callback()
        )


# ============================================================
# BOTÃO LIMPAR
# ============================================================

class BotaoLimpar(BotaoArredondado):

    def __init__(
        self,
        callback,
        **kwargs
    ):
        super().__init__(
            font_max=14,
            font_min=11,
            **kwargs
        )

        self.text = (
            "LIMPAR NOTAS"
        )

        self.bold = True

        self.size_hint_y = None

        self.height = dp(48)

        self.cor_normal = list(
            COR_LIMPAR
        )

        self.cor_pressionado = list(
            COR_FECHAR
        )

        self.raio = dp(16)

        self._atualizar_cor()

        self.bind(
            on_release=lambda *_:
            callback()
        )


# ============================================================
# BOTÃO CALCULAR E GERAR PDF
# ============================================================

class BotaoCalcular(BotaoArredondado):

    def __init__(
        self,
        callback,
        **kwargs
    ):
        super().__init__(
            font_max=16,
            font_min=11,
            **kwargs
        )

        self.text = (
            "CALCULAR COMBINAÇÕES"
        )

        self.bold = True

        self.size_hint_y = None

        self.height = dp(60)

        self.cor_normal = list(
            COR_CALCULAR
        )

        self.cor_pressionado = list(
            COR_CALCULAR_PRESSIONADO
        )

        self.cor_desativado = list(
            COR_BLOCO_DESATIVADO
        )

        self.color = (
            COR_NOTA_TEXTO_ATIVO
        )

        self.disabled_color = (
            COR_TEXTO_DESATIVADO
        )

        self.raio = dp(19)

        self._atualizar_cor()

        self.bind(
            on_release=lambda *_:
            callback()
        )


# ============================================================
# PAINEL ARREDONDADO
# ============================================================

class PainelOpcoes(BoxLayout):

    def __init__(
        self,
        **kwargs
    ):
        super().__init__(
            orientation="vertical",
            spacing=dp(7),
            padding=[
                dp(10),
                dp(10),
                dp(10),
                dp(12),
            ],
            size_hint_y=None,
            **kwargs
        )

        self.height = 0

        self.opacity = 0

        with self.canvas.before:

            Color(
                *COR_PAINEL
            )

            self.fundo = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[
                    dp(20),
                ],
            )

        self.bind(
            pos=self._atualizar_fundo,
            size=self._atualizar_fundo,
        )

    def _atualizar_fundo(
        self,
        *args
    ):
        self.fundo.pos = (
            self.pos
        )

        self.fundo.size = (
            self.size
        )


# ============================================================
# TELA PRINCIPAL
# ============================================================

class TelaPrincipal(BoxLayout):

    def __init__(
        self,
        **kwargs
    ):
        super().__init__(
            orientation="vertical",
            **kwargs
        )

        self.tonica_selecionada = None

        self.bloco_aberto = None

        self.modo_selecionado = None

        self.nome_modo_selecionado = None

        self.vozes_selecionadas = None

        self.nome_vozes_selecionadas = None

        self.notas_selecionadas = []

        # Estado independente do módulo ATONAL.
        # As notas atonais ficam separadas das notas dos modos tonais,
        # permitindo selecioná-las antes ou depois de abrir o bloco ATONAL.
        self.sistema_selecionado = None
        self.vozes_atonais_selecionadas = None
        self.nome_vozes_atonais_selecionadas = None
        self.notas_atonais_selecionadas = []
        self.pre_selecao_atonal = False
        self.label_notas_atonal = None
        self.botao_calcular_atonal = None

        self.botoes_blocos = {}

        self.botoes_modos = []

        self.botoes_vozes = []

        self.botoes_notas = {}

        self.botao_calcular = None

        self.label_progresso = None

        self.label_detalhe_progresso = None

        self.tarefa_pdf = None

        self._ultimo_percentual_agendado = -1

        with self.canvas.before:

            Color(
                *COR_FUNDO
            )

            self.fundo = RoundedRectangle(
                pos=self.pos,
                size=self.size,
            )

        self.bind(
            pos=self._atualizar_fundo,
            size=self._atualizar_fundo,
        )

        self._montar_interface()


    # ========================================================
    # FUNDO
    # ========================================================

    def _atualizar_fundo(
        self,
        *args
    ):
        self.fundo.pos = (
            self.pos
        )

        self.fundo.size = (
            self.size
        )


    # ========================================================
    # LABEL CENTRAL
    # ========================================================

    def _label(
        self,
        texto,
        tamanho=15,
        altura=38,
        destaque=False,
    ):
        label = Label(
            text=texto,
            markup=True,
            color=(
                COR_DESTAQUE
                if destaque
                else COR_TEXTO
            ),
            font_size=f"{tamanho}sp",
            size_hint_y=None,
            height=dp(altura),
            halign="center",
            valign="middle",
        )

        label.bind(
            size=lambda obj, valor:
            setattr(
                obj,
                "text_size",
                valor,
            )
        )

        return label


    # ========================================================
    # MONTAR TELA
    # ========================================================

    def _montar_interface(
        self
    ):
        self.scroll_principal = ScrollView(
            do_scroll_x=False,
            do_scroll_y=True,
            scroll_type=[
                "content",
                "bars",
            ],
            bar_width=dp(9),
        )

        self.conteudo = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=[
                dp(14),
                dp(24),
                dp(14),
                dp(30),
            ],
            size_hint_y=None,
        )

        self.conteudo.bind(
            minimum_height=
            self.conteudo.setter(
                "height"
            )
        )

        self.scroll_principal.add_widget(
            self.conteudo
        )

        self.add_widget(
            self.scroll_principal
        )


        # ----------------------------------------------------
        # TÍTULO
        # ----------------------------------------------------

        self.conteudo.add_widget(
            self._label(
                "[b]HARMONIA FUNCIONAL AVANÇADA[/b]",
                tamanho=22,
                altura=52,
                destaque=True,
            )
        )


        # ----------------------------------------------------
        # LOGO INTERNA
        # ----------------------------------------------------

        area_imagem = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(190),
        )

        if CAMINHO_LOGO.exists():

            area_imagem.add_widget(
                Image(
                    source=str(
                        CAMINHO_LOGO
                    ),
                    allow_stretch=True,
                    keep_ratio=True,
                )
            )

        else:

            area_imagem.add_widget(
                self._label(
                    "[b]ESPAÇO PARA A IMAGEM[/b]",
                    tamanho=19,
                    altura=190,
                    destaque=True,
                )
            )

        self.conteudo.add_widget(
            area_imagem
        )


        # ----------------------------------------------------
        # AUTOR
        # ----------------------------------------------------

        self.conteudo.add_widget(
            self._label(
                "Autor do aplicativo: Carlos Rogério",
                tamanho=14,
                altura=30,
            )
        )


        # ----------------------------------------------------
        # TONALIDADE
        # ----------------------------------------------------

        self.conteudo.add_widget(
            self._label(
                "[b]ESCOLHA A TONALIDADE[/b]",
                tamanho=18,
                altura=38,
                destaque=True,
            )
        )


        self.spinner_tonalidade = Spinner(
            text="Selecione a tonalidade",
            values=TONALIDADES,
            size_hint_y=None,
            height=dp(58),
            font_size="18sp",
            background_normal="",
            background_down="",
            background_color=COR_BLOCO,
            color=COR_TEXTO,
        )

        self.spinner_tonalidade.bind(
            text=self.selecionar_tonalidade
        )

        self.conteudo.add_widget(
            self.spinner_tonalidade
        )


        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        self.status = self._label(
            "Escolha uma tonalidade para os modos ou use ATONAL",
            tamanho=14,
            altura=38,
        )

        self.conteudo.add_widget(
            self.status
        )


        # ----------------------------------------------------
        # 4 BLOCOS: 3 TONais + ATONAL
        # ----------------------------------------------------

        self.area_blocos = BoxLayout(
            orientation="vertical",
            spacing=dp(9),
            size_hint_y=None,
        )

        self.area_blocos.bind(
            minimum_height=
            self.area_blocos.setter(
                "height"
            )
        )

        # Os três blocos tonais continuam dependendo da tonalidade.
        for bloco in listar_blocos():

            botao = BotaoBloco(
                chave_bloco=
                bloco["chave"],

                titulo_bloco=
                bloco["titulo"],

                callback=
                self.abrir_bloco,
            )

            botao.disabled = True

            self.botoes_blocos[
                bloco["chave"]
            ] = botao

            self.area_blocos.add_widget(
                botao
            )

        # O ATONAL é independente de tonalidade/campo harmônico.
        botao_atonal = BotaoBloco(
            chave_bloco="atonal",
            titulo_bloco="ATONAL",
            callback=self.abrir_bloco,
        )
        botao_atonal.disabled = False
        self.botoes_blocos["atonal"] = botao_atonal
        self.area_blocos.add_widget(botao_atonal)

        # Permite escolher as notas antes de entrar no ATONAL.
        self.botao_notas_atonal_inicio = BotaoVoltar(
            texto="SELECIONAR NOTAS PARA ATONAL",
            callback=self.selecionar_notas_atonal_antes,
        )
        self.area_blocos.add_widget(
            self.botao_notas_atonal_inicio
        )

        self.conteudo.add_widget(
            self.area_blocos
        )


        # ----------------------------------------------------
        # PAINEL DINÂMICO
        # ----------------------------------------------------

        self.painel_opcoes = (
            PainelOpcoes()
        )

        self.painel_opcoes.bind(
            minimum_height=
            self._altura_painel
        )

        self.conteudo.add_widget(
            self.painel_opcoes
        )


    # ========================================================
    # ALTURA DO PAINEL
    # ========================================================

    def _altura_painel(
        self,
        painel,
        altura
    ):
        if painel.opacity > 0:

            painel.height = altura

        else:

            painel.height = 0


    # ========================================================
    # TONALIDADE
    # ========================================================

    def selecionar_tonalidade(
        self,
        spinner,
        texto,
    ):
        if texto == (
            "Selecione a tonalidade"
        ):
            return

        self.tonica_selecionada = (
            texto
        )

        self.sistema_selecionado = None
        self.bloco_aberto = None
        self.modo_selecionado = None
        self.nome_modo_selecionado = None
        self.vozes_selecionadas = None
        self.nome_vozes_selecionadas = None
        self.notas_selecionadas = []

        self._fechar_painel()

        for botao in (
            self.botoes_blocos.values()
        ):

            botao.disabled = False

            botao.definir_cor(
                COR_BLOCO
            )

        self.status.text = (
            f"Tonalidade: "
            f"[b]{texto}[/b] — "
            "escolha um bloco"
        )


    # ========================================================
    # FECHAR PAINEL
    # ========================================================

    def _fechar_painel(
        self
    ):
        self.painel_opcoes.clear_widgets()

        self.painel_opcoes.height = 0

        self.painel_opcoes.opacity = 0

        self.botoes_modos = []

        self.botoes_vozes = []

        self.botoes_notas = {}


    def fechar_opcoes(
        self
    ):
        self._fechar_painel()

        self.bloco_aberto = None
        self.modo_selecionado = None
        self.nome_modo_selecionado = None
        self.vozes_selecionadas = None
        self.nome_vozes_selecionadas = None
        self.notas_selecionadas = []

        for botao in (
            self.botoes_blocos.values()
        ):

            botao.definir_cor(
                COR_BLOCO
            )

        if self.tonica_selecionada:
            self.status.text = (
                f"Tonalidade: "
                f"[b]{self.tonica_selecionada}[/b] "
                "— escolha um bloco"
            )
        else:
            self.status.text = (
                "Escolha uma tonalidade para os modos ou use ATONAL"
            )


    # ========================================================
    # BLOCO
    # ========================================================

    def abrir_bloco(
        self,
        chave_bloco,
        botao_clicado,
    ):
        # ATONAL não depende da seleção de uma tonalidade.
        if chave_bloco == "atonal":
            self.sistema_selecionado = "atonal"
            self.bloco_aberto = "atonal"

            self.modo_selecionado = None
            self.nome_modo_selecionado = None
            self.vozes_atonais_selecionadas = None
            self.nome_vozes_atonais_selecionadas = None

            for botao in self.botoes_blocos.values():
                botao.definir_cor(COR_BLOCO)

            botao_clicado.definir_cor(
                COR_BLOCO_ATIVO
            )

            self._mostrar_vozes_atonal()
            return

        # Os três blocos tonais continuam exigindo tonalidade.
        if not self.tonica_selecionada:
            self.status.text = (
                "Escolha primeiro a tonalidade para usar os modos tonais"
            )
            return

        self.sistema_selecionado = "tonal"

        self.bloco_aberto = (
            chave_bloco
        )

        self.modo_selecionado = None
        self.nome_modo_selecionado = None
        self.vozes_selecionadas = None
        self.nome_vozes_selecionadas = None
        self.notas_selecionadas = []

        for botao in (
            self.botoes_blocos.values()
        ):

            botao.definir_cor(
                COR_BLOCO
            )

        botao_clicado.definir_cor(
            COR_BLOCO_ATIVO
        )

        self._mostrar_modos(
            chave_bloco,
            botao_clicado.text,
        )


    # ========================================================
    # MODOS
    # ========================================================

    def _mostrar_modos(
        self,
        chave_bloco,
        titulo_bloco,
    ):
        self.painel_opcoes.clear_widgets()

        self.botoes_modos = []

        self.painel_opcoes.opacity = 1

        self.painel_opcoes.add_widget(
            self._label(
                f"[b]{titulo_bloco}[/b]",
                tamanho=17,
                altura=38,
                destaque=True,
            )
        )

        self.painel_opcoes.add_widget(
            BotaoFechar(
                callback=
                self.fechar_opcoes
            )
        )

        for modo in listar_modos(
            chave_bloco
        ):

            botao = BotaoModo(
                chave_modo=
                modo["chave"],

                nome_modo=
                modo["nome"],

                callback=
                self.selecionar_modo,
            )

            self.botoes_modos.append(
                botao
            )

            self.painel_opcoes.add_widget(
                botao
            )

        self.painel_opcoes.height = (
            self.painel_opcoes.minimum_height
        )

        self.status.text = (
            f"[b]{titulo_bloco}[/b] "
            "— escolha o campo harmônico"
        )


    def selecionar_modo(
        self,
        botao_clicado,
    ):
        self.modo_selecionado = (
            botao_clicado.chave_modo
        )

        self.nome_modo_selecionado = (
            botao_clicado.nome_modo
        )

        self.vozes_selecionadas = None
        self.nome_vozes_selecionadas = None
        self.notas_selecionadas = []

        self._mostrar_vozes()


    # ========================================================
    # VOZES
    # ========================================================

    def _mostrar_vozes(
        self
    ):
        self.painel_opcoes.clear_widgets()

        self.botoes_vozes = []

        self.painel_opcoes.opacity = 1

        self.painel_opcoes.add_widget(
            self._label(
                (
                    f"[b]"
                    f"{self.tonica_selecionada} "
                    f"{self.nome_modo_selecionado}"
                    f"[/b]"
                ),
                tamanho=18,
                altura=42,
                destaque=True,
            )
        )

        self.painel_opcoes.add_widget(
            self._label(
                "[b]ESCOLHA A QUANTIDADE DE VOZES[/b]",
                tamanho=15,
                altura=38,
            )
        )

        self.painel_opcoes.add_widget(
            BotaoVoltar(
                texto="VOLTAR AOS CAMPOS",
                callback=
                self.voltar_aos_campos,
            )
        )

        for quantidade, texto in (
            OPCOES_VOZES
        ):

            botao = BotaoVoz(
                quantidade=
                quantidade,

                texto=
                texto,

                callback=
                self.selecionar_vozes,
            )

            self.botoes_vozes.append(
                botao
            )

            self.painel_opcoes.add_widget(
                botao
            )

        self.painel_opcoes.height = (
            self.painel_opcoes.minimum_height
        )

        self.status.text = (
            f"[b]"
            f"{self.tonica_selecionada} "
            f"{self.nome_modo_selecionado}"
            f"[/b] — escolha as vozes"
        )


    def voltar_aos_campos(
        self
    ):
        if not self.bloco_aberto:
            return

        botao = (
            self.botoes_blocos[
                self.bloco_aberto
            ]
        )

        self.modo_selecionado = None
        self.nome_modo_selecionado = None
        self.vozes_selecionadas = None
        self.nome_vozes_selecionadas = None
        self.notas_selecionadas = []

        self._mostrar_modos(
            self.bloco_aberto,
            botao.text,
        )


    def selecionar_vozes(
        self,
        botao_clicado,
    ):
        self.vozes_selecionadas = (
            botao_clicado.quantidade
        )

        self.nome_vozes_selecionadas = (
            botao_clicado.text
        )

        self.notas_selecionadas = []

        self._mostrar_notas()


    # ========================================================
    # NOTAS DAS COLUNAS
    # ========================================================

    def _mostrar_notas(
        self
    ):
        self.painel_opcoes.clear_widgets()

        self.botoes_notas = {}

        self.painel_opcoes.opacity = 1


        self.painel_opcoes.add_widget(
            self._label(
                (
                    f"[b]"
                    f"{self.tonica_selecionada} "
                    f"{self.nome_modo_selecionado}"
                    f"[/b]"
                ),
                tamanho=18,
                altura=42,
                destaque=True,
            )
        )


        self.painel_opcoes.add_widget(
            self._label(
                (
                    f"[b]"
                    f"{self.nome_vozes_selecionadas}"
                    f"[/b]"
                ),
                tamanho=14,
                altura=38,
            )
        )


        self.painel_opcoes.add_widget(
            self._label(
                (
                    "[b]ESCOLHA AS NOTAS "
                    "PARA AS COLUNAS[/b]"
                ),
                tamanho=16,
                altura=42,
                destaque=True,
            )
        )


        self.painel_opcoes.add_widget(
            self._label(
                (
                    "Você pode selecionar "
                    "mais de uma nota."
                ),
                tamanho=13,
                altura=30,
            )
        )


        # ----------------------------------------------------
        # GRADE DE NOTAS
        # ----------------------------------------------------

        grade = GridLayout(
            cols=4,
            spacing=dp(7),
            size_hint_y=None,
        )

        grade.bind(
            minimum_height=
            grade.setter(
                "height"
            )
        )


        for nota in NOTAS_COLUNAS:

            botao = BotaoNota(
                nota=nota,
                callback=
                self.alternar_nota,
            )

            if nota in self.notas_selecionadas:

                botao.selecionado = True

                botao.definir_cor(
                    COR_NOTA_ATIVA
                )

                botao.color = (
                    COR_NOTA_TEXTO_ATIVO
                )

            self.botoes_notas[
                nota
            ] = botao

            grade.add_widget(
                botao
            )


        self.painel_opcoes.add_widget(
            grade
        )


        # ----------------------------------------------------
        # MOSTRAR NOTAS SELECIONADAS
        # ----------------------------------------------------

        self.label_notas = self._label(
            "Notas selecionadas: nenhuma",
            tamanho=14,
            altura=46,
        )

        self.painel_opcoes.add_widget(
            self.label_notas
        )


        self.botao_calcular = BotaoCalcular(
            callback=
            self.iniciar_calculo_pdf
        )

        self.botao_calcular.disabled = (
            not bool(
                self.notas_selecionadas
            )
        )

        self.painel_opcoes.add_widget(
            self.botao_calcular
        )


        self.painel_opcoes.add_widget(
            BotaoLimpar(
                callback=
                self.limpar_notas
            )
        )


        self.painel_opcoes.add_widget(
            BotaoVoltar(
                texto="VOLTAR ÀS VOZES",
                callback=
                self.voltar_as_vozes,
            )
        )


        self.painel_opcoes.height = (
            self.painel_opcoes.minimum_height
        )


        self.status.text = (
            "[b]Selecione as notas "
            "das colunas[/b]"
        )


        Clock.schedule_once(
            lambda dt:
            self.scroll_principal.scroll_to(
                self.painel_opcoes,
                padding=dp(12),
                animate=True,
            ),
            0.10,
        )


    # ========================================================
    # SELECIONAR / DESMARCAR NOTA
    # ========================================================

    def alternar_nota(
        self,
        botao
    ):
        nota = botao.nota

        if nota in self.notas_selecionadas:

            self.notas_selecionadas.remove(
                nota
            )

            botao.selecionado = False

            botao.definir_cor(
                COR_NOTA
            )

            botao.color = (
                COR_TEXTO
            )

        else:

            self.notas_selecionadas.append(
                nota
            )

            botao.selecionado = True

            botao.definir_cor(
                COR_NOTA_ATIVA
            )

            botao.color = (
                COR_NOTA_TEXTO_ATIVO
            )


        self._atualizar_notas()


    # ========================================================
    # ATUALIZAR TEXTO
    # ========================================================

    def _atualizar_notas(
        self
    ):
        if self.notas_selecionadas:

            texto = " - ".join(
                self.notas_selecionadas
            )

            self.label_notas.text = (
                f"Notas selecionadas: "
                f"[b]{texto}[/b]"
            )

        else:

            self.label_notas.text = (
                "Notas selecionadas: nenhuma"
            )


        if self.botao_calcular is not None:

            self.botao_calcular.disabled = (
                not bool(
                    self.notas_selecionadas
                )
            )


    # ========================================================
    # LIMPAR
    # ========================================================

    def limpar_notas(
        self
    ):
        self.notas_selecionadas = []

        for botao in (
            self.botoes_notas.values()
        ):

            botao.selecionado = False

            botao.definir_cor(
                COR_NOTA
            )

            botao.color = (
                COR_TEXTO
            )

        self._atualizar_notas()


    # ========================================================
    # ATONAL - NOTAS ANTES DO BLOCO
    # ========================================================

    def selecionar_notas_atonal_antes(
        self
    ):
        self.sistema_selecionado = "atonal"
        self.pre_selecao_atonal = True
        self._mostrar_notas_atonal(
            pre_selecao=True
        )


    # ========================================================
    # ATONAL - VOZES
    # ========================================================

    def _mostrar_vozes_atonal(
        self
    ):
        self.pre_selecao_atonal = False

        self.painel_opcoes.clear_widgets()
        self.botoes_vozes = []
        self.painel_opcoes.opacity = 1

        self.painel_opcoes.add_widget(
            self._label(
                "[b]ATONAL[/b]",
                tamanho=19,
                altura=42,
                destaque=True,
            )
        )

        self.painel_opcoes.add_widget(
            self._label(
                "Não utiliza campo harmônico nem modo.",
                tamanho=13,
                altura=32,
            )
        )

        if self.notas_atonais_selecionadas:
            texto_notas = " - ".join(
                self.notas_atonais_selecionadas
            )
            self.painel_opcoes.add_widget(
                self._label(
                    f"Notas já selecionadas: [b]{texto_notas}[/b]",
                    tamanho=13,
                    altura=38,
                )
            )
        else:
            self.painel_opcoes.add_widget(
                self._label(
                    "Notas selecionadas: nenhuma",
                    tamanho=13,
                    altura=34,
                )
            )

        self.painel_opcoes.add_widget(
            BotaoVoltar(
                texto="SELECIONAR / ALTERAR NOTAS",
                callback=self.selecionar_notas_atonal_antes,
            )
        )

        self.painel_opcoes.add_widget(
            self._label(
                "[b]ESCOLHA O TIPO DE ACORDE[/b]",
                tamanho=15,
                altura=38,
            )
        )

        for quantidade, texto in OPCOES_VOZES_ATONAL:
            botao = BotaoVoz(
                quantidade=quantidade,
                texto=texto,
                callback=self.selecionar_vozes_atonal,
            )
            self.botoes_vozes.append(botao)
            self.painel_opcoes.add_widget(botao)

        self.painel_opcoes.add_widget(
            BotaoFechar(
                callback=self.fechar_opcoes
            )
        )

        self.painel_opcoes.height = (
            self.painel_opcoes.minimum_height
        )

        self.status.text = (
            "[b]ATONAL[/b] — escolha tríade, tétrade, 5, 6 ou 7 vozes"
        )

        Clock.schedule_once(
            lambda dt:
            self.scroll_principal.scroll_to(
                self.painel_opcoes,
                padding=dp(12),
                animate=True,
            ),
            0.10,
        )


    def selecionar_vozes_atonal(
        self,
        botao_clicado,
    ):
        self.sistema_selecionado = "atonal"
        self.bloco_aberto = "atonal"

        self.vozes_atonais_selecionadas = (
            botao_clicado.quantidade
        )
        self.nome_vozes_atonais_selecionadas = (
            botao_clicado.text
        )

        # IMPORTANTE: não apaga as notas já selecionadas.
        self._mostrar_notas_atonal(
            pre_selecao=False
        )


    def voltar_as_vozes_atonais(
        self
    ):
        # IMPORTANTE: as notas permanecem selecionadas.
        self._mostrar_vozes_atonal()


    # ========================================================
    # ATONAL - NOTAS
    # ========================================================

    def _mostrar_notas_atonal(
        self,
        pre_selecao=False,
    ):
        self.pre_selecao_atonal = bool(
            pre_selecao
        )

        self.painel_opcoes.clear_widgets()
        self.botoes_notas = {}
        self.painel_opcoes.opacity = 1

        self.painel_opcoes.add_widget(
            self._label(
                "[b]ATONAL[/b]",
                tamanho=19,
                altura=42,
                destaque=True,
            )
        )

        if pre_selecao:
            subtitulo = (
                "Selecione as notas antes de escolher o tipo de acorde"
            )
        else:
            subtitulo = (
                self.nome_vozes_atonais_selecionadas
                or "Escolha as notas"
            )

        self.painel_opcoes.add_widget(
            self._label(
                f"[b]{subtitulo}[/b]",
                tamanho=14,
                altura=42,
            )
        )

        self.painel_opcoes.add_widget(
            self._label(
                "Você pode selecionar uma ou várias notas.",
                tamanho=13,
                altura=30,
            )
        )

        grade = GridLayout(
            cols=4,
            spacing=dp(7),
            size_hint_y=None,
        )
        grade.bind(
            minimum_height=
            grade.setter("height")
        )

        for nota in NOTAS_COLUNAS:
            botao = BotaoNota(
                nota=nota,
                callback=self.alternar_nota_atonal,
            )

            if nota in self.notas_atonais_selecionadas:
                botao.selecionado = True
                botao.definir_cor(
                    COR_NOTA_ATIVA
                )
                botao.color = (
                    COR_NOTA_TEXTO_ATIVO
                )

            self.botoes_notas[nota] = botao
            grade.add_widget(botao)

        self.painel_opcoes.add_widget(grade)

        self.label_notas_atonal = self._label(
            "Notas selecionadas: nenhuma",
            tamanho=14,
            altura=46,
        )
        self.painel_opcoes.add_widget(
            self.label_notas_atonal
        )

        self.botao_calcular_atonal = BotaoCalcular(
            callback=(
                self._continuar_para_atonal
                if pre_selecao
                else self._calcular_atonal_interface
            )
        )

        if pre_selecao:
            self.botao_calcular_atonal.text = (
                "CONTINUAR PARA ATONAL"
            )
        else:
            self.botao_calcular_atonal.text = (
                "CALCULAR COMBINAÇÕES"
            )

        self.botao_calcular_atonal.disabled = (
            not bool(
                self.notas_atonais_selecionadas
            )
        )

        self.painel_opcoes.add_widget(
            self.botao_calcular_atonal
        )

        self.painel_opcoes.add_widget(
            BotaoLimpar(
                callback=self.limpar_notas_atonais
            )
        )

        if pre_selecao:
            self.painel_opcoes.add_widget(
                BotaoVoltar(
                    texto="VOLTAR",
                    callback=self.fechar_opcoes,
                )
            )
        else:
            self.painel_opcoes.add_widget(
                BotaoVoltar(
                    texto="VOLTAR ÀS VOZES ATONAIS",
                    callback=self.voltar_as_vozes_atonais,
                )
            )

        self.painel_opcoes.height = (
            self.painel_opcoes.minimum_height
        )

        self._atualizar_notas_atonal()

        self.status.text = (
            "[b]ATONAL[/b] — selecione as notas das colunas"
        )

        Clock.schedule_once(
            lambda dt:
            self.scroll_principal.scroll_to(
                self.painel_opcoes,
                padding=dp(12),
                animate=True,
            ),
            0.10,
        )


    def alternar_nota_atonal(
        self,
        botao
    ):
        nota = botao.nota

        if nota in self.notas_atonais_selecionadas:
            self.notas_atonais_selecionadas.remove(
                nota
            )
            botao.selecionado = False
            botao.definir_cor(COR_NOTA)
            botao.color = COR_TEXTO
        else:
            self.notas_atonais_selecionadas.append(
                nota
            )
            botao.selecionado = True
            botao.definir_cor(
                COR_NOTA_ATIVA
            )
            botao.color = (
                COR_NOTA_TEXTO_ATIVO
            )

        self._atualizar_notas_atonal()


    def _atualizar_notas_atonal(
        self
    ):
        if self.label_notas_atonal is not None:
            if self.notas_atonais_selecionadas:
                texto = " - ".join(
                    self.notas_atonais_selecionadas
                )
                self.label_notas_atonal.text = (
                    f"Notas selecionadas: [b]{texto}[/b]"
                )
            else:
                self.label_notas_atonal.text = (
                    "Notas selecionadas: nenhuma"
                )

        if self.botao_calcular_atonal is not None:
            self.botao_calcular_atonal.disabled = (
                not bool(
                    self.notas_atonais_selecionadas
                )
            )


    def limpar_notas_atonais(
        self
    ):
        self.notas_atonais_selecionadas = []

        for botao in self.botoes_notas.values():
            botao.selecionado = False
            botao.definir_cor(COR_NOTA)
            botao.color = COR_TEXTO

        self._atualizar_notas_atonal()


    def _continuar_para_atonal(
        self
    ):
        if not self.notas_atonais_selecionadas:
            return

        self.sistema_selecionado = "atonal"
        self.bloco_aberto = "atonal"

        for botao in self.botoes_blocos.values():
            botao.definir_cor(COR_BLOCO)

        self.botoes_blocos["atonal"].definir_cor(
            COR_BLOCO_ATIVO
        )

        self._mostrar_vozes_atonal()


    # ========================================================
    # AVISO PARA CÁLCULOS MUITO GRANDES
    #
    # O aviso é apenas informativo. O usuário pode continuar
    # independentemente da quantidade total de combinações.
    # ========================================================


    # ========================================================
    # ETAPA_9_9_PREVIA_COMBINACOES
    #
    # Mostra as combinações antes de gerar qualquer PDF.
    # Apenas 200 combinações ficam na tela por vez.
    # Nenhuma lista gigante é criada em memória.
    # ========================================================

    def _combinacao_por_indice(
        self,
        listas,
        indice,
    ):
        """
        Obtém diretamente uma combinação do produto cartesiano
        sem percorrer todas as anteriores.

        A ordem é equivalente a itertools.product:
        a última coluna varia mais rapidamente.
        """
        combinacao = [
            None
        ] * len(listas)

        restante = int(
            indice
        )

        for posicao in range(
            len(listas) - 1,
            -1,
            -1,
        ):
            tamanho = len(
                listas[posicao]
            )

            if tamanho <= 0:
                return None

            restante, indice_local = divmod(
                restante,
                tamanho,
            )

            combinacao[posicao] = (
                listas[posicao][
                    indice_local
                ]
            )

        return combinacao


    def _mostrar_previa_combinacoes(
        self,
        resultado,
        sistema,
        pagina=0,
    ):
        limite_pagina = 200

        total = int(
            resultado[
                "total_combinacoes"
            ]
        )

        if total <= 0:
            self.painel_opcoes.clear_widgets()
            self.painel_opcoes.opacity = 1

            self.painel_opcoes.add_widget(
                self._label(
                    "[b]NENHUMA COMBINAÇÃO ENCONTRADA[/b]",
                    tamanho=18,
                    altura=48,
                    destaque=True,
                )
            )

            voltar = (
                lambda:
                self._mostrar_notas_atonal(
                    False
                )
                if sistema == "atonal"
                else self._mostrar_notas()
            )

            self.painel_opcoes.add_widget(
                BotaoVoltar(
                    texto="VOLTAR",
                    callback=voltar,
                )
            )

            self.painel_opcoes.height = (
                self.painel_opcoes.minimum_height
            )
            return

        total_paginas = (
            total
            + limite_pagina
            - 1
        ) // limite_pagina

        pagina = max(
            0,
            min(
                int(pagina),
                total_paginas - 1,
            ),
        )

        inicio = (
            pagina
            * limite_pagina
        )

        fim = min(
            inicio + limite_pagina,
            total,
        )

        listas = [
            [
                acorde["nome"]
                for acorde in coluna
            ]
            for coluna in resultado[
                "colunas"
            ]
        ]

        self.painel_opcoes.clear_widgets()
        self.painel_opcoes.opacity = 1

        titulo = (
            "COMBINAÇÕES ATONAIS"
            if sistema == "atonal"
            else "COMBINAÇÕES POSSÍVEIS"
        )

        self.painel_opcoes.add_widget(
            self._label(
                f"[b]{titulo}[/b]",
                tamanho=19,
                altura=48,
                destaque=True,
            )
        )

        if sistema == "atonal":
            descricao = (
                resultado[
                    "descricao_vozes"
                ]
            )
        else:
            descricao = (
                resultado[
                    "descricao_campo"
                ]
                + "\n"
                + resultado[
                    "descricao_vozes"
                ]
            )

        self.painel_opcoes.add_widget(
            self._label(
                descricao,
                tamanho=13,
                altura=58,
            )
        )

        self.painel_opcoes.add_widget(
            self._label(
                (
                    "Notas: "
                    + " - ".join(
                        resultado[
                            "notas_exibicao"
                        ]
                    )
                ),
                tamanho=13,
                altura=38,
            )
        )

        self.painel_opcoes.add_widget(
            self._label(
                (
                    "[b]TOTAL DE COMBINAÇÕES: "
                    f"{self._numero_pt(total)}"
                    "[/b]"
                ),
                tamanho=17,
                altura=46,
                destaque=True,
            )
        )

        self.painel_opcoes.add_widget(
            self._label(
                (
                    f"Página {self._numero_pt(pagina + 1)} "
                    f"de {self._numero_pt(total_paginas)}\n"
                    f"Mostrando {self._numero_pt(inicio + 1)} "
                    f"até {self._numero_pt(fim)}"
                ),
                tamanho=13,
                altura=52,
            )
        )

        # ----------------------------------------------------
        # Navegação superior
        # ----------------------------------------------------

        if pagina > 0:
            self.painel_opcoes.add_widget(
                BotaoVoltar(
                    texto="← PÁGINA ANTERIOR",
                    callback=lambda:
                    self._mostrar_previa_combinacoes(
                        resultado,
                        sistema,
                        pagina - 1,
                    ),
                )
            )

        if pagina + 1 < total_paginas:
            self.painel_opcoes.add_widget(
                BotaoVoltar(
                    texto="PRÓXIMA PÁGINA →",
                    callback=lambda:
                    self._mostrar_previa_combinacoes(
                        resultado,
                        sistema,
                        pagina + 1,
                    ),
                )
            )

        if pagina > 1:
            self.painel_opcoes.add_widget(
                BotaoVoltar(
                    texto="IR PARA A PRIMEIRA PÁGINA",
                    callback=lambda:
                    self._mostrar_previa_combinacoes(
                        resultado,
                        sistema,
                        0,
                    ),
                )
            )

        if pagina < total_paginas - 2:
            self.painel_opcoes.add_widget(
                BotaoVoltar(
                    texto="IR PARA A ÚLTIMA PÁGINA",
                    callback=lambda:
                    self._mostrar_previa_combinacoes(
                        resultado,
                        sistema,
                        total_paginas - 1,
                    ),
                )
            )

        # ----------------------------------------------------
        # Combinações desta página
        # ----------------------------------------------------

        for indice_global in range(
            inicio,
            fim,
        ):
            combinacao = (
                self._combinacao_por_indice(
                    listas,
                    indice_global,
                )
            )

            numero = (
                indice_global + 1
            )

            texto_combinacao = (
                "  |  ".join(
                    combinacao
                )
            )

            self.painel_opcoes.add_widget(
                self._label(
                    (
                        f"{numero:02d}. "
                        f"{texto_combinacao}"
                    ),
                    tamanho=11,
                    altura=48,
                )
            )

        # ----------------------------------------------------
        # Navegação inferior
        # ----------------------------------------------------

        if pagina > 0:
            self.painel_opcoes.add_widget(
                BotaoVoltar(
                    texto="← PÁGINA ANTERIOR",
                    callback=lambda:
                    self._mostrar_previa_combinacoes(
                        resultado,
                        sistema,
                        pagina - 1,
                    ),
                )
            )

        if pagina + 1 < total_paginas:
            self.painel_opcoes.add_widget(
                BotaoVoltar(
                    texto="PRÓXIMA PÁGINA →",
                    callback=lambda:
                    self._mostrar_previa_combinacoes(
                        resultado,
                        sistema,
                        pagina + 1,
                    ),
                )
            )

        # ----------------------------------------------------
        # Só agora aparece a opção de gerar PDF
        # ----------------------------------------------------

        botao_pdf = BotaoCalcular(
            callback=lambda:
            self._perguntar_gerar_pdf(
                resultado,
                sistema,
            )
        )

        botao_pdf.text = (
            "GERAR PDF"
        )

        self.painel_opcoes.add_widget(
            botao_pdf
        )

        voltar = (
            lambda:
            self._mostrar_notas_atonal(
                False
            )
            if sistema == "atonal"
            else self._mostrar_notas()
        )

        self.painel_opcoes.add_widget(
            BotaoVoltar(
                texto="VOLTAR ÀS NOTAS",
                callback=voltar,
            )
        )

        self.painel_opcoes.height = (
            self.painel_opcoes.minimum_height
        )

        self.status.text = (
            "[b]Confira as combinações antes de gerar o PDF[/b]"
        )

        Clock.schedule_once(
            lambda dt:
            setattr(
                self.scroll_principal,
                "scroll_y",
                1,
            ),
            0.05,
        )


    # ========================================================
    # PRIMEIRA CONFIRMAÇÃO
    # ========================================================

    def _perguntar_gerar_pdf(
        self,
        resultado,
        sistema,
    ):
        total = int(
            resultado[
                "total_combinacoes"
            ]
        )

        total_pdfs = (
            total
            + LIMITE_COMBINACOES_POR_PDF
            - 1
        ) // LIMITE_COMBINACOES_POR_PDF

        popup = Popup(
            title="GERAR PDF?",
            size_hint=(0.92, 0.58),
            auto_dismiss=False,
        )

        layout = BoxLayout(
            orientation="vertical",
            padding=dp(14),
            spacing=dp(12),
        )

        mensagem = Label(
            text=(
                "[b]Deseja gerar o PDF com estas combinações?[/b]\n\n"
                f"Total: {self._numero_pt(total)} combinações\n"
                f"Quantidade prevista: {self._numero_pt(total_pdfs)} PDF(s)\n\n"
                "Nenhum PDF será criado até você confirmar."
            ),
            markup=True,
            halign="center",
            valign="middle",
        )

        mensagem.bind(
            size=lambda obj, valor:
            setattr(
                obj,
                "text_size",
                valor,
            )
        )

        botoes = BoxLayout(
            size_hint_y=None,
            height=dp(54),
            spacing=dp(10),
        )

        botao_sim = Button(
            text="SIM, GERAR PDF",
            bold=True,
            background_normal="",
            background_down="",
            background_color=(
                0.18,
                0.55,
                0.28,
                1,
            ),
            color=(
                1,
                1,
                1,
                1,
            ),
        )

        botao_nao = Button(
            text="NÃO",
            bold=True,
            background_normal="",
            background_down="",
            background_color=(
                0.55,
                0.18,
                0.18,
                1,
            ),
            color=(
                1,
                1,
                1,
                1,
            ),
        )

        botoes.add_widget(
            botao_sim
        )
        botoes.add_widget(
            botao_nao
        )

        layout.add_widget(
            mensagem
        )
        layout.add_widget(
            botoes
        )

        popup.content = layout

        botao_nao.bind(
            on_release=popup.dismiss
        )

        def confirmar(*_):
            popup.dismiss()

            if (
                total
                >= LIMITE_AVISO_COMBINACOES
            ):
                self._mostrar_aviso_calculo_grande(
                    total,
                    lambda:
                    self._iniciar_geracao_pdf(
                        sistema
                    ),
                )

            else:
                Clock.schedule_once(
                    lambda dt:
                    self._iniciar_geracao_pdf(
                        sistema
                    ),
                    0,
                )

        botao_sim.bind(
            on_release=confirmar
        )

        popup.open()


    # ========================================================
    # INÍCIO REAL DA GERAÇÃO
    # ========================================================

    def _iniciar_geracao_pdf(
        self,
        sistema,
    ):
        if (
            self.tarefa_pdf is not None
            and self.tarefa_pdf.em_execucao
        ):
            return

        self._ultimo_percentual_agendado = -1

        if sistema == "atonal":

            self.sistema_selecionado = (
                "atonal"
            )

            self._mostrar_progresso_pdf_atonal()

            self.tarefa_pdf = TarefaPDFAtonal(
                vozes=self.vozes_atonais_selecionadas,
                notas=list(
                    self.notas_atonais_selecionadas
                ),
                pasta_saida=obter_pasta_saida_pdf(),
                ao_progresso=self._callback_progresso_thread,
                ao_concluir=self._callback_concluido_thread,
                ao_erro=self._callback_erro_thread,
            )

        else:

            self.sistema_selecionado = (
                "tonal"
            )

            self._mostrar_progresso_pdf()

            self.tarefa_pdf = TarefaPDF(
                tonica=self.tonica_selecionada,
                modo=self.modo_selecionado,
                vozes=self.vozes_selecionadas,
                notas=list(
                    self.notas_selecionadas
                ),
                pasta_saida=obter_pasta_saida_pdf(),
                ao_progresso=self._callback_progresso_thread,
                ao_concluir=self._callback_concluido_thread,
                ao_erro=self._callback_erro_thread,
            )

        try:
            self.tarefa_pdf.iniciar()

        except Exception as erro:

            if sistema == "atonal":
                self._mostrar_erro_atonal(
                    str(erro)
                )

            else:
                self._mostrar_erro_pdf(
                    str(erro)
                )


    def _mostrar_aviso_calculo_grande(
        self,
        total,
        ao_continuar,
    ):
        total_pdfs = (
            total
            + LIMITE_COMBINACOES_POR_PDF
            - 1
        ) // LIMITE_COMBINACOES_POR_PDF

        popup = Popup(
            title="SEGUNDA CONFIRMAÇÃO — PDF MUITO GRANDE",
            size_hint=(0.94, 0.72),
            auto_dismiss=False,
        )

        layout = BoxLayout(
            orientation="vertical",
            padding=dp(14),
            spacing=dp(12),
        )

        mensagem = Label(
            text=(
                "[b]TEM CERTEZA QUE DESEJA CONTINUAR?[/b]\n\n"
                f"Total: {self._numero_pt(total)} combinações.\n\n"
                f"Serão gerados aproximadamente "
                f"{self._numero_pt(total_pdfs)} PDF(s), "
                "com no máximo "
                f"{self._numero_pt(LIMITE_COMBINACOES_POR_PDF)} "
                "combinações em cada arquivo.\n\n"
                "Essa operação pode demorar bastante "
                "e utilizar muito espaço de armazenamento."
            ),
            markup=True,
            halign="center",
            valign="middle",
        )

        mensagem.bind(
            size=lambda obj, valor:
            setattr(
                obj,
                "text_size",
                valor,
            )
        )

        botoes = BoxLayout(
            size_hint_y=None,
            height=dp(54),
            spacing=dp(10),
        )

        botao_continuar = Button(
            text="SIM, GERAR TODOS",
            bold=True,
            background_normal="",
            background_down="",
            background_color=(
                0.18,
                0.55,
                0.28,
                1,
            ),
            color=(1, 1, 1, 1),
        )

        botao_cancelar = Button(
            text="CANCELAR",
            bold=True,
            background_normal="",
            background_down="",
            background_color=(
                0.55,
                0.18,
                0.18,
                1,
            ),
            color=(1, 1, 1, 1),
        )

        botoes.add_widget(
            botao_continuar
        )
        botoes.add_widget(
            botao_cancelar
        )

        layout.add_widget(
            mensagem
        )
        layout.add_widget(
            botoes
        )

        popup.content = layout

        botao_cancelar.bind(
            on_release=popup.dismiss
        )

        def continuar(*_):
            popup.dismiss()

            Clock.schedule_once(
                lambda dt:
                ao_continuar(),
                0,
            )

        botao_continuar.bind(
            on_release=continuar
        )

        popup.open()


    def _calcular_atonal_interface(
        self,
    ):
        if not self.notas_atonais_selecionadas:
            return

        if self.vozes_atonais_selecionadas not in (
            3,
            4,
            5,
            6,
            7,
        ):
            return

        if (
            self.tarefa_pdf is not None
            and self.tarefa_pdf.em_execucao
        ):
            return

        try:
            resultado = calcular_resultado_atonal(
                notas=list(
                    self.notas_atonais_selecionadas
                ),
                vozes=self.vozes_atonais_selecionadas,
            )

        except Exception as erro:
            self._mostrar_erro_atonal(
                str(erro)
            )
            return

        self.sistema_selecionado = (
            "atonal"
        )

        self._mostrar_previa_combinacoes(
            resultado,
            "atonal",
            0,
        )


    def _mostrar_progresso_pdf_atonal(
        self
    ):
        self.painel_opcoes.clear_widgets()
        self.painel_opcoes.opacity = 1

        self.painel_opcoes.add_widget(
            self._label(
                "[b]SISTEMA ATONAL[/b]",
                tamanho=18,
                altura=42,
                destaque=True,
            )
        )

        self.painel_opcoes.add_widget(
            self._label(
                (
                    f"[b]"
                    f"{self.nome_vozes_atonais_selecionadas}"
                    f"[/b]"
                ),
                tamanho=14,
                altura=38,
            )
        )

        self.painel_opcoes.add_widget(
            self._label(
                (
                    "Notas: "
                    + " - ".join(
                        self.notas_atonais_selecionadas
                    )
                ),
                tamanho=13,
                altura=38,
            )
        )

        self.label_progresso = self._label(
            "[b]PREPARANDO PDF ATONAL...[/b]",
            tamanho=18,
            altura=50,
            destaque=True,
        )
        self.painel_opcoes.add_widget(
            self.label_progresso
        )

        self.label_detalhe_progresso = self._label(
            "Calculando e organizando as combinações ATONAIS.",
            tamanho=13,
            altura=52,
        )
        self.painel_opcoes.add_widget(
            self.label_detalhe_progresso
        )

        self.painel_opcoes.add_widget(
            self._label(
                "Não feche o aplicativo durante a geração.",
                tamanho=12,
                altura=38,
            )
        )

        self.painel_opcoes.height = (
            self.painel_opcoes.minimum_height
        )

        self.status.text = (
            "[b]Gerando PDF ATONAL...[/b]"
        )


    def _mostrar_resultado_pdf_atonal(
        self,
        fluxo
    ):
        resultado = fluxo["resultado"]
        arquivos = fluxo["arquivos"]

        self.painel_opcoes.clear_widgets()
        self.painel_opcoes.opacity = 1

        self.painel_opcoes.add_widget(
            self._label(
                "[b]PDF ATONAL GERADO COM SUCESSO[/b]",
                tamanho=19,
                altura=48,
                destaque=True,
            )
        )

        self.painel_opcoes.add_widget(
            self._label(
                "[b]ATONAL — não utiliza campo harmônico[/b]",
                tamanho=16,
                altura=40,
            )
        )

        self.painel_opcoes.add_widget(
            self._label(
                resultado["descricao_vozes"],
                tamanho=14,
                altura=36,
            )
        )

        self.painel_opcoes.add_widget(
            self._label(
                (
                    "Notas: "
                    + " - ".join(
                        resultado["notas_exibicao"]
                    )
                ),
                tamanho=13,
                altura=38,
            )
        )

        for nota, quantidade in (
            resultado["quantidades_por_nota"].items()
        ):
            self.painel_opcoes.add_widget(
                self._label(
                    (
                        f"{nota}: "
                        f"{self._numero_pt(quantidade)} acordes"
                    ),
                    tamanho=13,
                    altura=32,
                )
            )

        self.painel_opcoes.add_widget(
            self._label(
                (
                    "[b]TOTAL DE COMBINAÇÕES: "
                    f"{self._numero_pt(resultado['total_combinacoes'])}"
                    "[/b]"
                ),
                tamanho=16,
                altura=44,
                destaque=True,
            )
        )

        self.painel_opcoes.add_widget(
            self._label(
                (
                    "[b]PDFs gerados: "
                    f"{len(arquivos)}[/b]"
                ),
                tamanho=15,
                altura=38,
            )
        )

        limite_lista = 12

        for arquivo in arquivos[:limite_lista]:
            self.painel_opcoes.add_widget(
                self._label(
                    (
                        f"Parte {arquivo['parte']}/"
                        f"{arquivo['total_partes']}: "
                        f"{self._numero_pt(arquivo['inicio'])} "
                        f"até {self._numero_pt(arquivo['fim'])}\n"
                        f"{arquivo['nome']}"
                    ),
                    tamanho=11,
                    altura=58,
                )
            )

        if len(arquivos) > limite_lista:
            restantes = len(arquivos) - limite_lista
            self.painel_opcoes.add_widget(
                self._label(
                    (
                        f"... e mais {restantes} "
                        "arquivo(s) na mesma pasta."
                    ),
                    tamanho=12,
                    altura=42,
                )
            )

        self.painel_opcoes.add_widget(
            self._label(
                (
                    "Pasta:\n"
                    f"{obter_destino_exibicao_pdf()}"
                ),
                tamanho=10,
                altura=58,
            )
        )

        self.painel_opcoes.add_widget(
            BotaoVoltar(
                texto="VOLTAR ÀS VOZES ATONAIS",
                callback=self.voltar_as_vozes_atonais,
            )
        )

        self.painel_opcoes.add_widget(
            BotaoVoltar(
                texto="NOVO CÁLCULO",
                callback=self.novo_calculo,
            )
        )

        self.painel_opcoes.height = (
            self.painel_opcoes.minimum_height
        )

        self.status.text = (
            "[b]PDF ATONAL gerado com sucesso[/b]"
        )


    def _mostrar_erro_atonal(
        self,
        mensagem
    ):
        self.painel_opcoes.clear_widgets()
        self.painel_opcoes.opacity = 1

        self.painel_opcoes.add_widget(
            self._label(
                "[b]ERRO NO CÁLCULO ATONAL[/b]",
                tamanho=18,
                altura=46,
                destaque=True,
            )
        )

        self.painel_opcoes.add_widget(
            self._label(
                mensagem,
                tamanho=12,
                altura=90,
            )
        )

        self.painel_opcoes.add_widget(
            BotaoVoltar(
                texto="VOLTAR ÀS NOTAS",
                callback=lambda:
                self._mostrar_notas_atonal(False),
            )
        )

        self.painel_opcoes.height = (
            self.painel_opcoes.minimum_height
        )

        self.status.text = (
            "Erro no cálculo ATONAL"
        )


    # ========================================================
    # FORMATAÇÃO DE NÚMEROS
    # ========================================================

    def _numero_pt(
        self,
        numero
    ):
        return (
            f"{numero:,}"
            .replace(
                ",",
                "."
            )
        )


    # ========================================================
    # INICIAR CÁLCULO E PDF
    # ========================================================

    def iniciar_calculo_pdf(
        self,
    ):
        if not self.notas_selecionadas:
            return

        if (
            self.tarefa_pdf is not None
            and self.tarefa_pdf.em_execucao
        ):
            return

        try:
            resultado = calcular_resultado(
                tonica=self.tonica_selecionada,
                modo=self.modo_selecionado,
                vozes=self.vozes_selecionadas,
                notas=list(
                    self.notas_selecionadas
                ),
            )

        except Exception as erro:
            self._mostrar_erro_pdf(
                str(erro)
            )
            return

        self.sistema_selecionado = (
            "tonal"
        )

        self._mostrar_previa_combinacoes(
            resultado,
            "tonal",
            0,
        )


    def _mostrar_progresso_pdf(
        self
    ):
        self.painel_opcoes.clear_widgets()

        self.painel_opcoes.opacity = 1

        self.painel_opcoes.add_widget(
            self._label(
                (
                    f"[b]"
                    f"{self.tonica_selecionada} "
                    f"{self.nome_modo_selecionado}"
                    f"[/b]"
                ),
                tamanho=18,
                altura=42,
                destaque=True,
            )
        )

        self.painel_opcoes.add_widget(
            self._label(
                (
                    f"[b]"
                    f"{self.nome_vozes_selecionadas}"
                    f"[/b]"
                ),
                tamanho=14,
                altura=38,
            )
        )

        self.label_progresso = (
            self._label(
                "[b]PREPARANDO PDF...[/b]",
                tamanho=18,
                altura=50,
                destaque=True,
            )
        )

        self.painel_opcoes.add_widget(
            self.label_progresso
        )

        self.label_detalhe_progresso = (
            self._label(
                (
                    "Calculando e organizando "
                    "as combinações."
                ),
                tamanho=13,
                altura=52,
            )
        )

        self.painel_opcoes.add_widget(
            self.label_detalhe_progresso
        )

        self.painel_opcoes.add_widget(
            self._label(
                (
                    "Não feche o aplicativo "
                    "durante a geração."
                ),
                tamanho=12,
                altura=38,
            )
        )

        self.painel_opcoes.height = (
            self.painel_opcoes.minimum_height
        )

        self.status.text = (
            "[b]Gerando PDF...[/b]"
        )


    # ========================================================
    # CALLBACK DA THREAD - PROGRESSO
    #
    # Não altera Kivy diretamente.
    # ========================================================

    def _callback_progresso_thread(
        self,
        atual,
        total,
        parte,
        total_partes,
    ):
        if total <= 0:
            return

        percentual = int(
            atual
            * 100
            / total
        )

        if atual > 0:

            percentual = max(
                1,
                percentual,
            )

        percentual = min(
            100,
            percentual,
        )

        if (
            percentual
            ==
            self._ultimo_percentual_agendado
            and
            atual != total
        ):
            return

        self._ultimo_percentual_agendado = (
            percentual
        )

        Clock.schedule_once(
            lambda dt,
            p=percentual,
            a=atual,
            t=total,
            pt=parte,
            tp=total_partes:
            self._atualizar_progresso_ui(
                p,
                a,
                t,
                pt,
                tp,
            ),
            0,
        )


    # ========================================================
    # ATUALIZAR PROGRESSO NA THREAD DO KIVY
    # ========================================================

    def _atualizar_progresso_ui(
        self,
        percentual,
        atual,
        total,
        parte,
        total_partes,
    ):
        if self.label_progresso is not None:

            self.label_progresso.text = (
                f"[b]"
                f"GERANDO PDF — "
                f"{percentual}%"
                f"[/b]"
            )

        if (
            self.label_detalhe_progresso
            is not None
        ):

            self.label_detalhe_progresso.text = (
                f"{self._numero_pt(atual)} "
                f"de "
                f"{self._numero_pt(total)} "
                f"combinações\n"
                f"PDF {parte} de "
                f"{total_partes}"
            )


    # ========================================================
    # CALLBACK DE CONCLUSÃO
    # ========================================================

    def _callback_concluido_thread(
        self,
        fluxo
    ):
        resultado = fluxo.get(
            "resultado",
            {}
        )

        if resultado.get("sistema") == "atonal":
            Clock.schedule_once(
                lambda dt, f=fluxo:
                self._mostrar_resultado_pdf_atonal(
                    f
                ),
                0,
            )
        else:
            Clock.schedule_once(
                lambda dt, f=fluxo:
                self._mostrar_resultado_pdf(
                    f
                ),
                0,
            )


    # ========================================================
    # CALLBACK DE ERRO
    # ========================================================

    def _callback_erro_thread(
        self,
        erro
    ):
        mensagem = str(
            erro
        )

        if self.sistema_selecionado == "atonal":
            Clock.schedule_once(
                lambda dt, m=mensagem:
                self._mostrar_erro_atonal(
                    m
                ),
                0,
            )
        else:
            Clock.schedule_once(
                lambda dt, m=mensagem:
                self._mostrar_erro_pdf(
                    m
                ),
                0,
            )


    # ========================================================
    # RESULTADO FINAL
    # ========================================================

    def _mostrar_resultado_pdf(
        self,
        fluxo
    ):
        resultado = fluxo[
            "resultado"
        ]

        arquivos = fluxo[
            "arquivos"
        ]

        self.painel_opcoes.clear_widgets()

        self.painel_opcoes.opacity = 1

        self.painel_opcoes.add_widget(
            self._label(
                "[b]PDF GERADO COM SUCESSO[/b]",
                tamanho=19,
                altura=48,
                destaque=True,
            )
        )

        self.painel_opcoes.add_widget(
            self._label(
                (
                    f"[b]"
                    f"{resultado['descricao_campo']}"
                    f"[/b]"
                ),
                tamanho=17,
                altura=40,
            )
        )

        self.painel_opcoes.add_widget(
            self._label(
                resultado[
                    "descricao_vozes"
                ],
                tamanho=14,
                altura=36,
            )
        )

        self.painel_opcoes.add_widget(
            self._label(
                (
                    "Escala: "
                    + " - ".join(
                        resultado[
                            "escala_nomes"
                        ]
                    )
                ),
                tamanho=13,
                altura=42,
            )
        )

        self.painel_opcoes.add_widget(
            self._label(
                (
                    "Notas: "
                    + " - ".join(
                        resultado[
                            "notas_exibicao"
                        ]
                    )
                ),
                tamanho=13,
                altura=38,
            )
        )

        self.painel_opcoes.add_widget(
            self._label(
                (
                    "Acordes válidos: "
                    f"{resultado['quantidade_acordes']}"
                ),
                tamanho=13,
                altura=34,
            )
        )

        self.painel_opcoes.add_widget(
            self._label(
                (
                    "[b]TOTAL DE COMBINAÇÕES: "
                    f"{self._numero_pt(resultado['total_combinacoes'])}"
                    "[/b]"
                ),
                tamanho=16,
                altura=44,
                destaque=True,
            )
        )

        self.painel_opcoes.add_widget(
            self._label(
                (
                    "[b]PDFs gerados: "
                    f"{len(arquivos)}[/b]"
                ),
                tamanho=15,
                altura=38,
            )
        )

        limite_lista = 12

        for arquivo in arquivos[
            :limite_lista
        ]:

            self.painel_opcoes.add_widget(
                self._label(
                    (
                        f"Parte "
                        f"{arquivo['parte']}/"
                        f"{arquivo['total_partes']}: "
                        f"{self._numero_pt(arquivo['inicio'])} "
                        f"até "
                        f"{self._numero_pt(arquivo['fim'])}\n"
                        f"{arquivo['nome']}"
                    ),
                    tamanho=11,
                    altura=58,
                )
            )

        if len(arquivos) > limite_lista:

            restantes = (
                len(arquivos)
                - limite_lista
            )

            self.painel_opcoes.add_widget(
                self._label(
                    (
                        f"... e mais "
                        f"{restantes} "
                        f"arquivo(s) na mesma pasta."
                    ),
                    tamanho=12,
                    altura=42,
                )
            )

        self.painel_opcoes.add_widget(
            self._label(
                (
                    "Pasta:\n"
                    f"{obter_destino_exibicao_pdf()}"
                ),
                tamanho=10,
                altura=58,
            )
        )

        self.painel_opcoes.add_widget(
            BotaoVoltar(
                texto="NOVO CÁLCULO",
                callback=
                self.novo_calculo,
            )
        )

        self.painel_opcoes.height = (
            self.painel_opcoes.minimum_height
        )

        self.status.text = (
            "[b]PDF gerado com sucesso[/b]"
        )


    # ========================================================
    # ERRO NA GERAÇÃO
    # ========================================================

    def _mostrar_erro_pdf(
        self,
        mensagem
    ):
        self.painel_opcoes.clear_widgets()

        self.painel_opcoes.opacity = 1

        self.painel_opcoes.add_widget(
            self._label(
                "[b]ERRO AO GERAR PDF[/b]",
                tamanho=18,
                altura=46,
                destaque=True,
            )
        )

        self.painel_opcoes.add_widget(
            self._label(
                mensagem,
                tamanho=12,
                altura=90,
            )
        )

        self.painel_opcoes.add_widget(
            BotaoVoltar(
                texto="VOLTAR ÀS NOTAS",
                callback=
                self._mostrar_notas,
            )
        )

        self.painel_opcoes.height = (
            self.painel_opcoes.minimum_height
        )

        self.status.text = (
            "Erro durante a geração do PDF"
        )


    # ========================================================
    # NOVO CÁLCULO
    # ========================================================

    def novo_calculo(
        self
    ):
        self._fechar_painel()

        self.tonica_selecionada = None

        self.bloco_aberto = None

        self.modo_selecionado = None

        self.nome_modo_selecionado = None

        self.vozes_selecionadas = None

        self.nome_vozes_selecionadas = None

        self.notas_selecionadas = []

        self.sistema_selecionado = None
        self.vozes_atonais_selecionadas = None
        self.nome_vozes_atonais_selecionadas = None
        self.notas_atonais_selecionadas = []
        self.pre_selecao_atonal = False

        self.tarefa_pdf = None

        self.spinner_tonalidade.text = (
            "Selecione a tonalidade"
        )

        for chave, botao in (
            self.botoes_blocos.items()
        ):

            # ATONAL permanece disponível mesmo sem tonalidade.
            botao.disabled = (
                chave != "atonal"
            )

            botao.definir_cor(
                COR_BLOCO
            )

        self.status.text = (
            "Escolha uma tonalidade para os modos ou use ATONAL"
        )

        self.scroll_principal.scroll_y = 1


    # ========================================================
    # VOLTAR ÀS VOZES
    # ========================================================

    def voltar_as_vozes(
        self
    ):
        self.notas_selecionadas = []

        self._mostrar_vozes()
