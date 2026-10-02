# -*- coding: utf-8 -*-

from itertools import product
from math import ceil
from pathlib import Path

from reportlab.lib.colors import Color
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

from app.armazenamento_pdf import (
    publicar_pdf_gerado,
    verificar_espaco_para_pdf,
    manutencao_memoria,
)

LIMITE_POR_PDF = 1_000_000
INTERVALO_MANUTENCAO_MEMORIA = 50_000

MARGEM_ESQUERDA = 55
MARGEM_DIREITA = 45
MARGEM_SUPERIOR = 55
MARGEM_INFERIOR = 55


# ============================================================
# MARCA-D'ÁGUA
# ============================================================

def adicionar_marca_dagua(c, largura, altura):
    c.saveState()

    c.setFont(
        "Helvetica-Bold",
        46,
    )

    c.setFillColor(
        Color(
            0,
            0,
            0,
            alpha=0.08,
        )
    )

    c.translate(
        largura / 2,
        altura / 2,
    )

    c.rotate(45)

    c.drawCentredString(
        0,
        0,
        "PROFESSOR: CARLOS ROGERIO",
    )

    c.rotate(-90)

    c.drawCentredString(
        0,
        0,
        "PROFESSOR: CARLOS ROGERIO",
    )

    c.restoreState()


# ============================================================
# INICIAR PÁGINA
# ============================================================

def iniciar_pagina(c, largura, altura):
    adicionar_marca_dagua(
        c,
        largura,
        altura,
    )

    return (
        altura
        - MARGEM_SUPERIOR
    )


# ============================================================
# QUEBRA DE TEXTO POR LARGURA REAL
# ============================================================

def quebrar_linha_pdf(
    texto,
    fonte,
    tamanho,
    largura_maxima,
):
    palavras = str(texto).split()

    if not palavras:
        return [""]

    linhas = []
    atual = ""

    for palavra in palavras:

        teste = (
            palavra
            if not atual
            else atual + " " + palavra
        )

        if (
            stringWidth(
                teste,
                fonte,
                tamanho,
            )
            <= largura_maxima
        ):
            atual = teste

        else:

            if atual:
                linhas.append(
                    atual
                )

            atual = palavra

    if atual:
        linhas.append(
            atual
        )

    return linhas


# ============================================================
# TEXTO NORMAL
# ============================================================

def escrever_linha_pdf(
    c,
    texto,
    y,
    largura,
    altura,
    fonte="Helvetica",
    tamanho=9,
    x=MARGEM_ESQUERDA,
    espacamento=13,
):
    largura_maxima = (
        largura
        - x
        - MARGEM_DIREITA
    )

    linhas = quebrar_linha_pdf(
        texto,
        fonte,
        tamanho,
        largura_maxima,
    )

    for linha in linhas:

        if y < MARGEM_INFERIOR:

            c.showPage()

            y = iniciar_pagina(
                c,
                largura,
                altura,
            )

        c.setFont(
            fonte,
            tamanho,
        )

        c.drawString(
            x,
            y,
            linha,
        )

        y -= espacamento

    return y


# ============================================================
# ESCREVER UMA COMBINAÇÃO
#
# Regra:
# 01. conteúdo...
#     continuação...
#
# Se a combinação inteira não couber no restante da página,
# começa na página seguinte.
# ============================================================

def escrever_combinacao(
    c,
    numero,
    combinacao,
    y,
    largura,
    altura,
):
    fonte = "Helvetica"
    tamanho = 8
    espacamento = 12

    x_numero = MARGEM_ESQUERDA

    numero_texto = (
        f"{numero:02d}."
    )

    largura_numero = stringWidth(
        numero_texto,
        fonte,
        tamanho,
    )

    x_conteudo = (
        x_numero
        + largura_numero
        + 8
    )

    largura_conteudo = (
        largura
        - x_conteudo
        - MARGEM_DIREITA
    )

    texto = " - ".join(
        combinacao
    )

    linhas = quebrar_linha_pdf(
        texto,
        fonte,
        tamanho,
        largura_conteudo,
    )

    altura_necessaria = (
        len(linhas)
        * espacamento
    )

    altura_util_pagina = (
        altura
        - MARGEM_SUPERIOR
        - MARGEM_INFERIOR
    )

    espaco_restante = (
        y
        - MARGEM_INFERIOR
    )

    # Se a combinação cabe inteira em uma página,
    # mas não cabe no espaço que restou,
    # começa na próxima página.
    if (
        altura_necessaria
        <= altura_util_pagina
        and
        altura_necessaria
        > espaco_restante
    ):
        c.showPage()

        y = iniciar_pagina(
            c,
            largura,
            altura,
        )

    c.setFont(
        fonte,
        tamanho,
    )

    for indice, linha in enumerate(
        linhas
    ):
        if y < MARGEM_INFERIOR:

            c.showPage()

            y = iniciar_pagina(
                c,
                largura,
                altura,
            )

        # Número somente na primeira linha.
        if indice == 0:

            c.drawString(
                x_numero,
                y,
                numero_texto,
            )

        c.drawString(
            x_conteudo,
            y,
            linha,
        )

        y -= espacamento

    # Pequeno espaço entre uma combinação e outra.
    y -= 2

    return y


