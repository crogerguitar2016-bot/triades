# -*- coding: utf-8 -*-

from itertools import product
from math import prod
from pathlib import Path
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    from reportlab.lib.colors import Color
    from reportlab.pdfbase.pdfmetrics import stringWidth
    REPORTLAB_DISPONIVEL = True
except ImportError:
    REPORTLAB_DISPONIVEL = False


# ============================================================
# HARMONIA FUNCIONAL AVANÇADA
# VERSÃO PYDROID 3 - 21 MODOS COM TÔNICA REAL
# Regras consolidadas de 3 a 7 vozes
# ============================================================

ESCALA_CROMATICA_VISUAL = (
    "do, do#, reb, re, re#, mib, mi, fa, fa#, solb, "
    "sol, sol#, lab, lá, la#, sib, si, dó"
)

# Alturas cromáticas (pitch classes)
NOTAS_PC = {
    # Português
    "do": 0, "dó": 0,
    "do#": 1, "dó#": 1, "reb": 1, "réb": 1,
    "re": 2, "ré": 2,
    "re#": 3, "ré#": 3, "mib": 3,
    "mi": 4,
    "fa": 5, "fá": 5,
    "fa#": 6, "fá#": 6, "solb": 6,
    "sol": 7,
    "sol#": 8, "lab": 8, "láb": 8,
    "la": 9, "lá": 9,
    "la#": 10, "lá#": 10, "sib": 10,
    "si": 11,

    # Internacional
    "c": 0,
    "c#": 1, "db": 1,
    "d": 2,
    "d#": 3, "eb": 3,
    "e": 4,
    "f": 5,
    "f#": 6, "gb": 6,
    "g": 7,
    "g#": 8, "ab": 8,
    "a": 9,
    "a#": 10, "bb": 10,
    "b": 11,
}

NOME_ENTRADA = {
    "do": "C", "dó": "C",
    "do#": "C#", "dó#": "C#", "reb": "Db", "réb": "Db",
    "re": "D", "ré": "D",
    "re#": "D#", "ré#": "D#", "mib": "Eb",
    "mi": "E",
    "fa": "F", "fá": "F",
    "fa#": "F#", "fá#": "F#", "solb": "Gb",
    "sol": "G",
    "sol#": "G#", "lab": "Ab", "láb": "Ab",
    "la": "A", "lá": "A",
    "la#": "A#", "lá#": "A#", "sib": "Bb",
    "si": "B",
}

PC_SUSTENIDO = {
    0: "C", 1: "C#", 2: "D", 3: "D#", 4: "E", 5: "F",
    6: "F#", 7: "G", 8: "G#", 9: "A", 10: "A#", 11: "B"
}

PC_BEMOL = {
    0: "C", 1: "Db", 2: "D", 3: "Eb", 4: "E", 5: "F",
    6: "Gb", 7: "G", 8: "Ab", 9: "A", 10: "Bb", 11: "B"
}

NATURAL_PC = {
    "C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11
}

LETRAS = ["C", "D", "E", "F", "G", "A", "B"]


# ============================================================
# 21 MODOS
#
# A nota digitada é SEMPRE a tônica real do modo escolhido.
# ============================================================

MODOS_GREGOS = {
    "jonio": {
        "nome": "Jônio",
        "formula": [2, 2, 1, 2, 2, 2, 1],
        "familia": "maior",
    },
    "dorico": {
        "nome": "Dórico",
        "formula": [2, 1, 2, 2, 2, 1, 2],
        "familia": "maior",
    },
    "frigio": {
        "nome": "Frígio",
        "formula": [1, 2, 2, 2, 1, 2, 2],
        "familia": "maior",
    },
    "lidio": {
        "nome": "Lídio",
        "formula": [2, 2, 2, 1, 2, 2, 1],
        "familia": "maior",
    },
    "mixolidio": {
        "nome": "Mixolídio",
        "formula": [2, 2, 1, 2, 2, 1, 2],
        "familia": "maior",
    },
    "eolio": {
        "nome": "Eólio",
        "formula": [2, 1, 2, 2, 1, 2, 2],
        "familia": "maior",
    },
    "locrio": {
        "nome": "Lócrio",
        "formula": [1, 2, 2, 1, 2, 2, 2],
        "familia": "maior",
    },
}


MODOS_MENOR_HARMONICA = {
    "menor_harmonica": {
        "nome": "Menor Harmônico",
        "formula": [2, 1, 2, 2, 1, 3, 1],
        "familia": "menor_harmonica",
    },
    "locrio_natural_6": {
        "nome": "Lócrio natural 6",
        "formula": [1, 2, 2, 1, 3, 1, 2],
        "familia": "menor_harmonica",
    },
    "jonio_sustenido_5": {
        "nome": "Jônio #5",
        "formula": [2, 2, 1, 3, 1, 2, 1],
        "familia": "menor_harmonica",
    },
    "dorico_sustenido_4": {
        "nome": "Dórico #4",
        "formula": [2, 1, 3, 1, 2, 1, 2],
        "familia": "menor_harmonica",
    },
    "frigio_dominante": {
        "nome": "Frígio Dominante",
        "formula": [1, 3, 1, 2, 1, 2, 2],
        "familia": "menor_harmonica",
    },
    "lidio_sustenido_2": {
        "nome": "Lídio #2",
        "formula": [3, 1, 2, 1, 2, 2, 1],
        "familia": "menor_harmonica",
    },
    "locrio_bb7": {
        "nome": "Lócrio bb7",
        "formula": [1, 2, 1, 2, 2, 1, 3],
        "familia": "menor_harmonica",
    },
}


