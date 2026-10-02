# -*- coding: utf-8 -*-

"""
Motor ATONAL da Harmonia Funcional Avançada.

Regras principais:
- não usa campo harmônico nem escala para filtrar acordes;
- a nota escolhida pode ocupar, nesta ordem:
  fundamental -> terça -> quinta -> sétima -> nona -> 11ª -> 13ª;
- a letra da fundamental é preservada estruturalmente pela sequência
  1 -> 6 -> 4 -> 2 -> 7 -> 5 -> 3;
- sustenidos, bemóis e acidentes múltiplos são calculados depois;
- as famílias e extensões reutilizam as regras do núcleo principal;
- na família diminuta, o ATONAL admite tanto o diminuto completo
  (7bb) quanto o meio-diminuto (ø7);
- em 13ª, mantém a regra do projeto: se a altura da 13ª já existir
  no acorde, essa formação não é gerada.
"""

from math import prod

import core_harmonia as core


GRAUS_POR_VOZES = {
    3: [1, 3, 5],
    4: [1, 3, 5, 7],
    5: [1, 3, 5, 7, 9],
    6: [1, 3, 5, 7, 9, 11],
    7: [1, 3, 5, 7, 9, 11, 13],
}

NOMES_GRAUS = {
    1: "fundamental",
    3: "terça",
    5: "quinta",
    7: "sétima",
    9: "nona",
    11: "décima primeira",
    13: "décima terceira",
}

# Distância diatônica da fundamental até cada grau.
# Ex.: para C aparecer como 3ª, voltamos 2 letras: C -> A.
DESLOCAMENTO_LETRAS = {
    1: 0,
    3: 2,
    5: 4,
    7: 6,
    9: 1,
    11: 3,
    13: 5,
}


# ============================================================
# MODELOS ATONAIS
# ============================================================

def _opcoes_setima_atonal(qualidade):
    """Retorna (rótulo, intervalo, meio_diminuto)."""
    if qualidade == "diminuto":
        return [
            ("7bb", 9, False),
            ("7", 10, True),
        ]

    return [
        (rotulo, intervalo, False)
        for rotulo, intervalo in core.SETIMAS[qualidade]
    ]


def _iterar_modelos(vozes):
    """
    Produz todos os modelos estruturais válidos para a quantidade
    de vozes solicitada, sem qualquer filtro de escala/campo.
    """
    if vozes not in GRAUS_POR_VOZES:
        raise ValueError("Quantidade de vozes deve ser 3, 4, 5, 6 ou 7.")

    for qualidade in core.ORDEM_QUALIDADES:
        triade = list(core.TRIADES[qualidade]["intervalos"])

        if vozes == 3:
            yield {
                "qualidade": qualidade,
                "intervalos": triade,
                "graus": [1, 3, 5],
                "setima": None,
                "extensoes": [],
                "meio_diminuto": False,
            }
            continue

        for rotulo_7, intervalo_7, meio_diminuto in _opcoes_setima_atonal(qualidade):
            intervalos_4 = triade + [intervalo_7]

            if vozes == 4:
                yield {
                    "qualidade": qualidade,
                    "intervalos": intervalos_4,
                    "graus": [1, 3, 5, 7],
                    "setima": rotulo_7,
                    "extensoes": [],
                    "meio_diminuto": meio_diminuto,
                }
                continue

            for rotulo_9, intervalo_9 in core.NONAS[qualidade]:
                intervalos_5 = intervalos_4 + [intervalo_9]

                if vozes == 5:
                    yield {
                        "qualidade": qualidade,
                        "intervalos": intervalos_5,
                        "graus": [1, 3, 5, 7, 9],
                        "setima": rotulo_7,
                        "extensoes": [rotulo_9],
                        "meio_diminuto": meio_diminuto,
                    }
                    continue

                for rotulo_11, intervalo_11 in core.DECIMAS_PRIMEIRAS[qualidade]:
                    intervalos_6 = intervalos_5 + [intervalo_11]

                    if vozes == 6:
                        yield {
                            "qualidade": qualidade,
                            "intervalos": intervalos_6,
                            "graus": [1, 3, 5, 7, 9, 11],
                            "setima": rotulo_7,
                            "extensoes": [rotulo_9, rotulo_11],
                            "meio_diminuto": meio_diminuto,
                        }
                        continue

                    for rotulo_13, intervalo_13 in core.DECIMAS_TERCEIRAS:
                        # Regra fixa já existente no projeto:
                        # a 13ª não pode repetir, por enarmonia,
                        # uma altura que já existe nas seis vozes.
                        if (intervalo_13 % 12) in {
                            intervalo % 12
                            for intervalo in intervalos_6
                        }:
                            continue

                        yield {
                            "qualidade": qualidade,
                            "intervalos": intervalos_6 + [intervalo_13],
                            "graus": [1, 3, 5, 7, 9, 11, 13],
                            "setima": rotulo_7,
                            "extensoes": [rotulo_9, rotulo_11, rotulo_13],
                            "meio_diminuto": meio_diminuto,
                        }


