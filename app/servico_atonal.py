# -*- coding: utf-8 -*-

"""
Serviço do módulo ATONAL.

Camada intermediária entre:
- interface Kivy;
- motor_atonal.py;
- geração de combinações/PDF.

Não altera o motor tonal existente.
"""

import core_harmonia as core
from app.motor_atonal import (
    gerar_coluna_atonal,
    gerar_colunas_atonais,
    calcular_total_combinacoes_atonais,
)


VOZES_ATONAIS = {
    3: "Tríades - 3 vozes",
    4: "Tétrades / sétimas - 4 vozes",
    5: "Acordes de nona - 5 vozes",
    6: "Acordes de décima primeira - 6 vozes",
    7: "Acordes de décima terceira - 7 vozes",
}

LIMITE_PREVIA_TELA = 200
LIMITE_COMBINACOES_POR_PDF = 1_000_000


def listar_vozes_atonais():
    return dict(VOZES_ATONAIS)


def descricao_vozes_atonal(vozes):
    if vozes not in VOZES_ATONAIS:
        raise ValueError(
            "Quantidade de vozes ATONAL deve ser 3, 4, 5, 6 ou 7."
        )
    return VOZES_ATONAIS[vozes]


def normalizar_notas(notas):
    """
    Valida as notas e preserva a grafia internacional da entrada.
    Exemplos:
    C -> C
    fa# -> F#
    solb -> Gb
    """
    resultado = []

    for nota in notas:
        core.nota_para_pc(nota)
        nome = core.nome_internacional_entrada(nota)
        if not nome:
            raise ValueError(f"Nota inválida: {nota}")
        resultado.append(nome)

    return resultado


def gerar_coluna(nota, vozes):
    return gerar_coluna_atonal(nota, vozes)


def gerar_colunas(notas, vozes):
    return gerar_colunas_atonais(notas, vozes)


def calcular_total(colunas):
    return calcular_total_combinacoes_atonais(colunas)


def calcular_quantidade_pdfs(total):
    if total <= 0:
        return 0

    return (
        total + LIMITE_COMBINACOES_POR_PDF - 1
    ) // LIMITE_COMBINACOES_POR_PDF


def _catalogo_unico(colunas):
    """
    Une os acordes encontrados nas colunas sem alterar a ordem
    da primeira ocorrência.

    O catálogo ATONAL não representa um campo harmônico.
    Ele apenas resume os acordes efetivamente encontrados para
    as notas selecionadas.
    """
    resultado = []
    chaves = set()

    for coluna in colunas:
        for acorde in coluna:
            chave = (
                acorde["nome"],
                tuple(acorde["pcs"]),
                tuple(acorde["graus"]),
            )

            if chave in chaves:
                continue

            chaves.add(chave)
            resultado.append(acorde)

    return resultado


def calcular_resultado_atonal(notas, vozes):
    """
    Retorna um dicionário preparado para interface e PDF.

    Cada nota selecionada cria sua própria coluna.
    O total de combinações é o produto dos tamanhos das colunas.
    """
    if vozes not in VOZES_ATONAIS:
        raise ValueError(
            "Quantidade de vozes ATONAL deve ser 3, 4, 5, 6 ou 7."
        )

    if not notas:
        raise ValueError("Selecione pelo menos uma nota.")

    notas_normalizadas = normalizar_notas(notas)

    colunas = gerar_colunas_atonais(
        notas_normalizadas,
        vozes,
    )

    total = calcular_total_combinacoes_atonais(colunas)

    quantidades_por_nota = {
        nota: len(coluna)
        for nota, coluna in zip(notas_normalizadas, colunas)
    }

    colunas_resumo = []

    for nota, coluna in zip(
        notas_normalizadas,
        colunas,
    ):
        colunas_resumo.append(
            {
                "nota": nota,
                "quantidade": len(coluna),
                "acordes": [
                    acorde["nome"]
                    for acorde in coluna
                ],
            }
        )

    acordes = _catalogo_unico(colunas)

    return {
        "sistema": "atonal",
        "nome_sistema": "ATONAL",
        "descricao_sistema": "ATONAL — não utiliza campo harmônico",

        # Compatibilidade deliberada com o fluxo/PDF tonal.
        "tonica": None,
        "modo": None,
        "nome_modo": None,
        "descricao_campo": "ATONAL — não utiliza campo harmônico",
        "escala": [],
        "escala_nomes": [],

        "vozes": vozes,
        "descricao_vozes": descricao_vozes_atonal(vozes),

        "notas": notas_normalizadas,
        "notas_exibicao": list(notas_normalizadas),

        "acordes": acordes,
        "quantidade_acordes": len(acordes),

        "colunas": colunas,
        "colunas_resumo": colunas_resumo,
        "quantidades_por_nota": quantidades_por_nota,

        "total_combinacoes": total,
        "limite_previa_tela": LIMITE_PREVIA_TELA,
        "limite_por_pdf": LIMITE_COMBINACOES_POR_PDF,
        "quantidade_pdfs": calcular_quantidade_pdfs(total),
    }


def validar_servico_atonal():
    esperados_c = {
        3: 12,
        4: 28,
        5: 85,
        6: 180,
        7: 490,
    }

    for vozes, esperado in esperados_c.items():
        resultado = calcular_resultado_atonal(["C"], vozes)

        obtido = len(resultado["colunas"][0])

        if obtido != esperado:
            raise RuntimeError(
                f"ATONAL C/{vozes} vozes: "
                f"esperado {esperado}, obtido {obtido}."
            )

        if resultado["total_combinacoes"] != esperado:
            raise RuntimeError(
                f"ATONAL total C/{vozes}: "
                f"esperado {esperado}, "
                f"obtido {resultado['total_combinacoes']}."
            )

        if resultado["quantidades_por_nota"]["C"] != esperado:
            raise RuntimeError(
                f"ATONAL resumo C/{vozes}: quantidade incorreta."
            )

    testes_duas_notas = {
        3: 144,       # 12 x 12
        4: 784,       # 28 x 28
        5: 7225,      # 85 x 85
        6: 32400,     # 180 x 180
        7: 240100,    # 490 x 490
    }

    for vozes, esperado in testes_duas_notas.items():
        resultado = calcular_resultado_atonal(
            ["C", "D"],
            vozes,
        )

        if resultado["total_combinacoes"] != esperado:
            raise RuntimeError(
                f"ATONAL C+D/{vozes} vozes: "
                f"esperado {esperado}, "
                f"obtido {resultado['total_combinacoes']}."
            )

    fs = calcular_resultado_atonal(["F#"], 7)
    if len(fs["colunas"][0]) != 490:
        raise RuntimeError(
            "ATONAL F#/7 vozes deveria gerar 490 acordes."
        )

    # Campos necessários para o PDF ATONAL.
    teste_pdf = calcular_resultado_atonal(["C", "D"], 3)
    obrigatorios = (
        "descricao_campo",
        "escala_nomes",
        "descricao_vozes",
        "notas_exibicao",
        "acordes",
        "colunas_resumo",
        "total_combinacoes",
    )
    for campo in obrigatorios:
        if campo not in teste_pdf:
            raise RuntimeError(
                f"Campo obrigatório ausente no resultado ATONAL: {campo}"
            )

    return True