MODOS_MENOR_MELODICA = {
    "menor_melodica": {
        "nome": "Menor Melódico",
        "formula": [2, 1, 2, 2, 2, 2, 1],
        "familia": "menor_melodica",
    },
    "dorico_b2": {
        "nome": "Dórico b2",
        "formula": [1, 2, 2, 2, 2, 1, 2],
        "familia": "menor_melodica",
    },
    "lidio_aumentado": {
        "nome": "Lídio Aumentado",
        "formula": [2, 2, 2, 2, 1, 2, 1],
        "familia": "menor_melodica",
    },
    "lidio_dominante": {
        "nome": "Lídio Dominante",
        "formula": [2, 2, 2, 1, 2, 1, 2],
        "familia": "menor_melodica",
    },
    "mixolidio_b6": {
        "nome": "Mixolídio b6",
        "formula": [2, 2, 1, 2, 1, 2, 2],
        "familia": "menor_melodica",
    },
    "locrio_natural_2": {
        "nome": "Lócrio natural 2",
        "formula": [2, 1, 2, 1, 2, 2, 2],
        "familia": "menor_melodica",
    },
    "alterado": {
        "nome": "Alterado / Superlócrio",
        "formula": [1, 2, 1, 2, 2, 2, 2],
        "familia": "menor_melodica",
    },
}


MODOS_TODOS = {}
MODOS_TODOS.update(MODOS_GREGOS)
MODOS_TODOS.update(MODOS_MENOR_HARMONICA)
MODOS_TODOS.update(MODOS_MENOR_MELODICA)


TIPOS_MENU = {
    # Modos da escala maior
    1: "jonio",
    2: "dorico",
    3: "frigio",
    4: "lidio",
    5: "mixolidio",
    6: "eolio",
    7: "locrio",

    # Modos da menor harmônica
    8: "menor_harmonica",
    9: "locrio_natural_6",
    10: "jonio_sustenido_5",
    11: "dorico_sustenido_4",
    12: "frigio_dominante",
    13: "lidio_sustenido_2",
    14: "locrio_bb7",

    # Modos da menor melódica
    15: "menor_melodica",
    16: "dorico_b2",
    17: "lidio_aumentado",
    18: "lidio_dominante",
    19: "mixolidio_b6",
    20: "locrio_natural_2",
    21: "alterado",
}


NOMES_TIPOS = {
    chave: dados["nome"]
    for chave, dados in MODOS_TODOS.items()
}


VOZES_MENU = {
    1: (3, "Tríades - 3 vozes"),
    2: (4, "Tétrades / sétimas - 4 vozes"),
    3: (5, "Acordes de nona - 5 vozes"),
    4: (6, "Acordes de décima primeira - 6 vozes"),
    5: (7, "Acordes de décima terceira - 7 vozes"),
    6: (0, "TODAS AS VOZES - 3, 4, 5, 6 e 7 vozes"),
}


# ============================================================
# REGRAS DAS TRÍADES
# ============================================================

TRIADES = {
    "maior": {
        "intervalos": [0, 4, 7],
        "simbolo": "",
    },
    "menor": {
        "intervalos": [0, 3, 7],
        "simbolo": "m",
    },
    "diminuto": {
        "intervalos": [0, 3, 6],
        "simbolo": "°",
    },
    "aumentado": {
        "intervalos": [0, 4, 8],
        "simbolo": "+",
    },
}

ORDEM_QUALIDADES = ["maior", "menor", "diminuto", "aumentado"]


# ============================================================
# REGRAS DAS SÉTIMAS
#
# maior     -> 7 ou 7M
# menor     -> 7 ou 7M
# diminuto  -> somente 7bb
# aumentado -> somente 7M
# Nunca gerar 7#
# ============================================================

SETIMAS = {
    "maior": [
        ("7", 10),
        ("7M", 11),
    ],
    "menor": [
        ("7", 10),
        ("7M", 11),
    ],
    "diminuto": [
        ("7bb", 9),
    ],
    "aumentado": [
        ("7M", 11),
    ],
}


# ============================================================
# REGRAS DAS NONAS
#
# 9b = nona diminuta
# 9  = nona maior
# 9# = nona aumentada
#
# Menor e diminuto NÃO recebem 9#
# ============================================================

NONAS = {
    "maior": [
        ("9b", 1),
        ("9", 2),
        ("9#", 3),
    ],
    "menor": [
        ("9b", 1),
        ("9", 2),
    ],
    "diminuto": [
        ("9b", 1),
        ("9", 2),
    ],
    "aumentado": [
        ("9b", 1),
        ("9", 2),
        ("9#", 3),
    ],
}


# ============================================================
# REGRAS DAS DÉCIMAS PRIMEIRAS
#
# 11  = décima primeira
# 11# = décima primeira aumentada
#
# Diminuto NÃO recebe 11#
# ============================================================

DECIMAS_PRIMEIRAS = {
    "maior": [
        ("11", 5),
        ("11#", 6),
    ],
    "menor": [
        ("11", 5),
        ("11#", 6),
    ],
    "diminuto": [
        ("11", 5),
    ],
    "aumentado": [
        ("11", 5),
        ("11#", 6),
    ],
}


# ============================================================
# REGRAS DAS DÉCIMAS TERCEIRAS
#
# 13b = décima terceira menor
# 13  = décima terceira maior
# 13# = décima terceira aumentada
#
# Se a altura da 13ª já estiver presente no acorde,
# o acorde NÃO é gerado.
# ============================================================

DECIMAS_TERCEIRAS = [
    ("13b", 8),
    ("13", 9),
    ("13#", 10),
]


# ============================================================
# FUNÇÕES BÁSICAS
# ============================================================

def limpar_nota(nota):
    return (
        nota.strip()
        .lower()
        .replace("♯", "#")
        .replace("♭", "b")
    )


def nota_para_pc(nota):
    chave = limpar_nota(nota)

    if chave not in NOTAS_PC:
        raise ValueError(f"Nota inválida: {nota}")

    return NOTAS_PC[chave]


def nome_internacional_entrada(nota):
    chave = limpar_nota(nota)

    if chave in NOME_ENTRADA:
        return NOME_ENTRADA[chave]

    if chave in NOTAS_PC:
        pc = NOTAS_PC[chave]
        if "b" in chave:
            return PC_BEMOL[pc]
        return PC_SUSTENIDO[pc]

    raise ValueError(f"Nota inválida: {nota}")