# ============================================================
# CABEÇALHO + CATÁLOGO + COLUNAS
# ============================================================

def escrever_informacoes_iniciais(
    c,
    largura,
    altura,
    resultado,
    parte,
    total_partes,
    inicio,
    fim,
):
    y = iniciar_pagina(
        c,
        largura,
        altura,
    )

    y = escrever_linha_pdf(
        c,
        "HARMONIA FUNCIONAL AVANÇADA",
        y,
        largura,
        altura,
        fonte="Helvetica-Bold",
        tamanho=14,
        espacamento=18,
    )

    y = escrever_linha_pdf(
        c,
        "PROFESSOR: CARLOS ROGERIO",
        y,
        largura,
        altura,
        fonte="Helvetica-Bold",
        tamanho=10,
        espacamento=18,
    )

    y = escrever_linha_pdf(
        c,
        (
            "Campo / modo: "
            + resultado[
                "descricao_campo"
            ]
        ),
        y,
        largura,
        altura,
        tamanho=10,
    )

    y = escrever_linha_pdf(
        c,
        (
            "Escala: "
            + " - ".join(
                resultado[
                    "escala_nomes"
                ]
            )
        ),
        y,
        largura,
        altura,
        tamanho=10,
        espacamento=18,
    )

    y = escrever_linha_pdf(
        c,
        (
            "Quantidade selecionada: "
            + resultado[
                "descricao_vozes"
            ]
        ),
        y,
        largura,
        altura,
        tamanho=10,
        espacamento=18,
    )

    if total_partes > 1:

        y = escrever_linha_pdf(
            c,
            (
                f"PARTE {parte} DE "
                f"{total_partes}"
            ),
            y,
            largura,
            altura,
            fonte="Helvetica-Bold",
            tamanho=11,
            espacamento=16,
        )

        y = escrever_linha_pdf(
            c,
            (
                f"Faixa desta parte: "
                f"{inicio} a {fim}"
            ),
            y,
            largura,
            altura,
            tamanho=9,
            espacamento=18,
        )

    # --------------------------------------------------------
    # CATÁLOGO
    # --------------------------------------------------------

    acordes = resultado[
        "acordes"
    ]

    y = escrever_linha_pdf(
        c,
        (
            "CATÁLOGO DE ACORDES "
            f"({len(acordes)})"
        ),
        y,
        largura,
        altura,
        fonte="Helvetica-Bold",
        tamanho=11,
        espacamento=17,
    )

    for indice, acorde in enumerate(
        acordes,
        1,
    ):
        texto = (
            f"{indice}. "
            f"{acorde['nome']} = "
            + " - ".join(
                acorde["notas"]
            )
        )

        y = escrever_linha_pdf(
            c,
            texto,
            y,
            largura,
            altura,
            tamanho=9,
        )

    y -= 10

    # --------------------------------------------------------
    # COLUNAS
    # --------------------------------------------------------

    y = escrever_linha_pdf(
        c,
        "COLUNAS DAS NOTAS DIGITADAS",
        y,
        largura,
        altura,
        fonte="Helvetica-Bold",
        tamanho=11,
        espacamento=17,
    )

    for coluna in resultado[
        "colunas_resumo"
    ]:

        nomes = (
            ", ".join(
                coluna[
                    "acordes"
                ]
            )
            if coluna[
                "acordes"
            ]
            else "nenhum"
        )

        texto = (
            f"{coluna['nota']}: "
            f"{nomes}"
        )

        y = escrever_linha_pdf(
            c,
            texto,
            y,
            largura,
            altura,
            tamanho=9,
        )

    return y


# ============================================================
# NOME DO ARQUIVO
# ============================================================