# ============================================================
# GRAFIA E POSIÇÃO ESTRUTURAL
# ============================================================

def _nota_internacional_preservando_entrada(nota):
    nome = core.nome_internacional_entrada(nota)
    if not nome:
        raise ValueError(f"Nota inválida: {nota}")
    return nome


def _letra_raiz_para_grau(letra_nota, grau):
    indice_nota = core.LETRAS.index(letra_nota)
    deslocamento = DESLOCAMENTO_LETRAS[grau]
    indice_raiz = (indice_nota - deslocamento) % 7
    return core.LETRAS[indice_raiz]


def _criar_registro_para_posicao(nota_digitada, grau_alvo, modelo):
    nota_internacional = _nota_internacional_preservando_entrada(nota_digitada)
    pc_alvo = core.nota_para_pc(nota_digitada)
    letra_nota = nota_internacional[0].upper()

    indice_posicao = modelo["graus"].index(grau_alvo)
    intervalo_da_posicao = modelo["intervalos"][indice_posicao]

    root_pc = (pc_alvo - intervalo_da_posicao) % 12
    letra_raiz = _letra_raiz_para_grau(letra_nota, grau_alvo)
    root_name = core.escrever_pc_na_letra(root_pc, letra_raiz)

    pcs = [
        (root_pc + intervalo) % 12
        for intervalo in modelo["intervalos"]
    ]

    registro = core.criar_registro(
        root_pc,
        root_name,
        modelo["qualidade"],
        pcs,
        modelo["graus"],
        setima=modelo["setima"],
        extensoes=modelo["extensoes"],
        meio_diminuto=modelo["meio_diminuto"],
    )

    registro["sistema"] = "atonal"
    registro["nota_procurada"] = nota_internacional
    registro["grau_nota_procurada"] = grau_alvo
    registro["funcao_nota_procurada"] = NOMES_GRAUS[grau_alvo]

    return registro


# ============================================================
# API PÚBLICA DO MOTOR ATONAL
# ============================================================

def gerar_coluna_atonal(nota_digitada, vozes):
    """
    Gera todos os acordes que contêm a nota escolhida.

    Ordem obrigatória:
    fundamental -> 3ª -> 5ª -> 7ª -> 9ª -> 11ª -> 13ª,
    conforme a quantidade de vozes.
    """
    if vozes not in GRAUS_POR_VOZES:
        raise ValueError("Quantidade de vozes deve ser 3, 4, 5, 6 ou 7.")

    # Valida a nota antes de iniciar.
    core.nota_para_pc(nota_digitada)
    _nota_internacional_preservando_entrada(nota_digitada)

    modelos = list(_iterar_modelos(vozes))
    resultado = []
    chaves = set()

    for grau_alvo in GRAUS_POR_VOZES[vozes]:
        for modelo in modelos:
            registro = _criar_registro_para_posicao(
                nota_digitada,
                grau_alvo,
                modelo,
            )

            # Proteção contra repetição real sem alterar a ordem.
            chave = (
                registro["nome"],
                tuple(registro["pcs"]),
                grau_alvo,
            )
            if chave in chaves:
                continue

            chaves.add(chave)
            resultado.append(registro)

    return resultado