def preferir_bemois(tonica):
    chave = limpar_nota(tonica)
    return "b" in chave and "#" not in chave


def construir_escala_por_formula(tonica, formula):
    raiz = nota_para_pc(tonica)

    escala = [raiz]
    atual = raiz

    for passo in formula[:-1]:
        atual = (atual + passo) % 12
        escala.append(atual)

    return escala


def criar_escala(tonica, tipo):
    """
    A tônica digitada é sempre a tônica REAL do modo escolhido.
    """
    if tipo not in MODOS_TODOS:
        raise ValueError(
            f"Tipo de campo/modo inválido: {tipo}"
        )

    return construir_escala_por_formula(
        tonica,
        MODOS_TODOS[tipo]["formula"],
    )


def nome_tipo(tipo):
    return NOMES_TIPOS.get(
        tipo,
        tipo.replace("_", " ").title(),
    )


def descricao_campo(tonica, tipo, escala, nomes_escala):
    return (
        f"{nome_internacional_entrada(tonica)} "
        f"{nome_tipo(tipo)}"
    )


def nomes_da_escala(escala, tonica):
    """
    Escreve os sete graus com grafia diatônica correta,
    preservando uma letra diferente para cada grau.

    Ex.:
    C Dórico -> C D Eb F G A Bb
    C Frígio Dominante -> C Db E F G Ab Bb
    C Alterado -> C Db Eb Fb Gb Ab Bb
    """
    nome_raiz = nome_internacional_entrada(tonica)
    letra_raiz = nome_raiz[0].upper()
    indice_raiz = LETRAS.index(letra_raiz)

    nomes = []

    for i, pc in enumerate(escala):
        letra_alvo = LETRAS[
            (indice_raiz + i) % 7
        ]

        nomes.append(
            escrever_pc_na_letra(
                pc,
                letra_alvo,
            )
        )

    return nomes


def mapa_raizes_da_escala(escala, tonica):
    nomes = nomes_da_escala(escala, tonica)
    return {pc: nome for pc, nome in zip(escala, nomes)}


# ============================================================
# GRAFIA DAS NOTAS DOS ACORDES
#
# A validação usa altura sonora.
# A escrita usa a letra estrutural do grau:
# 1, 3, 5, 7, 9, 11 e 13.
# Assim D° aparece como D-F-Ab, não D-F-G#.
# ============================================================

def separar_raiz(nome):
    letra = nome[0].upper()
    acidente = nome[1:]
    return letra, acidente


def escrever_pc_na_letra(pc_alvo, letra_alvo):
    natural = NATURAL_PC[letra_alvo]
    diferenca = (pc_alvo - natural) % 12

    if diferenca > 6:
        diferenca -= 12

    if diferenca == 0:
        return letra_alvo

    if diferenca > 0:
        return letra_alvo + ("#" * diferenca)

    return letra_alvo + ("b" * abs(diferenca))


def escrever_grau(root_name, pc_alvo, numero_grau):
    letra_raiz, _ = separar_raiz(root_name)
    indice_raiz = LETRAS.index(letra_raiz)

    deslocamentos = {
        1: 0,
        3: 2,
        5: 4,
        7: 6,
        9: 1,
        11: 3,
        13: 5,
    }

    letra_alvo = LETRAS[
        (indice_raiz + deslocamentos[numero_grau]) % 7
    ]

    return escrever_pc_na_letra(pc_alvo, letra_alvo)


# ============================================================
# NOMES DOS ACORDES
# ============================================================

def nome_base_triada(root_name, qualidade):
    return root_name + TRIADES[qualidade]["simbolo"]


def nome_acorde(
    root_name,
    qualidade,
    setima=None,
    extensoes=None,
    meio_diminuto=False,
):
    # Meio-diminuto: tríade diminuta + sétima menor.
    # Nomenclatura adotada no projeto: Bø7, C#ø7 etc.
    if meio_diminuto:
        nome = root_name + "ø7"
    else:
        nome = nome_base_triada(root_name, qualidade)

        if setima:
            nome += setima

    extensoes = extensoes or []

    if extensoes:
        nome += "(" + " ".join(extensoes) + ")"

    return nome


# ============================================================
# CRIA UM REGISTRO DE ACORDE
# ============================================================

def criar_registro(
    root_pc,
    root_name,
    qualidade,
    pcs,
    graus,
    setima=None,
    extensoes=None,
    meio_diminuto=False,
):
    notas_escritas = [
        escrever_grau(root_name, pc, grau)
        for pc, grau in zip(pcs, graus)
    ]

    return {
        "raiz_pc": root_pc,
        "raiz": root_name,
        "qualidade": qualidade,
        "nome": nome_acorde(
            root_name,
            qualidade,
            setima=setima,
            extensoes=extensoes,
            meio_diminuto=meio_diminuto,
        ),
        "pcs": list(pcs),
        "graus": list(graus),
        "notas": notas_escritas,
        "setima": setima,
        "meio_diminuto": meio_diminuto,
        "extensoes": list(extensoes or []),
        "vozes": len(pcs),
    }


# ============================================================
# GERA TODOS OS ACORDES VÁLIDOS DA QUANTIDADE DE VOZES
# ============================================================

