# -*- coding: utf-8 -*-

from math import prod

import core_harmonia as core


# ============================================================
# CONFIGURAÇÕES
# ============================================================

LIMITE_PREVIA_TELA = 200

LIMITE_COMBINACOES_POR_PDF = 1_000_000


# ============================================================
# 3 BLOCOS PRINCIPAIS
# ============================================================

BLOCOS = {
    "modal": {
        "titulo": "MODAL",
        "modos": (
            "jonio",
            "dorico",
            "frigio",
            "lidio",
            "mixolidio",
            "eolio",
            "locrio",
        ),
    },

    "menor_harmonica": {
        "titulo": "MENOR HARMÔNICA",
        "modos": (
            "menor_harmonica",
            "locrio_natural_6",
            "jonio_sustenido_5",
            "dorico_sustenido_4",
            "frigio_dominante",
            "lidio_sustenido_2",
            "locrio_bb7",
        ),
    },

    "menor_melodica": {
        "titulo": "MENOR MELÓDICA",
        "modos": (
            "menor_melodica",
            "dorico_b2",
            "lidio_aumentado",
            "lidio_dominante",
            "mixolidio_b6",
            "locrio_natural_2",
            "alterado",
        ),
    },
}


# ============================================================
# LISTAGEM DOS BLOCOS
# ============================================================

def listar_blocos():
    return [
        {
            "chave": chave,
            "titulo": dados["titulo"],
        }
        for chave, dados in BLOCOS.items()
    ]


# ============================================================
# LISTAGEM DOS MODOS
# ============================================================

def listar_modos(bloco):
    if bloco not in BLOCOS:
        raise ValueError(
            f"Bloco inválido: {bloco}"
        )

    resultado = []

    for chave_modo in BLOCOS[bloco]["modos"]:

        if chave_modo not in core.MODOS_TODOS:
            raise RuntimeError(
                f"Modo inexistente no núcleo: "
                f"{chave_modo}"
            )

        resultado.append(
            {
                "chave": chave_modo,
                "nome": (
                    core.MODOS_TODOS[
                        chave_modo
                    ]["nome"]
                ),
            }
        )

    return resultado


# ============================================================
# VALIDAÇÃO DO MODO
# ============================================================

def validar_modo(modo):
    if modo not in core.MODOS_TODOS:
        raise ValueError(
            f"Modo inválido: {modo}"
        )

    return True


# ============================================================
# PREPARAR ESCALA / MODO
# ============================================================

def preparar_modo(
    tonica,
    modo,
):
    validar_modo(modo)

    # Valida também a tônica.
    core.nota_para_pc(
        tonica
    )

    escala = core.criar_escala(
        tonica,
        modo,
    )

    escala_nomes = (
        core.nomes_da_escala(
            escala,
            tonica,
        )
    )

    descricao = (
        core.descricao_campo(
            tonica,
            modo,
            escala,
            escala_nomes,
        )
    )

    return {
        "tonica": (
            core.nome_internacional_entrada(
                tonica
            )
        ),
        "modo": modo,
        "nome_modo": (
            core.nome_tipo(
                modo
            )
        ),
        "descricao": descricao,
        "escala": escala,
        "escala_nomes": escala_nomes,
    }


# ============================================================
# GERAR ACORDES
# ============================================================

def gerar_acordes(
    tonica,
    modo,
    vozes,
):
    dados_modo = preparar_modo(
        tonica,
        modo,
    )

    escala = dados_modo[
        "escala"
    ]

    if vozes == 0:

        acordes = (
            core.gerar_todas_as_vozes(
                escala,
                tonica,
                tipo=modo,
            )
        )

    elif vozes in (
        3,
        4,
        5,
        6,
        7,
    ):

        acordes = core.gerar_acordes(
            escala,
            tonica,
            vozes,
            tipo=modo,
        )

    else:

        raise ValueError(
            "Quantidade de vozes inválida. "
            "Use 0, 3, 4, 5, 6 ou 7."
        )

    return acordes


# ============================================================
# GERAR COLUNAS
# ============================================================

def gerar_colunas(
    acordes,
    notas,
):
    if not notas:
        raise ValueError(
            "Selecione pelo menos uma nota."
        )

    colunas = []

    for nota in notas:

        # Validação da nota digitada.
        core.nota_para_pc(
            nota
        )

        coluna = (
            core.gerar_coluna_por_nota(
                nota,
                acordes,
            )
        )

        colunas.append(
            coluna
        )

    return colunas


