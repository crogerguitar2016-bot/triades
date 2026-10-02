# -*- coding: utf-8 -*-

from pathlib import Path

from app.servico_harmonia import (
    calcular_resultado,
)

from app.gerador_pdf import (
    gerar_pdfs,
)


# ============================================================
# FLUXO PRINCIPAL
#
# Esta será a função chamada futuramente
# pelo botão CALCULAR E GERAR PDF.
# ============================================================

def executar_calculo_e_pdf(
    tonica,
    modo,
    vozes,
    notas,
    pasta_saida,
    callback_progresso=None,
):
    pasta_saida = Path(
        pasta_saida
    )

    # --------------------------------------------------------
    # 1. CÁLCULO MUSICAL COMPLETO
    # --------------------------------------------------------

    resultado = calcular_resultado(
        tonica=tonica,
        modo=modo,
        vozes=vozes,
        notas=notas,
    )

    total = resultado[
        "total_combinacoes"
    ]


    # --------------------------------------------------------
    # 2. SEM COMBINAÇÕES
    # --------------------------------------------------------

    if total <= 0:

        return {
            "sucesso": True,
            "pdf_gerado": False,
            "mensagem": (
                "Nenhuma combinação encontrada."
            ),
            "resultado": resultado,
            "arquivos": [],
        }


    # --------------------------------------------------------
    # 3. GERAR TODOS OS PDFs NECESSÁRIOS
    # --------------------------------------------------------

    arquivos = gerar_pdfs(
        resultado,
        pasta_saida,
        callback_progresso=callback_progresso,
    )


    # --------------------------------------------------------
    # 4. RESUMO DOS ARQUIVOS
    # --------------------------------------------------------

    resumo_arquivos = []

    for arquivo in arquivos:

        resumo_arquivos.append(
            {
                "parte": arquivo["parte"],
                "total_partes": arquivo["total_partes"],
                "inicio": arquivo["inicio"],
                "fim": arquivo["fim"],
                "nome": arquivo.get(
                    "nome",
                    Path(str(arquivo["caminho"])).name,
                ),
                "caminho": arquivo["caminho"],
                "tamanho_bytes": arquivo.get(
                    "tamanho_bytes",
                    0,
                ),
                "destino_exibicao": arquivo.get(
                    "destino_exibicao"
                ),
            }
        )


    return {
        "sucesso": True,

        "pdf_gerado": True,

        "mensagem": (
            f"{len(resumo_arquivos)} "
            f"PDF(s) gerado(s)."
        ),

        "resultado": resultado,

        "arquivos": (
            resumo_arquivos
        ),
    }