def gerar_acordes(escala, tonica, vozes, tipo=None):
    if vozes not in (3, 4, 5, 6, 7):
        raise ValueError("Quantidade de vozes deve ser de 3 a 7.")

    escala_set = set(escala)
    nomes_raizes = mapa_raizes_da_escala(escala, tonica)

    acordes = []
    chaves_ja_incluidas = set()

    def adicionar(registro):
        # Evita registros realmente duplicados sem mudar
        # as regras musicais definidas.
        chave = (
            registro["raiz_pc"],
            registro["qualidade"],
            tuple(registro["pcs"]),
            registro["setima"],
            tuple(registro["extensoes"]),
        )

        if chave not in chaves_ja_incluidas:
            chaves_ja_incluidas.add(chave)
            acordes.append(registro)

    # IMPORTANTE:
    # A ordem das raízes é exatamente a ordem da escala,
    # portanto o campo começa sempre pela tônica.
    for root_pc in escala:
        root_name = nomes_raizes[root_pc]

        for qualidade in ORDEM_QUALIDADES:
            intervalos_triada = TRIADES[qualidade]["intervalos"]

            pcs_triada = [
                (root_pc + intervalo) % 12
                for intervalo in intervalos_triada
            ]

            if not all(pc in escala_set for pc in pcs_triada):
                continue

            if vozes == 3:
                adicionar(
                    criar_registro(
                        root_pc,
                        root_name,
                        qualidade,
                        pcs_triada,
                        [1, 3, 5],
                    )
                )
                continue

            # ---------------- SÉTIMA ----------------
            opcoes_setima = list(SETIMAS[qualidade])

            # REGRA DOS 7 MODOS GREGOS:
            # sempre que surgir uma tríade diminuta dentro de
            # Jônio, Dórico, Frígio, Lídio, Mixolídio, Eólio
            # ou Lócrio, ela poderá formar acorde meio-diminuto
            # com sétima menor (ø7), desde que essa sétima
            # pertença à própria escala modal.
            #
            # Exemplo em Mi Mixolídio:
            # G# - B - D + F# = G#ø7
            if (
                tipo in MODOS_GREGOS
                and qualidade == "diminuto"
            ):
                opcoes_setima = [("7", 10)]

            for rotulo_7, intervalo_7 in opcoes_setima:
                pc7 = (root_pc + intervalo_7) % 12

                if pc7 not in escala_set:
                    continue

                pcs_4 = pcs_triada + [pc7]

                meio_diminuto = (
                    qualidade == "diminuto"
                    and rotulo_7 == "7"
                )

                if vozes == 4:
                    adicionar(
                        criar_registro(
                            root_pc,
                            root_name,
                            qualidade,
                            pcs_4,
                            [1, 3, 5, 7],
                            setima=rotulo_7,
                            meio_diminuto=meio_diminuto,
                        )
                    )
                    continue

                # ---------------- NONA ----------------
                for rotulo_9, intervalo_9 in NONAS[qualidade]:
                    pc9 = (root_pc + intervalo_9) % 12

                    if pc9 not in escala_set:
                        continue

                    pcs_5 = pcs_4 + [pc9]

                    if vozes == 5:
                        adicionar(
                            criar_registro(
                                root_pc,
                                root_name,
                                qualidade,
                                pcs_5,
                                [1, 3, 5, 7, 9],
                                setima=rotulo_7,
                                extensoes=[rotulo_9],
                                meio_diminuto=meio_diminuto,
                            )
                        )
                        continue

                    # ---------------- 11ª ----------------
                    for rotulo_11, intervalo_11 in DECIMAS_PRIMEIRAS[qualidade]:
                        pc11 = (root_pc + intervalo_11) % 12

                        if pc11 not in escala_set:
                            continue

                        pcs_6 = pcs_5 + [pc11]

                        if vozes == 6:
                            adicionar(
                                criar_registro(
                                    root_pc,
                                    root_name,
                                    qualidade,
                                    pcs_6,
                                    [1, 3, 5, 7, 9, 11],
                                    setima=rotulo_7,
                                    extensoes=[rotulo_9, rotulo_11],
                                    meio_diminuto=meio_diminuto,
                                )
                            )
                            continue

                        # ---------------- 13ª ----------------
                        for rotulo_13, intervalo_13 in DECIMAS_TERCEIRAS:
                            pc13 = (root_pc + intervalo_13) % 12

                            if pc13 not in escala_set:
                                continue

                            # REGRA FIXA:
                            # Se a 13ª coincidir enarmonicamente
                            # com QUALQUER nota já existente,
                            # este acorde de 13ª não existe.
                            if pc13 in pcs_6:
                                continue

                            pcs_7 = pcs_6 + [pc13]

                            adicionar(
                                criar_registro(
                                    root_pc,
                                    root_name,
                                    qualidade,
                                    pcs_7,
                                    [1, 3, 5, 7, 9, 11, 13],
                                    setima=rotulo_7,
                                    extensoes=[
                                        rotulo_9,
                                        rotulo_11,
                                        rotulo_13,
                                    ],
                                    meio_diminuto=meio_diminuto,
                                )
                            )

    return acordes


def gerar_todas_as_vozes(escala, tonica, tipo=None):
    """
    Reúne, nesta ordem:
    3 vozes -> 4 vozes -> 5 vozes -> 6 vozes -> 7 vozes.

    As regras musicais de cada quantidade de vozes continuam
    exatamente as mesmas da geração individual.
    """
    todos = []

    for quantidade in (3, 4, 5, 6, 7):
        todos.extend(
            gerar_acordes(
                escala,
                tonica,
                quantidade,
                tipo=tipo,
            )
        )

    return todos


# ============================================================
# COLUNAS POR NOTA
#
# Ordem:
# fundamental -> terça -> quinta -> sétima ->
# nona -> 11ª -> 13ª
#
# Se houver vários acordes na mesma função, todos entram.
# ============================================================

def gerar_coluna_por_nota(nota_digitada, acordes):
    pc_procurado = nota_para_pc(nota_digitada)

    if not acordes:
        return []

    quantidade_posicoes = len(acordes[0]["pcs"])

    resultado = []
    nomes_adicionados = set()

    for posicao in range(quantidade_posicoes):
        for acorde in acordes:
            if acorde["pcs"][posicao] == pc_procurado:
                if acorde["nome"] not in nomes_adicionados:
                    nomes_adicionados.add(acorde["nome"])
                    resultado.append(acorde)

    return resultado