def criar_nome_arquivo(
    resultado,
    parte,
    total_partes,
):
    tonica = (
        resultado["tonica"]
        .replace("#", "s")
        .replace(" ", "_")
    )

    modo = (
        resultado["modo"]
        .replace(" ", "_")
    )

    vozes = resultado[
        "vozes"
    ]

    sufixo_vozes = (
        "todas_vozes"
        if vozes == 0
        else f"{vozes}_vozes"
    )

    base = (
        f"harmonia_"
        f"{tonica}_"
        f"{modo}_"
        f"{sufixo_vozes}"
    )

    if total_partes > 1:

        return (
            f"{base}_"
            f"parte_{parte:03d}_"
            f"de_{total_partes:03d}.pdf"
        )

    return (
        base
        + ".pdf"
    )


# ============================================================
# GERAR TODOS OS PDFs
# ============================================================

def gerar_pdfs(
    resultado,
    pasta_saida,
    callback_progresso=None,
):
    pasta_saida = Path(
        pasta_saida
    )

    pasta_saida.mkdir(
        parents=True,
        exist_ok=True,
    )

    total = resultado[
        "total_combinacoes"
    ]

    if total <= 0:
        raise ValueError(
            "Não existem combinações "
            "para gerar o PDF."
        )

    total_partes = ceil(
        total
        / LIMITE_POR_PDF
    )

    listas_nomes = [
        [
            acorde["nome"]
            for acorde in coluna
        ]
        for coluna in resultado[
            "colunas"
        ]
    ]

    gerador_combinacoes = enumerate(
        product(
            *listas_nomes
        ),
        start=1,
    )

    arquivos_gerados = []

    for parte in range(
        1,
        total_partes + 1,
    ):
        inicio = (
            (parte - 1)
            * LIMITE_POR_PDF
            + 1
        )

        fim = min(
            parte
            * LIMITE_POR_PDF,
            total,
        )

        nome_arquivo = criar_nome_arquivo(
            resultado,
            parte,
            total_partes,
        )

        caminho = (
            pasta_saida
            / nome_arquivo
        )

        verificar_espaco_para_pdf(
            pasta_saida
        )
        manutencao_memoria()

        c = canvas.Canvas(
            str(caminho),
            pagesize=A4,
            pageCompression=1,
        )

        largura, altura = A4

        # ====================================================
        # INFORMAÇÕES INICIAIS
        #
        # Podem ocupar quantas páginas forem necessárias.
        # ====================================================

        escrever_informacoes_iniciais(
            c,
            largura,
            altura,
            resultado,
            parte,
            total_partes,
            inicio,
            fim,
        )

        # ====================================================
        # REGRA OBRIGATÓRIA:
        #
        # As combinações SEMPRE começam
        # em uma página nova.
        # ====================================================

        c.showPage()

        y = iniciar_pagina(
            c,
            largura,
            altura,
        )

        y = escrever_linha_pdf(
            c,
            (
                "COMBINAÇÕES - "
                f"TOTAL GERAL: {total}"
            ),
            y,
            largura,
            altura,
            fonte="Helvetica-Bold",
            tamanho=11,
            espacamento=18,
        )

        if total_partes > 1:

            y = escrever_linha_pdf(
                c,
                (
                    f"PARTE {parte} DE "
                    f"{total_partes} - "
                    f"{inicio} A {fim}"
                ),
                y,
                largura,
                altura,
                fonte="Helvetica-Bold",
                tamanho=9,
                espacamento=18,
            )

        # ====================================================
        # COMBINAÇÕES DESTA PARTE
        # ====================================================

        quantidade_desta_parte = (
            fim
            - inicio
            + 1
        )

        for _ in range(
            quantidade_desta_parte
        ):
            try:
                numero, combinacao = next(
                    gerador_combinacoes
                )

            except StopIteration:
                break

            y = escrever_combinacao(
                c,
                numero,
                combinacao,
                y,
                largura,
                altura,
            )

            if (
                numero
                % INTERVALO_MANUTENCAO_MEMORIA
                == 0
            ):
                manutencao_memoria()

            if callback_progresso is not None:

                passo_progresso = max(
                    1,
                    total // 1000,
                )

                if (
                    numero == 1
                    or
                    numero == total
                    or
                    numero % passo_progresso == 0
                ):

                    callback_progresso(
                        numero,
                        total,
                        parte,
                        total_partes,
                    )

        c.save()
        del c

        manutencao_memoria()

        publicado = publicar_pdf_gerado(
            caminho
        )

        manutencao_memoria()

        arquivos_gerados.append(
            {
                "parte": parte,
                "total_partes": total_partes,
                "inicio": inicio,
                "fim": fim,
                "nome": publicado["nome"],
                "caminho": publicado["caminho"],
                "tamanho_bytes": publicado["tamanho_bytes"],
                "destino_exibicao": publicado["destino_exibicao"],
            }
        )

    return arquivos_gerados