def gerar_colunas_atonais(notas_digitadas, vozes):
    return [
        gerar_coluna_atonal(nota, vozes)
        for nota in notas_digitadas
    ]


def calcular_total_combinacoes_atonais(colunas):
    if not colunas or not all(colunas):
        return 0
    return prod(len(coluna) for coluna in colunas)


def separar_por_posicao(coluna):
    grupos = {}
    for acorde in coluna:
        grau = acorde["grau_nota_procurada"]
        grupos.setdefault(grau, []).append(acorde)
    return grupos


def resumo_quantidades(nota_digitada):
    return {
        vozes: len(gerar_coluna_atonal(nota_digitada, vozes))
        for vozes in (3, 4, 5, 6, 7)
    }


# ============================================================
# VALIDAÇÃO INTERNA
# ============================================================

def validar_motor_atonal():
    esperados = {
        3: 12,
        4: 28,
        5: 85,
        6: 180,
        7: 490,
    }

    por_posicao = {
        3: 4,
        4: 7,
        5: 17,
        6: 30,
        7: 70,
    }

    for vozes, total_esperado in esperados.items():
        coluna = gerar_coluna_atonal("C", vozes)

        if len(coluna) != total_esperado:
            raise RuntimeError(
                f"ATONAL C/{vozes} vozes: esperado {total_esperado}, "
                f"obtido {len(coluna)}."
            )

        grupos = separar_por_posicao(coluna)
        for grau in GRAUS_POR_VOZES[vozes]:
            quantidade = len(grupos.get(grau, []))
            if quantidade != por_posicao[vozes]:
                raise RuntimeError(
                    f"ATONAL C/{vozes} vozes/grau {grau}: "
                    f"esperado {por_posicao[vozes]}, obtido {quantidade}."
                )

    # Caso de referência oficial das tríades de C.
    nomes_c3 = [a["nome"] for a in gerar_coluna_atonal("C", 3)]
    esperado_c3 = [
        "C", "Cm", "C°", "C+",
        "Ab", "Am", "A°", "Ab+",
        "F", "Fm", "F#°", "Fb+",
    ]
    if nomes_c3 != esperado_c3:
        raise RuntimeError(
            "Ordem/grafia das tríades de C não corresponde à regra atonal.\n"
            f"Esperado: {esperado_c3}\nObtido: {nomes_c3}"
        )

    # Caso de referência das tétrades com C na fundamental.
    grupos_c4 = separar_por_posicao(gerar_coluna_atonal("C", 4))
    nomes_fundamental = [a["nome"] for a in grupos_c4[1]]
    esperado_fundamental = [
        "C7", "C7M", "Cm7", "Cm7M", "C°7bb", "Cø7", "C+7M"
    ]
    if nomes_fundamental != esperado_fundamental:
        raise RuntimeError(
            "Tétrades de C na fundamental não correspondem à regra definida.\n"
            f"Esperado: {esperado_fundamental}\nObtido: {nomes_fundamental}"
        )

    # Transposição estrutural: F# deve seguir 1-6-4-2-7-5-3
    # pelas letras F-D-B-G-E-C-A.
    grupos_fs7 = separar_por_posicao(gerar_coluna_atonal("F#", 7))
    letras_esperadas = {
        1: "F",
        3: "D",
        5: "B",
        7: "G",
        9: "E",
        11: "C",
        13: "A",
    }
    for grau, letra in letras_esperadas.items():
        for acorde in grupos_fs7[grau]:
            if acorde["raiz"][0] != letra:
                raise RuntimeError(
                    f"F# no grau {grau}: raiz {acorde['raiz']} deveria "
                    f"preservar a letra {letra}."
                )

    return True