# ============================================================
# ENTRADA DE VÁRIAS NOTAS
# ============================================================

def separar_notas_digitadas(texto):
    texto = texto.replace(" e ", ",")
    partes = []

    if "," in texto:
        partes = texto.split(",")
    else:
        partes = texto.split()

    return [p.strip() for p in partes if p.strip()]


# ============================================================
# PDF
# ============================================================

def obter_pasta_saida():
    candidatos = [
        Path("/storage/emulated/0/Download"),
        Path("/sdcard/Download"),
        Path.home() / "storage" / "downloads",
        Path.home() / "Downloads",
        Path.cwd(),
    ]

    for pasta in candidatos:
        try:
            if pasta.exists() and pasta.is_dir():
                teste = pasta / ".teste_harmonia_escrita"
                teste.write_text("ok", encoding="utf-8")
                teste.unlink()
                return pasta
        except Exception:
            pass

    return Path.cwd()


def adicionar_marca_dagua(c, largura, altura):
    c.saveState()
    c.setFont("Helvetica-Bold", 46)
    c.setFillColor(Color(0, 0, 0, alpha=0.08))
    c.translate(largura / 2, altura / 2)
    c.rotate(45)
    c.drawCentredString(0, 0, "PROFESSOR: CARLOS ROGERIO")
    c.rotate(-90)
    c.drawCentredString(0, 0, "PROFESSOR: CARLOS ROGERIO")
    c.restoreState()


def quebrar_linha_pdf(texto, fonte, tamanho, largura_maxima):
    palavras = texto.split()
    linhas = []
    atual = ""

    for palavra in palavras:
        teste = palavra if not atual else atual + " " + palavra

        if stringWidth(teste, fonte, tamanho) <= largura_maxima:
            atual = teste
        else:
            if atual:
                linhas.append(atual)
            atual = palavra

    if atual:
        linhas.append(atual)

    return linhas or [""]


def iniciar_pagina(c, largura, altura):
    adicionar_marca_dagua(c, largura, altura)
    return altura - 55


def escrever_linha_pdf(
    c,
    texto,
    y,
    largura,
    altura,
    fonte="Helvetica",
    tamanho=9,
    x=55,
    espacamento=13,
):
    margem_direita = 45
    largura_maxima = largura - x - margem_direita

    linhas = quebrar_linha_pdf(
        texto,
        fonte,
        tamanho,
        largura_maxima,
    )

    for linha in linhas:
        if y < 55:
            c.showPage()
            y = iniciar_pagina(c, largura, altura)

        c.setFont(fonte, tamanho)
        c.drawString(x, y, linha)
        y -= espacamento

    return y


def gerar_pdf(
    caminho,
    tonica,
    tipo,
    escala_nomes,
    vozes,
    acordes,
    notas_digitadas,
    colunas,
):
    c = canvas.Canvas(str(caminho), pagesize=A4)
    largura, altura = A4

    y = iniciar_pagina(c, largura, altura)

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

    descricao = descricao_campo(
        tonica,
        tipo,
        [nota_para_pc(n) if isinstance(n, str) else n for n in escala_nomes],
        escala_nomes,
    )

    y = escrever_linha_pdf(
        c,
        f"Campo / modo: {descricao}",
        y,
        largura,
        altura,
        tamanho=10,
    )

    y = escrever_linha_pdf(
        c,
        "Escala: " + " - ".join(escala_nomes),
        y,
        largura,
        altura,
        tamanho=10,
        espacamento=18,
    )

    descricao_quantidade = (
        "Todas as vozes: 3, 4, 5, 6 e 7"
        if vozes == 0
        else f"{vozes} vozes"
    )

    y = escrever_linha_pdf(
        c,
        f"Quantidade selecionada: {descricao_quantidade}",
        y,
        largura,
        altura,
        tamanho=10,
        espacamento=20,
    )

    y = escrever_linha_pdf(
        c,
        f"CATÁLOGO DE ACORDES ({len(acordes)})",
        y,
        largura,
        altura,
        fonte="Helvetica-Bold",
        tamanho=11,
        espacamento=17,
    )

    for i, acorde in enumerate(acordes, 1):
        linha = (
            f"{i}. {acorde['nome']} = "
            + " - ".join(acorde["notas"])
        )
        y = escrever_linha_pdf(
            c,
            linha,
            y,
            largura,
            altura,
            tamanho=9,
        )

    y -= 10

    if y < 80:
        c.showPage()
        y = iniciar_pagina(c, largura, altura)

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

    for nota, coluna in zip(notas_digitadas, colunas):
        nomes = ", ".join(a["nome"] for a in coluna) if coluna else "nenhum"
        texto = f"{nome_internacional_entrada(nota)}: {nomes}"

        y = escrever_linha_pdf(
            c,
            texto,
            y,
            largura,
            altura,
            tamanho=9,
        )

    y -= 10

    total = (
        prod(len(coluna) for coluna in colunas)
        if colunas and all(colunas)
        else 0
    )

    y = escrever_linha_pdf(
        c,
        f"COMBINAÇÕES - TOTAL: {total}",
        y,
        largura,
        altura,
        fonte="Helvetica-Bold",
        tamanho=11,
        espacamento=17,
    )

    if total:
        combinacoes = product(
            *[
                [a["nome"] for a in coluna]
                for coluna in colunas
            ]
        )

        for numero, combinacao in enumerate(combinacoes, 1):
            linha = f"{numero}. " + " - ".join(combinacao)

            y = escrever_linha_pdf(
                c,
                linha,
                y,
                largura,
                altura,
                tamanho=8,
                espacamento=12,
            )
    else:
        y = escrever_linha_pdf(
            c,
            "Nenhuma combinação encontrada.",
            y,
            largura,
            altura,
            tamanho=9,
        )

    c.save()


# ============================================================
# EXIBIÇÃO NO TERMINAL
# ============================================================

