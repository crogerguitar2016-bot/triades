# -*- coding: utf-8 -*-

"""
Gerador de PDF exclusivo do módulo ATONAL.

O gerador tonal original permanece intocado.
Mantém as mesmas regras de paginação, marca-d'água,
numeração global e divisão automática por 1.000.000.
"""

from itertools import product
from math import ceil
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from app.gerador_pdf import (
    LIMITE_POR_PDF as LIMITE_POR_PDF_TONAL,
    iniciar_pagina,
    escrever_linha_pdf,
    escrever_combinacao,
)

from app.armazenamento_pdf import (
    publicar_pdf_gerado,
    verificar_espaco_para_pdf,
    manutencao_memoria,
)


# Mantém oficialmente o mesmo limite do gerador tonal.
# Fica como variável deste módulo para permitir testes controlados
# sem alterar o limite oficial do projeto.
LIMITE_POR_PDF = LIMITE_POR_PDF_TONAL
INTERVALO_MANUTENCAO_MEMORIA = 50_000


def _sanitizar_nome(texto):
    return (
        str(texto)
        .replace("#", "s")
        .replace(" ", "_")
        .replace("/", "-")
        .replace("\\", "-")
    )


def escrever_informacoes_iniciais_atonal(
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
        "SISTEMA: ATONAL",
        y,
        largura,
        altura,
        fonte="Helvetica-Bold",
        tamanho=11,
        espacamento=16,
    )

    y = escrever_linha_pdf(
        c,
        "Campo harmônico / modo: não se aplica",
        y,
        largura,
        altura,
        tamanho=10,
    )

    y = escrever_linha_pdf(
        c,
        "Escala: não se aplica",
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
            + resultado["descricao_vozes"]
        ),
        y,
        largura,
        altura,
        tamanho=10,
        espacamento=16,
    )

    y = escrever_linha_pdf(
        c,
        (
            "Notas pesquisadas: "
            + " - ".join(
                resultado["notas_exibicao"]
            )
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
            f"PARTE {parte} DE {total_partes}",
            y,
            largura,
            altura,
            fonte="Helvetica-Bold",
            tamanho=11,
            espacamento=16,
        )

        y = escrever_linha_pdf(
            c,
            f"Faixa desta parte: {inicio} a {fim}",
            y,
            largura,
            altura,
            tamanho=9,
            espacamento=18,
        )

    # ========================================================
    # CATÁLOGO DOS ACORDES ENCONTRADOS
    # ========================================================

    acordes = resultado["acordes"]

    y = escrever_linha_pdf(
        c,
        (
            "CATÁLOGO DE ACORDES ENCONTRADOS "
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

    # ========================================================
    # COLUNAS POR NOTA
    # ========================================================

    y = escrever_linha_pdf(
        c,
        "COLUNAS DAS NOTAS PESQUISADAS",
        y,
        largura,
        altura,
        fonte="Helvetica-Bold",
        tamanho=11,
        espacamento=17,
    )

    for coluna in resultado["colunas_resumo"]:
        y = escrever_linha_pdf(
            c,
            (
                f"{coluna['nota']} "
                f"({coluna['quantidade']} acordes)"
            ),
            y,
            largura,
            altura,
            fonte="Helvetica-Bold",
            tamanho=9,
            espacamento=14,
        )

        nomes = (
            ", ".join(
                coluna["acordes"]
            )
            if coluna["acordes"]
            else "nenhum"
        )

        y = escrever_linha_pdf(
            c,
            nomes,
            y,
            largura,
            altura,
            tamanho=8,
            espacamento=12,
        )

        y -= 5

    return y


def criar_nome_arquivo_atonal(
    resultado,
    parte,
    total_partes,
):
    vozes = resultado["vozes"]

    notas = "_".join(
        _sanitizar_nome(nota)
        for nota in resultado["notas_exibicao"]
    )

    # Evita nomes de arquivo excessivamente longos quando muitas
    # notas forem selecionadas. A informação completa permanece no PDF.
    if len(notas) > 80:
        notas = notas[:80].rstrip("_")

    base = (
        f"harmonia_atonal_"
        f"{vozes}_vozes_"
        f"{notas}"
    )

    if total_partes > 1:
        return (
            f"{base}_"
            f"parte_{parte:03d}_"
            f"de_{total_partes:03d}.pdf"
        )

    return base + ".pdf"


def gerar_pdfs_atonais(
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
            "Não existem combinações ATONAIS para gerar o PDF."
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

    # Um único iterador sequencial é usado em todas as partes.
    # Assim a parte seguinte continua exatamente de onde a anterior parou.
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

        nome_arquivo = criar_nome_arquivo_atonal(
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

        # Informações iniciais podem usar quantas páginas forem necessárias.
        escrever_informacoes_iniciais_atonal(
            c,
            largura,
            altura,
            resultado,
            parte,
            total_partes,
            inicio,
            fim,
        )

        # REGRA FIXA: combinações sempre começam em página nova.
        c.showPage()

        y = iniciar_pagina(
            c,
            largura,
            altura,
        )

        y = escrever_linha_pdf(
            c,
            (
                "COMBINAÇÕES ATONAIS - "
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
                    f"PARTE {parte} DE {total_partes} - "
                    f"{inicio} A {fim}"
                ),
                y,
                largura,
                altura,
                fonte="Helvetica-Bold",
                tamanho=9,
                espacamento=18,
            )

        quantidade_desta_parte = (
            fim
            - inicio
            + 1
        )

        passo_progresso = max(
            1,
            total // 1000,
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
                if (
                    numero == 1
                    or numero == total
                    or numero % passo_progresso == 0
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
