# -*- coding: utf-8 -*-

from pathlib import Path


# ============================================================
# NORMALIZAR LISTA DE PDFs GERADOS
# ============================================================

def preparar_lista_pdfs(
    arquivos
):
    resultado = []

    for item in arquivos:

        caminho = Path(
            item["caminho"]
        )

        resultado.append(
            {
                "parte": item[
                    "parte"
                ],

                "total_partes": item[
                    "total_partes"
                ],

                "inicio": item[
                    "inicio"
                ],

                "fim": item[
                    "fim"
                ],

                "nome": caminho.name,

                "caminho": caminho,

                "existe": (
                    caminho.exists()
                ),

                "tamanho_bytes": (
                    caminho.stat().st_size
                    if caminho.exists()
                    else 0
                ),
            }
        )

    return resultado


# ============================================================
# PRIMEIRO PDF
# ============================================================

def obter_primeiro_pdf(
    arquivos
):
    lista = preparar_lista_pdfs(
        arquivos
    )

    if not lista:
        return None

    return lista[0]


# ============================================================
# LOCALIZAR PARTE ESPECÍFICA
# ============================================================

def obter_pdf_por_parte(
    arquivos,
    parte
):
    lista = preparar_lista_pdfs(
        arquivos
    )

    for item in lista:

        if item[
            "parte"
        ] == parte:

            return item

    return None


# ============================================================
# VALIDAR TODOS OS PDFs
# ============================================================

def validar_pdfs(
    arquivos
):
    lista = preparar_lista_pdfs(
        arquivos
    )

    if not lista:
        return {
            "valido": False,
            "quantidade": 0,
            "arquivos": [],
        }

    for item in lista:

        if not item[
            "existe"
        ]:

            return {
                "valido": False,
                "quantidade": len(
                    lista
                ),
                "arquivos": lista,
            }

    return {
        "valido": True,
        "quantidade": len(
            lista
        ),
        "arquivos": lista,
    }