def imprimir_catalogo(acordes):
    print("\n" + "=" * 60)
    print(f"ACORDES VÁLIDOS: {len(acordes)}")
    print("=" * 60)

    ultima_quantidade = None
    numero = 0

    nomes_grupos = {
        3: "TRÍADES - 3 VOZES",
        4: "TÉTRADES / SÉTIMAS - 4 VOZES",
        5: "NONAS - 5 VOZES",
        6: "DÉCIMAS PRIMEIRAS - 6 VOZES",
        7: "DÉCIMAS TERCEIRAS - 7 VOZES",
    }

    for acorde in acordes:
        quantidade = acorde.get("vozes", len(acorde["pcs"]))

        if quantidade != ultima_quantidade:
            print("\n" + "-" * 60)
            print(nomes_grupos.get(quantidade, f"{quantidade} VOZES"))
            print("-" * 60)
            ultima_quantidade = quantidade

        numero += 1

        print(
            f"{numero:>3}. "
            f"{acorde['nome']} = "
            f"{' - '.join(acorde['notas'])}"
        )


def imprimir_colunas(notas_digitadas, colunas):
    print("\n" + "=" * 60)
    print("COLUNAS POR NOTA")
    print("=" * 60)

    for nota, coluna in zip(notas_digitadas, colunas):
        print(
            f"\n{nome_internacional_entrada(nota)} "
            f"({len(coluna)} acordes):"
        )

        if not coluna:
            print("  Nenhum acorde encontrado.")
            continue

        for acorde in coluna:
            print(f"  {acorde['nome']}")


def imprimir_combinacoes(colunas, limite_tela=200):
    if not colunas or not all(colunas):
        print("\nNenhuma combinação encontrada.")
        return 0

    listas_nomes = [
        [a["nome"] for a in coluna]
        for coluna in colunas
    ]

    total = prod(len(lista) for lista in listas_nomes)

    print("\n" + "=" * 60)
    print(f"COMBINAÇÕES - TOTAL: {total}")
    print("=" * 60)

    for numero, combinacao in enumerate(
        product(*listas_nomes),
        1,
    ):
        if numero > limite_tela:
            break

        print(
            f"{numero}. "
            + " - ".join(combinacao)
        )

    if total > limite_tela:
        print(
            f"\nNa tela foram mostradas apenas as primeiras "
            f"{limite_tela} combinações."
        )
        print(
            "O PDF contém TODAS as combinações."
        )

    return total


# ============================================================
# VALIDAÇÃO INTERNA DAS REGRAS
# ============================================================