# ============================================================
# CALCULAR TOTAL
# ============================================================

def calcular_total(
    colunas
):
    if (
        not colunas
        or not all(colunas)
    ):
        return 0

    return prod(
        len(coluna)
        for coluna in colunas
    )


# ============================================================
# QUANTIDADE DE PDFs NECESSÁRIOS
# ============================================================

def calcular_quantidade_pdfs(
    total
):
    if total <= 0:
        return 0

    return (
        total
        + LIMITE_COMBINACOES_POR_PDF
        - 1
    ) // LIMITE_COMBINACOES_POR_PDF


# ============================================================
# DESCRIÇÃO DAS VOZES
# ============================================================

def descricao_vozes(
    vozes
):
    descricoes = {
        3: "3 VOZES — TRÍADES",
        4: "4 VOZES — TÉTRADES / SÉTIMAS",
        5: "5 VOZES — ACORDES DE NONA",
        6: "6 VOZES — DÉCIMAS PRIMEIRAS",
        7: "7 VOZES — DÉCIMAS TERCEIRAS",
        0: "TODAS AS VOZES",
    }

    if vozes not in descricoes:
        raise ValueError(
            f"Quantidade de vozes inválida: "
            f"{vozes}"
        )

    return descricoes[
        vozes
    ]


# ============================================================
# CÁLCULO COMPLETO PARA A INTERFACE
# ============================================================

def calcular_resultado(
    tonica,
    modo,
    vozes,
    notas,
):
    if not notas:
        raise ValueError(
            "Selecione pelo menos uma nota."
        )

    dados_modo = preparar_modo(
        tonica,
        modo,
    )

    acordes = gerar_acordes(
        tonica,
        modo,
        vozes,
    )

    colunas = gerar_colunas(
        acordes,
        notas,
    )

    total = calcular_total(
        colunas
    )

    quantidade_pdfs = (
        calcular_quantidade_pdfs(
            total
        )
    )

    colunas_resumo = []

    for nota, coluna in zip(
        notas,
        colunas,
    ):
        colunas_resumo.append(
            {
                "nota": (
                    core.nome_internacional_entrada(
                        nota
                    )
                ),
                "quantidade": len(
                    coluna
                ),
                "acordes": [
                    acorde["nome"]
                    for acorde in coluna
                ],
            }
        )

    return {
        "tonica": (
            dados_modo["tonica"]
        ),

        "modo": modo,

        "nome_modo": (
            dados_modo[
                "nome_modo"
            ]
        ),

        "descricao_campo": (
            dados_modo[
                "descricao"
            ]
        ),

        "escala": (
            dados_modo[
                "escala"
            ]
        ),

        "escala_nomes": (
            dados_modo[
                "escala_nomes"
            ]
        ),

        "vozes": vozes,

        "descricao_vozes": (
            descricao_vozes(
                vozes
            )
        ),

        "notas": list(
            notas
        ),

        "notas_exibicao": [
            core.nome_internacional_entrada(
                nota
            )
            for nota in notas
        ],

        "acordes": acordes,

        "quantidade_acordes": len(
            acordes
        ),

        "colunas": colunas,

        "colunas_resumo": (
            colunas_resumo
        ),

        "total_combinacoes": (
            total
        ),

        "limite_previa_tela": (
            LIMITE_PREVIA_TELA
        ),

        "limite_por_pdf": (
            LIMITE_COMBINACOES_POR_PDF
        ),

        "quantidade_pdfs": (
            quantidade_pdfs
        ),
    }


# ============================================================
# VALIDAÇÃO DO SERVIÇO
# ============================================================

def validar_servico():
    # O próprio núcleo possui suas validações musicais.
    core.validar_regras_principais()

    if len(
        listar_blocos()
    ) != 3:
        raise RuntimeError(
            "O serviço deve possuir "
            "exatamente 3 blocos."
        )

    total_modos = sum(
        len(
            listar_modos(
                bloco["chave"]
            )
        )
        for bloco in listar_blocos()
    )

    if total_modos != 21:
        raise RuntimeError(
            f"Esperados 21 modos, "
            f"obtidos {total_modos}."
        )

    return True