def validar_regras_principais():
    escala = criar_escala("la", "menor_harmonica")

    contagens = {
        4: 10,
        5: 8,
        6: 6,
        7: 6,
    }

    for vozes, esperado in contagens.items():
        obtido = len(
            gerar_acordes(
                escala,
                "la",
                vozes,
            )
        )

        if obtido != esperado:
            raise RuntimeError(
                f"Falha na validação de {vozes} vozes: "
                f"esperado {esperado}, obtido {obtido}."
            )

    # Validação das 72 combinações de tríades:
    acordes_3 = gerar_acordes(
        escala,
        "la",
        3,
    )

    colunas = [
        gerar_coluna_por_nota(nota, acordes_3)
        for nota in ["la", "re", "fa"]
    ]

    total = prod(len(c) for c in colunas)

    if total != 72:
        raise RuntimeError(
            f"Falha na validação das tríades: "
            f"esperado 72, obtido {total}."
        )


    # Validação adicional:
    # Si menor harmônico + acordes de sétima + notas Si e Mi
    # Si deve gerar 3 acordes, Mi deve gerar 6, totalizando 18.
    escala_si = criar_escala("si", "menor_harmonica")
    acordes_si_4 = gerar_acordes(
        escala_si,
        "si",
        4,
    )

    coluna_si = gerar_coluna_por_nota(
        "si",
        acordes_si_4,
    )

    coluna_mi = gerar_coluna_por_nota(
        "mi",
        acordes_si_4,
    )

    total_si_mi = len(coluna_si) * len(coluna_mi)

    if len(coluna_si) != 3:
        raise RuntimeError(
            f"Falha na coluna de Si: "
            f"esperado 3, obtido {len(coluna_si)}."
        )

    if len(coluna_mi) != 6:
        raise RuntimeError(
            f"Falha na coluna de Mi: "
            f"esperado 6, obtido {len(coluna_mi)}."
        )

    if total_si_mi != 18:
        raise RuntimeError(
            f"Falha nas combinações Si/Mi com sétimas: "
            f"esperado 18, obtido {total_si_mi}."
        )

    # Validação da opção TODAS AS VOZES.
    todos_la = gerar_todas_as_vozes(
        escala,
        "la",
    )

    esperado_todos_la = sum(
        len(gerar_acordes(escala, "la", v))
        for v in (3, 4, 5, 6, 7)
    )

    if len(todos_la) != esperado_todos_la:
        raise RuntimeError(
            "Falha na validação da opção Todas as Vozes."
        )

    # Validação dos sete modos com C como tônica REAL.
    esperados_modos = {
        "jonio":      [0, 2, 4, 5, 7, 9, 11],
        "dorico":     [0, 2, 3, 5, 7, 9, 10],
        "frigio":     [0, 1, 3, 5, 7, 8, 10],
        "lidio":      [0, 2, 4, 6, 7, 9, 11],
        "mixolidio":  [0, 2, 4, 5, 7, 9, 10],
        "eolio":      [0, 2, 3, 5, 7, 8, 10],
        "locrio":     [0, 1, 3, 5, 6, 8, 10],
    }

    for modo, esperado in esperados_modos.items():
        obtido = criar_escala(
            "do",
            modo,
        )

        if obtido != esperado:
            raise RuntimeError(
                f"Falha na validação de C {modo}: "
                f"esperado {esperado}, obtido {obtido}."
            )

    # ========================================================
    # VALIDAÇÃO DOS 21 MODOS COM DÓ COMO TÔNICA REAL
    # ========================================================
    esperados_21_modos = {
        # Família da maior
        "jonio": [0, 2, 4, 5, 7, 9, 11],
        "dorico": [0, 2, 3, 5, 7, 9, 10],
        "frigio": [0, 1, 3, 5, 7, 8, 10],
        "lidio": [0, 2, 4, 6, 7, 9, 11],
        "mixolidio": [0, 2, 4, 5, 7, 9, 10],
        "eolio": [0, 2, 3, 5, 7, 8, 10],
        "locrio": [0, 1, 3, 5, 6, 8, 10],

        # Família da menor harmônica
        "menor_harmonica": [0, 2, 3, 5, 7, 8, 11],
        "locrio_natural_6": [0, 1, 3, 5, 6, 9, 10],
        "jonio_sustenido_5": [0, 2, 4, 5, 8, 9, 11],
        "dorico_sustenido_4": [0, 2, 3, 6, 7, 9, 10],
        "frigio_dominante": [0, 1, 4, 5, 7, 8, 10],
        "lidio_sustenido_2": [0, 3, 4, 6, 7, 9, 11],
        "locrio_bb7": [0, 1, 3, 4, 6, 8, 9],

        # Família da menor melódica
        "menor_melodica": [0, 2, 3, 5, 7, 9, 11],
        "dorico_b2": [0, 1, 3, 5, 7, 9, 10],
        "lidio_aumentado": [0, 2, 4, 6, 8, 9, 11],
        "lidio_dominante": [0, 2, 4, 6, 7, 9, 10],
        "mixolidio_b6": [0, 2, 4, 5, 7, 8, 10],
        "locrio_natural_2": [0, 2, 3, 5, 6, 8, 10],
        "alterado": [0, 1, 3, 4, 6, 8, 10],
    }

    for modo, esperado in esperados_21_modos.items():
        obtido = criar_escala(
            "do",
            modo,
        )

        if obtido != esperado:
            raise RuntimeError(
                f"Falha na validação do modo {modo}: "
                f"esperado {esperado}, obtido {obtido}."
            )

    # Validação do acorde meio-diminuto no Jônio:
    c_jonio = criar_escala("do", "jonio")
    tetrades_c_jonio = gerar_acordes(
        c_jonio,
        "do",
        4,
        tipo="jonio",
    )

    nomes_c_jonio = [a["nome"] for a in tetrades_c_jonio]

    if "Bø7" not in nomes_c_jonio:
        raise RuntimeError(
            "Falha no Jônio: Bø7 deveria existir no VII grau."
        )

    if len(tetrades_c_jonio) != 7:
        raise RuntimeError(
            f"Falha no Jônio em tétrades: esperado 7 acordes, "
            f"obtido {len(tetrades_c_jonio)}."
        )

    # Validação específica de Mi Mixolídio:
    # a tônica digitada é MI.
    e_mixolidio = criar_escala(
        "mi",
        "mixolidio",
    )

    tetrades_e_mixolidio = gerar_acordes(
        e_mixolidio,
        "mi",
        4,
        tipo="mixolidio",
    )

    nomes_e_mixolidio = [
        a["nome"]
        for a in tetrades_e_mixolidio
    ]

    esperados_e_mixolidio = [
        "E7",
        "F#m7",
        "G#ø7",
        "A7M",
        "Bm7",
        "C#m7",
        "D7M",
    ]

    if nomes_e_mixolidio != esperados_e_mixolidio:
        raise RuntimeError(
            "Falha em Mi Mixolídio nas tétrades.\n"
            f"Esperado: {esperados_e_mixolidio}\n"
            f"Obtido:   {nomes_e_mixolidio}"
        )

    # ========================================================
    # CHECAGEM DO VII GRAU MEIO-DIMINUTO DO JÔNIO
    # ========================================================
    # O acorde ø7 deve continuar existindo quando avançamos
    # para 5, 6 e 7 vozes, obedecendo às regras já definidas:
    #
    # 5 vozes: 9b ou 9; nunca 9#
    # 6 vozes: somente 11; nunca 11#
    # 7 vozes: 13b, 13 ou 13#, apenas quando não repetir
    #           nenhuma altura já existente no acorde.
    #
    # Exemplo de referência: Dó Jônio, VII grau = B.

    acordes_5_c_jonio = gerar_acordes(
        c_jonio,
        "do",
        5,
        tipo="jonio",
    )

    acordes_6_c_jonio = gerar_acordes(
        c_jonio,
        "do",
        6,
        tipo="jonio",
    )

    acordes_7_c_jonio = gerar_acordes(
        c_jonio,
        "do",
        7,
        tipo="jonio",
    )

    nomes_5_c_jonio = [
        a["nome"]
        for a in acordes_5_c_jonio
        if a["raiz"] == "B"
    ]

    nomes_6_c_jonio = [
        a["nome"]
        for a in acordes_6_c_jonio
        if a["raiz"] == "B"
    ]

    nomes_7_c_jonio = [
        a["nome"]
        for a in acordes_7_c_jonio
        if a["raiz"] == "B"
    ]

    # Em Dó Jônio:
    # Bø7 = B-D-F-A
    # 9b = C  -> existe na escala
    # 9  = C# -> não existe
    # Portanto deve existir Bø7(9b).
    if "Bø7(9b)" not in nomes_5_c_jonio:
        raise RuntimeError(
            "Falha no Jônio em 5 vozes: "
            "Bø7(9b) deveria existir."
        )

    # 11 de B = E, que existe na escala.
    if "Bø7(9b 11)" not in nomes_6_c_jonio:
        raise RuntimeError(
            "Falha no Jônio em 6 vozes: "
            "Bø7(9b 11) deveria existir."
        )

    # 13b de B = G, que existe e não repete nenhuma
    # altura já presente em B-D-F-A-C-E.
    if "Bø7(9b 11 13b)" not in nomes_7_c_jonio:
        raise RuntimeError(
            "Falha no Jônio em 7 vozes: "
            "Bø7(9b 11 13b) deveria existir."
        )

    # Proteções contra extensões proibidas para a família diminuta.
    if any("9#" in nome for nome in nomes_5_c_jonio):
        raise RuntimeError(
            "Falha: acorde meio-diminuto não pode receber 9#."
        )

    if any("11#" in nome for nome in nomes_6_c_jonio):
        raise RuntimeError(
            "Falha: acorde meio-diminuto não pode receber 11#."
        )


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def main():
    validar_regras_principais()

    print("\n" + "=" * 60)
    print("HARMONIA FUNCIONAL AVANÇADA")
    print("=" * 60)

    print("\nEscala cromática utilizada:")
    print(ESCALA_CROMATICA_VISUAL)

    tonica = input(
        "\nDigite a tônica do campo/modo "
        "(ex.: do, re, mi, fa#, sib, lá): "
    ).strip()

    try:
        nota_para_pc(tonica)
    except ValueError as erro:
        print(erro)
        return

    print("\nEscolha o campo harmônico / modo:")

    print("\n--- MODOS DA ESCALA MAIOR ---")
    print("1 - Jônio")
    print("2 - Dórico")
    print("3 - Frígio")
    print("4 - Lídio")
    print("5 - Mixolídio")
    print("6 - Eólio")
    print("7 - Lócrio")

    print("\n--- MODOS DA MENOR HARMÔNICA ---")
    print("8  - Menor Harmônico")
    print("9  - Lócrio natural 6")
    print("10 - Jônio #5")
    print("11 - Dórico #4")
    print("12 - Frígio Dominante")
    print("13 - Lídio #2")
    print("14 - Lócrio bb7")

    print("\n--- MODOS DA MENOR MELÓDICA ---")
    print("15 - Menor Melódico")
    print("16 - Dórico b2")
    print("17 - Lídio Aumentado")
    print("18 - Lídio Dominante")
    print("19 - Mixolídio b6")
    print("20 - Lócrio natural 2")
    print("21 - Alterado / Superlócrio")

    try:
        opcao_tipo = int(
            input("Digite a opção: ").strip()
        )
    except ValueError:
        print("Opção inválida.")
        return

    if opcao_tipo not in TIPOS_MENU:
        print("Opção inválida.")
        return

    tipo = TIPOS_MENU[opcao_tipo]

    escala = criar_escala(
        tonica,
        tipo,
    )

    escala_nomes = nomes_da_escala(
        escala,
        tonica,
    )

    print("\n" + "=" * 60)

    descricao = descricao_campo(
        tonica,
        tipo,
        escala,
        escala_nomes,
    )

    print(
        f"CAMPO / MODO: {descricao.upper()}"
    )
    print("=" * 60)

    print(
        "Escala: "
        + " - ".join(escala_nomes)
    )

    print("\nEscolha a quantidade de vozes:")

    for opcao, (_, descricao) in VOZES_MENU.items():
        print(f"{opcao} - {descricao}")

    try:
        opcao_vozes = int(
            input("Digite a opção: ").strip()
        )
    except ValueError:
        print("Opção inválida.")
        return

    if opcao_vozes not in VOZES_MENU:
        print("Opção inválida.")
        return

    vozes, descricao_vozes = VOZES_MENU[
        opcao_vozes
    ]

    if vozes == 0:
        acordes = gerar_todas_as_vozes(
            escala,
            tonica,
            tipo=tipo,
        )
    else:
        acordes = gerar_acordes(
            escala,
            tonica,
            vozes,
            tipo=tipo,
        )

    print(
        f"\nSelecionado: {descricao_vozes}"
    )

    imprimir_catalogo(acordes)

    entrada = input(
        "\nDigite as notas para formar as colunas "
        "(ex.: lá, re, fa): "
    )

    notas_digitadas = separar_notas_digitadas(
        entrada
    )

    if not notas_digitadas:
        print("Nenhuma nota digitada.")
        return

    for nota in notas_digitadas:
        try:
            nota_para_pc(nota)
        except ValueError as erro:
            print(erro)
            return

    colunas = [
        gerar_coluna_por_nota(
            nota,
            acordes,
        )
        for nota in notas_digitadas
    ]

    imprimir_colunas(
        notas_digitadas,
        colunas,
    )

    total = imprimir_combinacoes(
        colunas,
        limite_tela=200,
    )

    pasta_saida = obter_pasta_saida()

    sufixo_vozes = (
        "todas_vozes"
        if vozes == 0
        else f"{vozes}_vozes"
    )

    nome_base_arquivo = (
        nome_internacional_entrada(tonica)
        .replace("#", "s")
        .replace("b", "b")
    )

    nome_arquivo = (
        f"harmonia_"
        f"{nome_base_arquivo}_"
        f"{tipo}_"
        f"{sufixo_vozes}.pdf"
    )

    caminho_pdf = pasta_saida / nome_arquivo

    if not REPORTLAB_DISPONIVEL:
        print("\n" + "=" * 60)
        print(f"TOTAL DE COMBINAÇÕES: {total}")
        print("Os cálculos foram concluídos normalmente.")
        print("PDF não gerado porque o pacote reportlab não está instalado.")
        print("No PyDroid 3, abra Pip e instale: reportlab")
        print("=" * 60)
        return

    try:
        gerar_pdf(
            caminho_pdf,
            tonica,
            tipo,
            escala_nomes,
            vozes,
            acordes,
            notas_digitadas,
            colunas,
        )

        print("\n" + "=" * 60)
        print(f"TOTAL DE COMBINAÇÕES: {total}")
        print(f"PDF gerado em: {caminho_pdf}")
        print("=" * 60)

    except Exception as erro:
        print(
            "\nNão foi possível gerar o PDF:"
        )
        print(erro)


if __name__ == "__main__":
    main()
